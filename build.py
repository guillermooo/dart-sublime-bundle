'''Builds Dart projects intelligently.
'''

import sublime
import sublime_plugin

import os
from functools import partial

from Dart import PluginLogger
from Dart.lib.sdk import SDK
from Dart.lib.dart_project import ViewInspector
from Dart.lib.dart_project import find_pubspec


_logger = PluginLogger(__name__)


class ContextProvider(sublime_plugin.EventListener):
    '''Implements the 'dart_is_project_file' context for .sublime-keymap
    files.
    '''
    def on_query_context(self, view, key, operator, operand, match_all):
        if key == 'dart_is_project_file':
            return ViewInspector(view).is_project_file


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
        if ViewInspector(view).is_pubspec:
            self.window.run_command('dart_build_pubspec', {
                'action': action,
                'file_name': view.file_name()
                })
            return

        self.window.run_command('dart_run', {
            'action': action,
            'file_name': view.file_name()
            })


class DartRunCommand(sublime_plugin.WindowCommand):
    '''Runs a file with the most appropriate action.
    '''
    def run(self, file_name, action='primary'):
        '''
        @action
          On of: primary, secondary
        '''
        working_dir = find_pubspec(file_name)
        if not working_dir:
            working_dir = os.path.dirname(file_name)

        sdk = SDK()

        if action == 'primary':
            # TODO(guillermooo): add regexes
            cmd = [sdk.path_to_dart2js,
                        '--minify', '-o', file_name + '.js',
                        file_name]
            self.execute(cmd, working_dir)
            return

        if action != 'secondary':
            _logger("unknown action: %s", action)
            return

        # TODO(guillermooo): add regexes
        cmd = [sdk.path_to_dart, '--checked', file_name]
        self.execute(cmd, working_dir)

    def execute(self, cmd, working_dir):
        self.window.run_command('exec', {
            'cmd': cmd,
            'working_dir': working_dir
            })


class DartBuildPubspecCommand(sublime_plugin.WindowCommand):
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
            cmd = [SDK().path_to_pub] + ['get']
            self.execute(cmd, working_dir)
            return

        if action != 'secondary':
            _logger.error('not implemented')
            return

        f = partial(self.on_done, file_name, working_dir)
        self.window.show_quick_panel(self.PUB_CMDS, f)

    def on_done(self, file_name, working_dir, idx):
        if idx == -1:
            return

        cmd = [SDK().path_to_pub] + [self.PUB_CMDS[idx]]
        working_dir = os.path.dirname(file_name)
        self.execute(cmd, working_dir)

    def execute(self, cmd, working_dir):
        self.window.run_command('exec', {
            'cmd': cmd,
            'working_dir': working_dir
            })
