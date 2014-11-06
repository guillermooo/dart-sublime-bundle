# Copyright (c) 2014, Guillermo López-Anglada. Please see the AUTHORS file for details.
# All rights reserved. Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.)

'''Holds state about the editor.
'''

import threading

from Dart.sublime_plugin_lib.panels import OutputPanel


class EditorContext(object):
    search_id_lock = threading.Lock()

    # FIXME(guillermooo): This is utterly wrong. This needs to be a singleton.
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
        with EditorContext.search_id_lock:
            if not self.results_panel:
                return

            for item in items:
                self.results_panel.write(item.to_encoded_pos())

            self.results_panel.show()
