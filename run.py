'''Builds Dart projects intelligently.
'''

import sublime
import sublime_plugin

import os
import time

from Dart import PluginLogger
from Dart.lib.build.base import DartBuildCommandBase
from Dart.lib.panels import OutputPanel
from Dart.lib.pub_package import DartView
from Dart.lib.pub_package import find_pubspec
from Dart.lib.sdk import Dartium
from Dart.lib.sdk import RunDartWithObservatory
from Dart.lib.sdk import SDK
from Dart.lib.sublime import after
from Dart.lib.subprocess import GenericBinary


_logger = PluginLogger(__name__)


def plugin_unloaded():
    # Kill any existing server.
    # FIXME(guillermooo): this doesn't manage to clean up resources when
    # ST exits.
    sublime.active_window().run_command('dart_run_file', {'kill_only': True,
                                        'file_name': '???'})


class DartRunInObservatoryCommand(sublime_plugin.WindowCommand):
    '''Runs a server app through the Observatory.

    Note:
        - We don't need this for web apps, because in that case
          the Observatory is always available in the Dartium
          Dev Tools panel.
    '''
    def is_enabled(self):
        # TODO(guillermooo): Fix this in pub_package.DartView
        view = self.window.active_view()
        if not view:
            return False
        dart_view = DartView(view)
        return (not dart_view.is_web_app) and dart_view.is_server_app

    def run(self):
        # TODO(guillermooo): Document this
        view = self.window.active_view()
        self.window.run_command('dart_run_file', {
            "file_name": view.file_name(),
            "action": "secondary"
            })


class ContextProvider(sublime_plugin.EventListener):
    '''Implements the 'dart_can_do_launch' context for .sublime-keymap
    files.
    '''
    def on_query_context(self, view, key, operator, operand, match_all):
        if key == 'dart_can_do_launch':
            value = DartView(view).is_runnable
            return self._check(value, operator, operand, match_all)

        if key == 'dart_can_show_observatory':
            value = DartRunFileCommand.observatory != None
            return self._check(value, operator, operand, match_all)

        if key == 'dart_services_running':
            value = (DartRunFileCommand.observatory != None or
                     DartRunFileCommand.is_server_running,
                     DartRunFileCommand.is_script_running)
            return self._check(value, operator, operand, match_all)

    def _check(self, value, operator, operand, match_all):
        if operator == sublime.OP_EQUAL:
            if operand == True:
                return value
            elif operand == False:
                return not value
        elif operator == sublime.OP_NOT_EQUAL:
            if operand == True:
                return not value
            elif operand == False:
                return value


class DartSmartRunCommand(sublime_plugin.WindowCommand):
    '''Runs the current file in the most appropriate way.
    '''

    def run(self, action='primary', kill_only=False):
        '''
        @action
          One of: primary, secondary
        '''
        view = self.window.active_view()
        if DartView(view).is_pubspec:
            self.window.run_command('dart_run_pubspec', {
                'action': action,
                'file_name': view.file_name()
                })
            return

        self.window.run_command('dart_run_file', {
            'action': action,
            'file_name': view.file_name(),
            'kill_only': kill_only,
            })


