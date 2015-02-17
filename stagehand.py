# Copyright (c) 2014, Guillermo López-Anglada. Please see the AUTHORS file for details.
# All rights reserved. Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.)

import sublime
import sublime_plugin

from subprocess import CalledProcessError
from subprocess import check_output
from subprocess import Popen
import glob
import json
import os
import sys

from Dart.lib.sdk import SDK
from Dart.sublime_plugin_lib import PluginLogger
from Dart.sublime_plugin_lib.collections import CircularArray
from Dart.sublime_plugin_lib.fs_completion import FileSystemCompletion
from Dart.sublime_plugin_lib.panels import ErrorPanel
from Dart.sublime_plugin_lib.path import join_on_win
from Dart.sublime_plugin_lib.path import pushd
from Dart.sublime_plugin_lib.plat import supress_window
from Dart.sublime_plugin_lib.sublime import after



_logger = PluginLogger(__name__)


class DartStagehandWizard(sublime_plugin.WindowCommand):

    def run(self):
        # We assume that stagehand won't be updated frequently during a single
        # ST session. If it is, though, the user will need to restart ST in
        # order to see potential new templates.
        if not hasattr(self, 'options'):
            self.options = self.get_templates()
        if not self.options:
            return
        self.window.show_quick_panel(self.options,
                                     self.on_done)

    def on_done(self, i):
        if i == -1:
            return
        template = self.options[i][0]
        self.window.run_command('dart_stagehand', {'template': template})

    def get_templates(self):
        sdk = SDK()

        try:
            out = check_output([sdk.path_to_pub, 'global', 'run', 'stagehand', '--machine'],
                    startupinfo=supress_window()).decode('utf-8')
        except CalledProcessError as e:
            error_panel = ErrorPanel()
            error_panel.write('\n')
            error_panel.write('Could not run Stagehand.\n')
            error_panel.write('\n')
            error_panel.write('Stagehand is a tool to help you get started with new projects.\n')
            error_panel.write('\n')
            error_panel.write('To enable Stagehand, run the following command from a terminal:\n')
            error_panel.write('\n')
            error_panel.write('$ pub global activate stagehand')
            error_panel.show()
            msg = 'Could not run stagehand:\n {0}'.format(str(e))
            _logger.debug(msg)
            return None

        decoded = json.loads(out)
        entries = []
        for tpl in decoded:
            entry = [tpl['name'], tpl['description'],
                     "entrypoint: {}".format(tpl['entrypoint'])]
            entries.append(entry)
        return entries


class DartStagehand(sublime_plugin.WindowCommand):
    cancel_change_event = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, template=None):
        if not template:
            return
        self.template = template

        view = self.window.show_input_panel('Please select a directory:', '',
                                            self.on_done,
                                            self.on_change,
                                            self.on_cancel)
        view.settings().set('gutter', False)
        view.settings().set('rulers', None)
        view.settings().set('is_plugin_widget', True)
        view.set_syntax_file('Packages/Dart/Support/Dart (File System Navigation).hidden-tmLanguage')

        path = os.path.expanduser('~')
        v = self.window.active_view()
        if v and v.file_name():
            path = os.path.dirname(v.file_name())

        view.run_command('append', {'characters': path + '/'})

        view.sel().clear()
        view.sel().add(sublime.Region(view.size()))

        DartCompleteFs.user_interaction = False

    def on_done(self, s):
        DartCompleteFs.cache = None
        DartCompleteFs.index = 0
        DartCompleteFs.user_interaction = False

        if not self.check_installed():
            self.install()
            del self.template
            return

        self.generate(s, self.template)
        del self.template

    def on_change(self, s):
        if DartStagehand.cancel_change_event:
            DartStagehand.cancel_change_event = False
            return
        DartCompleteFs.user_interaction = True

    def on_cancel(self):
        DartCompleteFs.cache = None
        DartCompleteFs.index = 0
        DartCompleteFs.user_interaction = False
        del self.template

    def check_installed(self):
        sdk = SDK()
        out = check_output([sdk.path_to_pub, 'global', 'list'],
                           startupinfo=supress_window())
        return 'stagehand' in out.decode('utf-8')

    def install(self):
        sdk = SDK()
        self.window.run_command('dart_exec', {
            'cmd' :[sdk.path_to_pub, 'global', 'activate', 'stagehand'],
            'preamble': "Installing stagehand... (This may take a few seconds.)\n"
            })

    def generate(self, path=None, template=None):
        assert path and template, 'wrong call'

        try:
            if not os.path.exists(path):
                os.mkdir(path)
        except OSError as e:
            _logger.error(e)
            sublime.status_message('Dart: Error. Check console for details.')
            return

        with pushd(path):
            was_empty_dir = len(glob.glob("*")) == 0
            sdk = SDK()
            self.window.run_command('dart_exec', {
                'cmd': [sdk.path_to_pub, 'global', 'run',
                        'stagehand', template],
                'preamble': "Running stagehand...\n",
                'working_dir': path,
                })

            if was_empty_dir:
                after(2000, self.create_sublime_project, path)

    def create_sublime_project(self, path):
        parent, leaf = os.path.split(path)

        data = {
            'folders': [{
                'follow_symlinks': True,
                'path': '.'
            }]
        }

        proj_file = os.path.join(path, leaf + '.sublime-project')
        with open(proj_file, 'wt') as f:
            f.write(json.dumps(data))

        try:
            Popen([sublime.executable_path(), proj_file],
                  startupinfo=supress_window())
        except Exception as e:
            _logger.debug('could not open new project with subl[.exe]')
            _logger.debug(e)


class DartCompleteFs(sublime_plugin.TextCommand):
    cache = None
    index = 0
    user_interaction = False
    fs_completer = None
    locked_dir = ''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        DartCompleteFs.fs_completer = FileSystemCompletion(
                                casesensitive=(sublime.platform() == 'linux'))

    def run(self, edit, reverse=False):
        path = self.view.substr(sublime.Region(0, self.view.size()))

        if not DartCompleteFs.cache or DartCompleteFs.user_interaction:
            DartCompleteFs.user_interaction = False
            DartCompleteFs.index = 0
            DartCompleteFs.locked_dir = os.path.dirname(path)

            items = DartCompleteFs.fs_completer.get_completions(
                                                           path,
                                                           force_refresh=True)

            DartCompleteFs.cache = CircularArray(items)

        if len(DartCompleteFs.cache) == 0:
            DartCompleteFs.index = 0
            return

        item = DartCompleteFs.cache.forward() if not reverse \
                                              else DartCompleteFs.cache.backward()
        content = os.path.join(DartCompleteFs.locked_dir, item)

        self.view.erase(edit, sublime.Region(0, self.view.size()))
        # Change event of input panel runs async, so make sure it knows this
        # time it was a non-interactive change.
        DartStagehand.cancel_change_event = True
        self.view.run_command('append', {'characters': content})

        self.view.sel().clear()
        self.view.sel().add(sublime.Region(self.view.size()))
