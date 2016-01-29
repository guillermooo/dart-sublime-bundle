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
from Dart.lib.path import is_view_dart_script
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


class DartFormatOnSave(sublime_plugin.EventListener):
    """Keeps tabs on the views currently being edited and formats them on save
    if so configured.
    """
    def on_pre_save(self, view):
        if not is_view_dart_script(view):
            _logger.debug("not a dart file: %s", view.file_name())
            return

        settings = sublime.load_settings('Dart - Plugin Settings.sublime-settings')
        dartfmt_on_save = settings.get('dartfmt_on_save')
        if not dartfmt_on_save:
            _logger.debug("dartfmt is disabled (dartfmt_on_save is false)")
            return

        print("Dart format: Running dartfmt on ", view.file_name())
        # Format the whole view using the dartfmt command, rather than the
        # analyzer, since we need it to happen synchronously. Otherwise, the
        # formatting would happen after the save, leaving a dirty view.
        text = view.substr(sublime.Region(0, view.size()))
        formatted_text = DartFormat().format(text)
        view.run_command('dart_replace_region', {
            'region': [0, view.size()],
            'text': formatted_text + '\n'
            })
