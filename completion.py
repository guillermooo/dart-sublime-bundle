import re

import sublime
import sublime_plugin

from Dart import analyzer
from Dart import editor_context


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
