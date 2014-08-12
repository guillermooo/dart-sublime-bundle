'''Search commands.
'''

import sublime
import sublime_plugin

from . import analyzer


class DartFindTopLevelDeclsCommand(sublime_plugin.WindowCommand):
    '''Displays the top-level declarations.
    '''
    def run(self):
        with analyzer.g_server_ready:
            if analyzer.g_server:
                v = self.window.active_view()
                word = v.word(v.sel()[0].b)
                word = v.substr(word).strip()
                print("xxx", "finding top level decls")
                analyzer.g_server.send_find_top_level_decls(word)
                return

        print("AAAA", "server not ready")
