# Copyright (c) 2014, Guillermo López-Anglada. Please see the AUTHORS file for details.
# All rights reserved. Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.)

'''Builds Dart projects intelligently.
'''

import sublime
import sublime_plugin

import os
import time
import re

from Dart import PluginLogger
from Dart.lib.build.base import DartBuildCommandBase
from Dart.lib.panels import OutputPanel
from Dart.lib.pub_package import DartFile
from Dart.lib.pub_package import find_pubspec
from Dart.lib.sdk import Dartium
from Dart.lib.sdk import RunDartWithObservatory
from Dart.lib.sdk import SDK
from Dart.lib.sublime import after
from Dart.lib.subprocess import GenericBinary
from Dart.lib.sdk import PubServe
from Dart.lib.event import EventSource
from Dart.lib import ga

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
        # TODO(guillermooo): Fix this in pub_package.DartFile
        view = self.window.active_view()
        if not view:
            return False
        dart_view = DartFile(view)
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
            value = DartFile(view).is_runnable
            return self._check(value, operator, operand, match_all)

        if key == 'dart_can_do_relaunch':
            value = (DartFile(view).is_runnable or
                     DartSmartRunCommand.last_run_file[1])
            return self._check(value, operator, operand, match_all)

        if key == 'dart_can_show_observatory':
            value = DartRunFileCommand.observatory != None
            return self._check(value, operator, operand, match_all)

        if key == 'dart_services_running':
            value = any((DartRunFileCommand.observatory != None,
                        DartRunFileCommand.is_server_running,
                        DartRunFileCommand.is_script_running))
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


class PubServeListener(object):
    '''Special listener to capture 'pub serve --port=0' port information.
    Also starts Dartium.
    '''
    def __init__(self, instance, panel, path):
        self.instance = instance
        self.panel = panel
        self.path = path

    def on_data(self, text):
        if not self.instance.port:
            m = re.match('^Serving .*? on http://.*?:(\d+)', text)
            if m:
                self.instance.port = int(m.groups()[0])
                _logger.debug('captured pub serve port: %d' % self.instance.port)
                _logger.debug('starting dartium...')
                self.panel.write('Starting Dartium...\n')
                url = 'http://localhost:' + str(self.instance.port)
                if self.path:
                    url += '/' + self.path
                Dartium().start(url)
        self.panel.write(text)

    def on_error(self, text):
        self.panel.write(text)


class DartSmartRunCommand(DartBuildCommandBase):
    '''Runs the current file in the most appropriate way.
    '''
    last_run_file = (None, None)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_event_handler(EventSource.ON_DART_RUN,
                               DartSmartRunCommand.on_dart_run)

    def run(self, action='primary', force_update=False, kill_only=False):
        '''
        @action
          One of: primary, secondary
        '''

        self.raise_event(self, EventSource.ON_DART_RUN)

        try:
            view = self.window.active_view()
        except TypeError:
            return

        if force_update or DartSmartRunCommand.last_run_file[0] is None:
            try:
                DartSmartRunCommand.last_run_file = (
                                                DartFile(view).is_pubspec,
                                                view.file_name())
            except TypeError:
                return

        if DartSmartRunCommand.last_run_file[0]:
            self.window.run_command('dart_run_pubspec', {
                'action': action,
                'file_name': DartSmartRunCommand.last_run_file[1]
                })
            return

        self.window.run_command('dart_run_file', {
            'action': action,
            'file_name': DartSmartRunCommand.last_run_file[1],
            'kill_only': kill_only,
            })

    # This class will be instantiated for each view/window, so we need to
    # ensure that only one function will be registered as event handler.
    # Therefore, we use a function whose id is the same across all instances.
    @classmethod
    def on_dart_run(cls, *args, **kwargs):
        ga.Event(category='actions',
                 action='on_dart_run',
                 label='Running "Run" command',
                 value=1,
                 ).send()


class DartRunFileCommand(DartBuildCommandBase):
    '''Runs a file with the most appropriate action.

    Runs .dart and .html files.
    '''
    observatory = None
    pub_serve = None
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

    @property
    def pub_serve_port(self):
        try:
            return DartRunFileCommand.pub_serve.port
        except Exception:
            _logger.error('could not retrieve pub serve port')
            return

    @pub_serve_port.setter
    def pub_serve_port(self, value):
        DartRunFileCommand.pub_serve.port = value

    def run(self, file_name=None, action='primary', kill_only=False):
        '''
        @action
          One of: primary, secondary

        @kill_only
          Whether we should simply kill any running processes.
        '''
        assert kill_only or (file_name and not kill_only), 'wrong call'

        # First, clean up any existing prosesses.
        if DartRunFileCommand.is_server_running:
            self.execute(kill=True)
            self.pub_serve.stop()
            DartRunFileCommand.is_server_running = False
            if self.panel:
                self.panel.write('[pub serve stopped]\n')

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

        dart_view = DartFile.from_path(file_name)

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
                  dart_view.path
                  ))
            _logger.debug("cannot determine best run action for %s",
                          dart_view.path)
            return

        self.run_server_app(file_name, working_dir, action)

    def start_default_browser(self, file_name):
        sdk = SDK()

        if not sdk.path_to_default_user_browser:
            _logger.info('no default user browser defined')
            print("Dart: No default user browser defined "
                  "in Dart plugin settings")
            return

        dart_view = DartFile.from_path(file_name)
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

        # TODO(guillermooo): improve event args
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
            self.start_default_browser(dart_view.path)
            return

        self.panel = OutputPanel('dart.out')
        self.panel.write('=' * 80)
        self.panel.write('\n')
        self.panel.write('Running pub serve...\n')
        self.panel.write('=' * 80)
        self.panel.write('\n')
        self.panel.show()

        DartRunFileCommand.pub_serve = PubServe(
                                        cwd=working_dir,
                                        is_example=dart_view.is_example,
                                        )
        pub_serve_listener = PubServeListener(DartRunFileCommand.pub_serve,
                                              self.panel,
                                              dart_view.url_path)
        DartRunFileCommand.pub_serve.listener = pub_serve_listener
        DartRunFileCommand.pub_serve.start()

        DartRunFileCommand.is_server_running = True

    def stop_server_observatory(self):
        if DartRunFileCommand.observatory:
            DartRunFileCommand.observatory.stop()
            DartRunFileCommand.observatory = None

            if self.panel:
                self.panel.write('[Observatory stopped]\n')

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
                panel_name='dart.out',
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
            panel_name='dart.out',
            )
