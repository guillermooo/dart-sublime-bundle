import re

import sublime
import sublime_plugin

from Dart.sublime_plugin_lib import PluginLogger
from Dart.sublime_plugin_lib.events import IdleIntervalEventListener
from Dart.sublime_plugin_lib.path import is_active


from Dart import analyzer
from Dart.analyzer import AnalysisServer
from Dart import editor_context
from Dart.lib.path import is_view_dart_script


_logger = PluginLogger(__name__)


class IdleAutocomplete(IdleIntervalEventListener):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.duration = 400

    def check(self, view):
        return True

    def on_idle(self, view):
        prev_char = view.substr(view.sel()[0].begin() - 1)
        if not prev_char in '.':
            return

        if not AnalysisServer.ping():
            return

        if view.is_dirty() and is_active(view):
            _logger.debug('sending overlay data for %s', view.file_name())
            analyzer.g_server.send_add_content(view)

        if is_active(view):
            view.window().run_command('dart_get_completions')


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
    _INHIBIT_OTHER = (sublime.INHIBIT_WORD_COMPLETIONS |
            sublime.INHIBIT_EXPLICIT_COMPLETIONS)

    def _format(self, completions):
        pass

    def on_query_completions(self, view, prefix, locations):
        if not is_view_dart_script(view):
            return ([], 0)

        if view.settings().get('command_mode') is True:
            return ([], 0)

        completions = []
        with editor_context.autocomplete_context as actx:
            completions = actx.formatted_results
            actx.invalidate_results()

        if completions:
            return (completions, self._INHIBIT_OTHER)

        return ([], 0)
