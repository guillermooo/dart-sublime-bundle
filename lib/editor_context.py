# Copyright (c) 2014, Guillermo López-Anglada. Please see the AUTHORS file for details.
# All rights reserved. Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.)

'''
Holds state about the editor.
'''

from collections import defaultdict
import threading

from Dart.sublime_plugin_lib.panels import OutputPanel
from Dart.lib.autocomplete import AutocompleteContext


class EditorContext(object):
    write_lock = threading.Lock()

    # FIXME(guillermooo): This is utterly wrong. This needs to be a singleton.
    def __init__(self):
        self.results_panel = None
        self._navigation = None
        self._errors = []
        self._errors_index = -1
        self.autocomplete_context = AutocompleteContext()
        # Maps view.id's request id's, and these to response types.
        self.request_ids = defaultdict(dict)

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

    def get_current_error(self):
        return self.errors[self.errors_index]
