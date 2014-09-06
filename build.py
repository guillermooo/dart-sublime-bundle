'''Builds Dart projects intelligently.
'''

import sublime
import sublime_plugin

from functools import partial
import os
import time

from Dart import PluginLogger
from Dart.lib.build.base import DartBuildCommandBase
from Dart.lib.dart_project import DartView
from Dart.lib.dart_project import find_pubspec
from Dart.lib.sdk import Dartium
from Dart.lib.sdk import GenericBinary
from Dart.lib.sdk import SDK


_logger = PluginLogger(__name__)


def plugin_unloaded():
    # Kill any existing server.
    sublime.active_window().run_command('dart_run', {'kill_only': True})


class ContextProvider(sublime_plugin.EventListener):
    '''Implements the 'dart_can_do_launch' context for .sublime-keymap
    files.
    '''
    def on_query_context(self, view, key, operator, operand, match_all):
        if key == 'dart_can_do_launch':
            return DartView(view).is_runnable


class DartBuildProjectCommand(sublime_plugin.WindowCommand):
    '''Orchestrates different build tasks.

    Meant to be called from a key binding.
    '''
    def run(self, action='primary'):
        '''
        @action
          One of: 'primary', 'secondary'
        '''
        view = self.window.active_view()
        if DartView(view).is_pubspec:
            self.window.run_command('dart_build_pubspec', {
                'action': action,
                'file_name': view.file_name()
                })
            return

        self.window.run_command('dart_run', {
            'action': action,
            'file_name': view.file_name(),
            })


class DartRunCommand(DartBuildCommandBase):
    '''Runs a file with the most appropriate action.

    Intended for .dart and .html files.
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.server = False

    def run(self, file_name, action='primary', kill_only=False):
        '''
        @action
          One of: primary, secondary
        '''
        if self.server and kill_only:
            self.execute(kill=True)
            self.server = False
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

        sdk = SDK()
        dart_view = DartView(self.window.active_view())

        if dart_view.is_server_app:
            self.run_server_app(file_name, working_dir)
            return

        if dart_view.is_web_app:
            self.run_web_app(file_name, working_dir, action)
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

        self.run_server_app(file_name, working_dir)

    def start_default_browser(self):
        sdk = SDK()

        # TODO(guillermooo): make GUIProcess wrapper to abstract out some of
        # the stuff below?
        if sublime.platform() == 'osx':
            bin_ = GenericBinary('open', sdk.path_to_default_user_browser)
            sublime.set_timeout(
                lambda: bin_.start(args=['http://localhost:8080']), 1000)
            return

        elif sublime.platform() == 'windows':
            # FIXME(guillermooo): On Windows, Firefox won't work when started
            # from the cmdline only. If it's started first from the shell, it
            # will work here as well.
            path = sdk.path_to_default_user_browser
            bin_ = GenericBinary(path)
            sublime.set_timeout(lambda: bin_.start(
                                   args=['http://localhost:8080'],
                                   shell=True,
                                   cwd=os.path.dirname(path)),
                                1000)
            return

        TypeError('not implemented for linux')

    def run_server_app(self, file_name, working_dir):
        self.execute(
            cmd=[SDK().path_to_dart, '--checked', file_name],
            working_dir=working_dir,
            file_regex="'file:///(.+)': error: line (\\d+) pos (\\d+): (.*)$",
            preamble='Running dart...\n',
            )

    def run_web_app(self, file_name, working_dir, action):

        if self.server:
            self.execute(kill=True)
        self.server = True

        sdk = SDK()

        if action == 'secondary':
            if not sdk.path_to_default_user_browser:
                print("Dart: No default browser found")
                _logger.info('no default browser found')
                return

            self.execute(
                cmd=[sdk.path_to_pub, 'serve'],
                working_dir=working_dir,
                )
            self.start_default_browser()
            return

        self.execute(
            cmd=[sdk.path_to_pub, 'serve', '--no-dart2js'],
            working_dir=working_dir,
            )

        # TODO(guillermooo): run dartium in checked mode
        sublime.set_timeout(lambda: Dartium().start('http://localhost:8080'),
                            1000)


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
