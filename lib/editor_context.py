# Copyright (c) 2014, Guillermo López-Anglada. Please see the AUTHORS file for details.
# All rights reserved. Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.)

'''Holds state about the editor.
'''

import threading

from Dart.sublime_plugin_lib.panels import OutputPanel


class EditorContext(object):
    write_lock = threading.Lock()
    search_id_lock = threading.Lock()

    # FIXME(guillermooo): This is utterly wrong. This needs to be a singleton.
    def __init__(self):
        self._search_id = None
        self.results_panel = None
        self._navigation = None
        self._errors = []
        self._errors_index = -1

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

    @property
    def navigation(self):
        with EditorContext.write_lock:
            return self._navigation

    @navigation.setter
    def navigation(self, value):
        # TODO(guillermooo): store this data by file
        with EditorContext.write_lock:
            self._navigation = value

    @property
    def errors(self):
        with EditorContext.write_lock:
            return self._errors

    @errors.setter
    def errors(self, values):
        with EditorContext.write_lock:
            self._errors_index = -1
            self._errors = list(values)

    @property
    def errors_index(self):
        with EditorContext.write_lock:
            return self._errors_index

    def increment_error_index(self):
        with EditorContext.write_lock:
            if self._errors_index == len(self._errors) - 1:
                raise IndexError('end of errors list')
            self._errors_index += 1

    def decrement_error_index(self):
        with EditorContext.write_lock:
            if self._errors_index == 0:
                raise IndexError('start of errors list')
            self._errors_index -= 1

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
