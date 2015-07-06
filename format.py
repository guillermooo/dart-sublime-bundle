# Copyright (c) 2014, Guillermo López-Anglada. Please see the AUTHORS file for details.
# All rights reserved. Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.)

from subprocess import PIPE
from subprocess import Popen

import sublime
import sublime_plugin

from Dart.sublime_plugin_lib import PluginLogger
from Dart.sublime_plugin_lib.plat import supress_window

from Dart import analyzer
from Dart.lib.sdk import DartFormat


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

        analyzer.g_server.send_format_file(view)


class DartReplaceRegion(sublime_plugin.TextCommand):
    def run(self, edit, region, text):
        reg = sublime.Region(*region)
        self.view.replace(edit, reg, text)
        self.view.run_command('reindent')
