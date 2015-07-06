import re

import sublime
import sublime_plugin

from Dart.sublime_plugin_lib import PluginLogger
from Dart.sublime_plugin_lib.events import IdleIntervalEventListener
from Dart.sublime_plugin_lib.path import is_active

from Dart import analyzer
from Dart._init_ import editor_context
from Dart.analyzer import AnalysisServer
from Dart.lib.path import is_view_dart_script
from Dart.lib.pub_package import DartFile


_logger = PluginLogger(__name__)


class IdleAutocomplete(IdleIntervalEventListener):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.duration = 300

    def check(self, view):
        # Offer Dart completions in Dart files when the caret isn't in a
        # string or comment. If strings or comments, offer plain Sublime Text
        # completions.
        return (not self._in_string_or_comment(view)
                and DartFile(view).is_dart_file)

    def on_idle(self, view):
        self._show_completions(view)

    def _show_completions(self, view):
        try:
            # TODO: We probably should show completions after other chars.
            is_after_dot = view.substr(view.sel()[0].b - 1) == '.'
        except IndexError:
            return

        if not is_after_dot:
            return

        if not AnalysisServer.ping():
            return

        if view.is_dirty() and is_active(view):
            _logger.debug('sending overlay data for %s', view.file_name())
            analyzer.g_server.send_add_content(view)

        if is_active(view):
            view.window().run_command('dart_get_completions')

    def _in_string_or_comment(self, view):
        try:
            return view.match_selector(view.sel()[0].b,
                    'source.dart string, source.dart comment')
        except IndexError:
            pass


class DartGetCompletions(sublime_plugin.WindowCommand):
    def run(self):
        view = self.window.active_view()
        if not view:
            return

        fname = view.file_name()
        if not fname:
            return

        # TODO(guillermooo): only retrieve completions for empty selections.
        offset = view.sel()[0].end()
        analyzer.g_server.send_get_suggestions(view, fname, offset)


class AutocompleteEventListener(sublime_plugin.EventListener):
    _INHIBIT_OTHER = (sublime.INHIBIT_WORD_COMPLETIONS |
            sublime.INHIBIT_EXPLICIT_COMPLETIONS)

    @staticmethod
    def _in_string_or_comment(view, locations):
        return all((view.match_selector(loc, 'source.dart comment, source.dart string')
            or view.match_selector(loc - 1, 'source.dart comment, sorce.dart string'))
                for loc in locations)

    def on_query_completions(self, view, prefix, locations):
        if not is_view_dart_script(view):
            return ([], 0)

        if view.settings().get('command_mode') is True:
            return ([], self._INHIBIT_OTHER)

        if self._in_string_or_comment(view, locations):
            return ([], 0)

        completions = []
        with editor_context.autocomplete_context as actx:
            completions = actx.formatted_results
            actx.invalidate_results()

        if completions:
            return (completions, self._INHIBIT_OTHER)

        return ([], self._INHIBIT_OTHER)
