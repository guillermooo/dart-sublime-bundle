'''Search commands.
'''

import sublime
import sublime_plugin

from Dart import PluginLogger
from Dart import analyzer


_logger = PluginLogger(__name__)


class DartFindTopLevelDeclsCommand(sublime_plugin.WindowCommand):
    '''Displays the top-level declarations.
    '''
    def run(self):
        if analyzer.g_server.ping():
            v = self.window.active_view()
            word = v.word(v.sel()[0].b)
            word = v.substr(word).strip()
            _logger.info("finding top level decls")
            analyzer.g_server.send_find_top_level_decls(v, word)
            return


class DartFindReferences(sublime_plugin.WindowCommand):
    '''Displays the references of the given element.
    '''
    def run(self):
        if analyzer.g_server.ping():
            v = self.window.active_view()
            _logger.info("finding element references")
            analyzer.g_server.send_find_element_refs(v)
            return
