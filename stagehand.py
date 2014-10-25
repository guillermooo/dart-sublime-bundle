# Copyright (c) 2014, Guillermo López-Anglada. Please see the AUTHORS file for details.
# All rights reserved. Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.)

import sublime
import sublime_plugin

import os

from Dart.lib.fs_completion import FileSystemCompletion
from Dart.lib.sublime import after



class DartStagehand(sublime_plugin.WindowCommand):
    cancel_change_event = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self):
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

    def on_change(self, s):
        if DartStagehand.cancel_change_event:
            DartStagehand.cancel_change_event = False
            return
        DartCompleteFs.user_interaction = True

    def on_cancel(self):
        DartCompleteFs.cache = None
        DartCompleteFs.index = 0
        DartCompleteFs.user_interaction = False


class CircularArray(object):
    def __init__(self, items):
        self._index = -1
        self._items = items

    def __iter__(self):
        return self

    def __next__(self):
        self._index += 1
        if self._index >= len(self._items):
            self._index = 0
        return self._items[self._index]

    def __len__(self):
        return len(self._items)


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
