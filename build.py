'''Builds Dart projects intelligently.
'''

import sublime
import sublime_plugin

from functools import partial
import os
import time

from Dart import PluginLogger
from Dart.lib.sdk import SDK
from Dart.lib.dart_project import find_pubspec_path
from Dart.lib.build.base import DartBuildCommandBase
from Dart.lib.pub_package import DartView
from Dart.lib.pub_package import find_pubspec
from Dart.lib.sdk import Dartium
from Dart.lib.subprocess import GenericBinary
from Dart.lib.sdk import SDK
from Dart.lib.sdk import RunDartWithObservatory
from Dart.lib.panels import OutputPanel
from Dart.lib.sublime import after


_logger = PluginLogger(__name__)


def plugin_unloaded():
    # Kill any existing server.
    # FIXME(guillermooo): this doesn't manage to clean up resources when
    # ST exits.
    sublime.active_window().run_command('dart_run_file', {'kill_only': True,
                                        'file_name': '???'})


class DartStopAllCommand(sublime_plugin.WindowCommand):
    '''Stops Dart programs or services run by this plugin.

    Namely:
      - pub serve
      - plain server apps
      - server apps through Observatory
    '''

    def run(self):
        self.window.run_command('dart_run_file', {
            "file_name": "???",
            "kill_only": True
            })

        self.window.run_command("dart_exec", {
            "kill": True
            })


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
                     DartRunFileCommand.server_running)
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


class DartBuildProjectCommand(sublime_plugin.WindowCommand):
    '''Runs the current file in the most appropriate way.
    '''

    def run(self, action='primary'):
        '''
        @action
          One of: primary, secondary
        '''
        view = self.window.active_view()
        if DartView(view).is_pubspec:
            self.window.run_command('dart_build_pubspec', {
                'action': action,
                'file_name': view.file_name()
                })
            return

        self.window.run_command('dart_run_file', {
            'action': action,
            'file_name': view.file_name(),
            })


class DartRunFileCommand(DartBuildCommandBase):
    '''Runs a file with the most appropriate action.

    Intended for .dart and .html files.
    '''
    observatory = None
    server_running = False

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
            return

    def run(self, file_name, action='primary', kill_only=False):
        '''
        @action
          One of: primary, secondary
        '''

        if DartRunFileCommand.server_running:
            self.execute(kill=True)
            DartRunFileCommand.server_running = False

        self.stop_server_observatory()

        if kill_only:
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

        working_dir = find_pubspec_path(file_name)
        if not working_dir:
            working_dir = os.path.dirname(file_name)

        sdk = SDK()
        dart_view = DartView(self.window.active_view())

        if dart_view.is_server_app:
            self.run_server_app(file_name, working_dir, action)
            return

        if dart_view.is_web_app:
            self.run_web_app(dart_view, working_dir, action)
            return

        if action == 'primary':
            self.execute(
                    cmd=[sdk.path_to_dart2js,
                                '--minify', '-o', file_name + '.js',
                                file_name],
                    working_dir=working_dir,
                    file_regex="(\\S*):(\\d*):(\\d*): (.*)",
                    preamble='Running dart2js...\n',
                    )
            return

        if action != 'secondary':
            _logger("unknown action: %s", action)
            return

        self.run_server_app(file_name, working_dir, action)

    def start_default_browser(self):
        sdk = SDK()

        if not sdk.path_to_default_user_browser:
            _logger.info('no default user browser defined')
            print("Dart: No default user browser defined in User settings")
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
                                   cwd=os.path.dirname(path)
                                   ))
            return

        path = sdk.path_to_default_user_browser
        bin_ = GenericBinary(path)
        after(1000, lambda: bin_.start(
                               args=[url],
                               shell=True,
                               cwd=os.path.dirname(path)
                               ))

    def run_server_app(self, file_name, working_dir, action):
        if action == 'secondary':
            # run with observatory
            # we need to do additional processing in this case, so we don't
            # use the regular .execute() command to manage the subprocess.
            self.panel = OutputPanel('dart.out')
            self.panel.write('='*80)
            self.panel.write('\n')
            self.panel.write('Running dart with Observatory.\n')
            self.panel.write('='*80)
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
                url = 'http://localhost:{}'.format(DartRunFileCommand.observatory.port)
                if DartRunFileCommand.observatory.port is None:
                    _logger.debug('could not capture observatory port')
                    print("Dart: Cannot start Observatory because its port couldn't be found")
                    return
                d.start(url)
            after(1250, lambda: start_dartium())
            return

        self.execute(
            cmd=[SDK().path_to_dart, '--checked', file_name],
            working_dir=working_dir,
            file_regex="'file:///(.+)': error: line (\\d+) pos (\\d+): (.*)$",
            preamble='Running dart...\n',
            )

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
            DartRunFileCommand.server_running = True
            self.start_default_browser()
            return

        cmd=[sdk.path_to_pub, 'serve']
        if dart_view.is_example:
            cmd.append('example')
        self.execute(cmd=cmd, working_dir=working_dir)
        DartRunFileCommand.server_running = True

        url = 'http://localhost:8080'
        if dart_view.url_path:
            url = url + "/" + dart_view.url_path
        after(1000, lambda: Dartium().start(url))

    def stop_server_observatory(self):
        if DartRunFileCommand.observatory:
            DartRunFileCommand.observatory.stop()
            DartRunFileCommand.observatory = None

    def on_data(self, text):
        self.panel.write(text)

    def on_error(self, text):
        self.panel.write(text)


class DartBuildPubspecCommand(DartBuildCommandBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    '''Build behavior for pubspec.yaml.
    '''
    PUB_CMDS = [
                'deps',
                'help',
                'upgrade',
                'version',
               ]

    def run(self, action, file_name):
        '''
        @action
          One of: 'primary', 'secondary'

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

        f = partial(self.on_done, file_name, working_dir)
        self.window.show_quick_panel(self.PUB_CMDS, f)

    def on_done(self, file_name, working_dir, idx):
        if idx == -1:
            return

        self.execute(
            cmd=[SDK().path_to_pub] + [self.PUB_CMDS[idx]],
            working_dir=os.path.dirname(file_name),
            preamble="Running pub...\n",
            )