class DartRunFileCommand(DartBuildCommandBase):
    '''Runs a file with the most appropriate action.

    Runs .dart and .html files.
    '''
    observatory = None
    is_server_running = False
    is_script_running = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.panel = None

    def __del__(self):
        # FIXME(guillermooo): this doesn't manage to clean up resources when
        # ST exits.
        self.stop_server_observatory()
        self.execute(kill=True)

    def observatory_port(self):
        try:
            return DartRunFileCommand.observatory.port
        except Exception:
            _logger.error('could not retrieve Observatory port')
            return

    def run(self, file_name=None, action='primary', kill_only=False):
        '''
        @action
          One of: primary, secondary

        @kill_only
          Whether we should simply kill any running processes.
        '''
        assert kill_only or (file_name and not kill_only), 'wrong call'

        # First, clean up any existing processes.
        if DartRunFileCommand.is_server_running:
            self.execute(kill=True)
            DartRunFileCommand.is_server_running = False

        self.stop_server_observatory()

        if kill_only:
            self.window.run_command("dart_exec", {
                "kill": True
                })
            DartRunFileCommand.is_script_running = False
            return

        try:
            working_dir = os.path.dirname(find_pubspec(file_name))
        except:
            try:
                if not working_dir:
                    working_dir = os.path.dirname(file_name)
            except:
                _logger.debug('cannot run an unsaved file')
                return

        dart_view = DartView(self.window.active_view())

        if dart_view.is_server_app:
            self.run_server_app(file_name, working_dir, action)
            return

        if dart_view.is_web_app:
            self.run_web_app(dart_view, working_dir, action)
            return

        # At this point, we are looking at a file that either:
        #   - is not a .dart or .html file
        #   - is outside of a pub package
        # As a last restort, run the file as a script, but only if the user
        # requested a 'secondary' action.
        if action != 'secondary' or not dart_view.is_dart_file:
            print("Dart: Cannot determine best action for {}".format(
                  dart_view.view.file_name()
                  ))
            _logger.debug("cannot determine best run action for %s",
                          dart_view.view.file_name())
            return

        self.run_server_app(file_name, working_dir, action)

    def start_default_browser(self):
        sdk = SDK()

        if not sdk.path_to_default_user_browser:
            _logger.info('no default user browser defined')
            print("Dart: No default user browser defined "
                  "in Dart plugin settings")
            return

        dart_view = DartView(self.window.active_view())
        url = 'http://localhost:8080'
        if dart_view.url_path:
            url = url + "/" + dart_view.url_path

        # TODO(guillermooo): make GUIProcess wrapper to abstract out some of
        # the stuff below?
        if sublime.platform() == 'osx':
            bin_ = GenericBinary('open', sdk.path_to_default_user_browser)
            after(1000, lambda: bin_.start(args=[url]))
            return

        elif sublime.platform() == 'windows':
            # FIXME(guillermooo): On Windows, Firefox won't work when started
            # from the cmdline only. If it's started first from the shell, it
            # will work here as well.
            path = sdk.path_to_default_user_browser
            bin_ = GenericBinary(path)
            after(1000, lambda: bin_.start(
                                   args=[url],
                                   shell=True,
                                   cwd=os.path.dirname(path),
                                   ))
            return

        path = sdk.path_to_default_user_browser
        bin_ = GenericBinary(path)
        after(1000, lambda: bin_.start(
                               args=[url],
                               shell=True,
                               cwd=os.path.dirname(path),
                               ))

    def run_server_app(self, file_name, working_dir, action):
        if action == 'secondary':
            # run with observatory
            # we need to do additional processing in this case, so we don't
            # use the regular .execute() method to manage the subprocess.
            self.panel = OutputPanel('dart.out')
            self.panel.write('=' * 80)
            self.panel.write('\n')
            self.panel.write('Running dart with Observatory.\n')
            self.panel.write('=' * 80)
            self.panel.write('\n')
            self.panel.write('Starting Dartium...\n')
            self.panel.show()
            DartRunFileCommand.observatory = RunDartWithObservatory(
                                                           file_name,
                                                           cwd=working_dir,
                                                           listener=self)
            DartRunFileCommand.observatory.start()
            def start_dartium():
                d = Dartium()
                port = DartRunFileCommand.observatory.port
                if port is None:
                    _logger.debug('could not capture observatory port')
                    print("Dart: Cannot start Observatory "
                          "because its port couldn't be retrieved")
                    return
                d.start('http://localhost:{}'.format(port))

            after(1000, lambda: start_dartium())
            return

        self.execute(
            cmd=[SDK().path_to_dart, '--checked', file_name],
            working_dir=working_dir,
            file_regex=r"'file:///(.+)': error: line (\d+) pos (\d+): (.*)$",
            preamble='Running dart...\n',
            )
        DartRunFileCommand.is_script_running = True

    def run_web_app(self, dart_view, working_dir, action):
        sdk = SDK()

        if action == 'secondary':
            if not sdk.path_to_default_user_browser:
                print("Dart: No default browser found")
                _logger.info('no default browser found')
                return

            cmd=[sdk.path_to_pub, 'serve']
            if dart_view.is_example:
                cmd.append('example')
            self.execute(cmd=cmd, working_dir=working_dir)
            DartRunFileCommand.is_server_running = True
            self.start_default_browser()
            return

        cmd=[sdk.path_to_pub, 'serve']
        if dart_view.is_example:
            cmd.append('example')
        self.execute(cmd=cmd, working_dir=working_dir)
        DartRunFileCommand.is_server_running = True

        url = 'http://localhost:8080'
        if dart_view.url_path:
            url = url + "/" + dart_view.url_path
        after(1000, lambda: Dartium().start(url))

    def stop_server_observatory(self):
        if DartRunFileCommand.observatory:
            DartRunFileCommand.observatory.stop()
            DartRunFileCommand.observatory = None

            if self.panel:
                self.panel.write('[Observatory stopped]')


    def on_data(self, text):
        self.panel.write(text)

    def on_error(self, text):
        self.panel.write(text)


class DartRunPubspecCommand(DartBuildCommandBase):
    '''Performs actions on a pubspec.yaml file.
    '''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    PUB_CMDS = [
                'deps',
                'help',
                'upgrade',
                'version',
               ]

    def run(self, action, file_name):
        '''
        @action
          One of: primary, secondary

        @file_name
          A valid path.
        '''
        working_dir = os.path.dirname(file_name)

        if action == 'primary':
            self.execute(
                cmd=[SDK().path_to_pub] + ['get'],
                working_dir=working_dir,
                preamble="Running pub...\n",
                )
            return

        if action != 'secondary':
            _logger.error('not implemented')
            return

        f = lambda i: self.on_done(i, file_name, working_dir)
        self.window.show_quick_panel(self.PUB_CMDS, f)

    def on_done(self, idx, file_name, working_dir):
        if idx == -1:
            return

        self.execute(
            cmd=[SDK().path_to_pub] + [self.PUB_CMDS[idx]],
            working_dir=os.path.dirname(file_name),
            preamble="Running pub...\n",
            )
