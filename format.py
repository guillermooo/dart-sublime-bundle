# Copyright (c) 2014, Guillermo López-Anglada. Please see the AUTHORS file for details.
# All rights reserved. Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.)

import sublime
import sublime_plugin

from Dart import PluginLogger
from Dart.lib.plat import supress_window
from Dart.lib.sdk import DartFormat

from subprocess import PIPE
from subprocess import Popen

_logger = PluginLogger(__name__)


class DartFormatCommand(sublime_plugin.WindowCommand):
    '''Formats the selected text in Sublime Text using `dartfmt`.

    Notes:
    - Can be used as a build system.
    '''
    def run(self, **kwargs):
        view = self.window.active_view()
        if not view:
            return

        # Reformat the whole file.
        text = view.substr(sublime.Region(0, view.size()))
        formatted_text = DartFormat().format(text)

        if not formatted_text:
            sublime.status_message("Dart: Could not format anything.")
            return

        view.run_command('dart_replace_region', {
            'region': [0, view.size()],
            'text': formatted_text + '\n'
            })


class DartReplaceRegion(sublime_plugin.TextCommand):
    def run(self, edit, region, text):
        reg = sublime.Region(*region)
        self.view.replace(edit, reg, text)
        self.view.run_command('reindent')
