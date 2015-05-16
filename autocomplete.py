import re

import sublime
import sublime_plugin

from Dart import analyzer
from Dart import editor_context
from Dart.lib.path import is_view_dart_script


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
    _PROPERTY = '\u25CB {}'
    _FUNCTION = '\u25BA {}'

    def _format(self, completions):
        pass

    def on_query_completions(self, view, prefix, locations):
        if not is_view_dart_script(view):
            return ([], 0)

        completions = []
        with editor_context.autocomplete_context as actx:
            completions = actx.formatted_results
            actx.invalidate_results()

        if completions:
            return (completions, sublime.INHIBIT_WORD_COMPLETIONS | sublime.INHIBIT_EXPLICIT_COMPLETIONS)

        return ([], 0)
