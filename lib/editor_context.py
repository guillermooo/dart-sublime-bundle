'''Holds state about the editor.
'''

import threading


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

