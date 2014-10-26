# Copyright (c) 2014, Guillermo López-Anglada. Please see the AUTHORS file for details.
# All rights reserved. Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.)

import sublime
import sublime_plugin

import os
from subprocess import check_output

from Dart.lib.fs_completion import FileSystemCompletion
from Dart.lib.sublime import after
from Dart.lib.sdk import SDK
from Dart.lib.plat import supress_window
from Dart.lib.collections import CircularArray


class DartStagehandWizard(sublime_plugin.WindowCommand):
    options = [
        'consoleapp',
        'package',
        'polymerapp',
        'shelfapp',
        'webapp',
    ]

    def run(self):
        self.window.show_quick_panel(DartStagehandWizard.options,
                                     self.on_done)

    def on_done(self, i):
        if i == -1:
            return
        template = DartStagehandWizard.options[i]
        self.window.run_command('dart_stagehand', {'template': template})


class DartStagehand(sublime_plugin.WindowCommand):
    cancel_change_event = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, template=None):
        if not template:
            return
        self.template = template

        view = self.window.show_input_panel('', '',
                                            self.on_done,
                                            self.on_change,
                                            self.on_cancel)
        view.settings().set('gutter', False)
        view.settings().set('rulers', None)
        view.settings().set('is_vintageous_widget', True)
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
            self.template = None
            return

        self.generate(s, self.template)
        self.template = None

    def on_change(self, s):
        if DartStagehand.cancel_change_event:
            DartStagehand.cancel_change_event = False
            return
        DartCompleteFs.user_interaction = True

    def on_cancel(self):
        DartCompleteFs.cache = None
        DartCompleteFs.index = 0
        DartCompleteFs.user_interaction = False
        self.template = None

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
        sdk = SDK()
        self.window.run_command('dart_exec', {
            'cmd' : [sdk.path_to_pub, 'global', 'run',
                     'stagehand', '-o', path, template],
            'preamble': "Running stagehand...\n"
            })


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

    def run(self, edit):
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

        content = os.path.join(DartCompleteFs.locked_dir,
                               next(DartCompleteFs.cache))

        self.view.erase(edit, sublime.Region(0, self.view.size()))
        # Change event of input panel runs async, so make sure it knows this
        # time it was a non-interactive change.
        DartStagehand.cancel_change_event = True
        self.view.run_command('append', {'characters': content})

        self.view.sel().clear()
        self.view.sel().add(sublime.Region(self.view.size()))
