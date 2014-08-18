'''Holds state about the editor.
'''

import threading

from Dart.lib.panels import OutputPanel


class EditorContext(object):
    search_id_lock = threading.Lock()

    def __init__(self):
        self._search_id = None
        self.results_panel = None

    @property
    def search_id(self):
        with EditorContext.search_id_lock:
            return self._search_id

    @search_id.setter
    def search_id(self, value):
        with EditorContext.search_id_lock:
            if self._search_id == value:
                return
            self.results_panel = OutputPanel('dart.search.results')
            self.results_panel.set('result_file_regex', r'^\w+\s+-\s+(.*?):(\d+):(\d+)')
            self._search_id = value

    @search_id.deleter
    def search_id(self):
        with EditorContext.search_id_lock:
            self._search_id = None

    def check_token(self, action, token):
        if action == 'search':
            if self.search_id is None:
                return
            return (token == self.search_id)

    def append_search_results(self, items):
        items = list(items)
        print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAA", list(items))
        with EditorContext.search_id_lock:
            print("UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU")
            if not self.results_panel:
                print("))))))))))))))))))))))))))))))))))))))))))")
                return

            for item in items:
                print("IIIIIIIIIIIIIIIII", item)
                self.results_panel.write(item.to_encoded_pos())

            self.results_panel.show()
