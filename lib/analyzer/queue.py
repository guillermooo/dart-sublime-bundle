# Copyright (c) 2014, Guillermo López-Anglada. Please see the AUTHORS file for details.
# All rights reserved. Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.)

import sublime

import queue
import json

import threading

from Dart import PluginLogger
from Dart.lib.path import is_active
from Dart.lib.path import is_active_path


_logger = PluginLogger(__name__)


class TaskPriority:
    HIGHEST = 0
    HIGHER = 100
    HIGH = 200
    DEFAULT = 300
    LOW = 400
    LOWER = 500
    LOWEST = 600


class AnalyzerQueue(queue.PriorityQueue):
    '''A priority queue for requests/responses from the analysis server.

    It automatically bumps up priority of requests/responses coming from or
    targeted at the current view.
    '''
    def __init__(self, name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
        self.lock_put = threading.Lock()
        self.lock_get = threading.Lock()

    def __str__(self):
        return "{} [{}]".format(self.__class__.__name__, self.name)

    def is_active(self, view_or_path):
        assert (isinstance(view_or_path, sublime.View) or
                isinstance(view_or_path, str)), "bad parameter"

        try:
            return is_active(view_or_path)
        except AttributeError:
            return is_active_path(view_or_path)

    def calculate_priority(self, view, given):
        '''Returns a priority based on @view and @given.

        If @view is a view and is the active view, @given is bumped. The same
        happens if @view is a path and is the path to the current view.

        @view
          Can be a view or a path.

        @given
          The given `TaskPriority`.
        '''
        if (not view) or (given == TaskPriority.HIGHEST):
            return given

        if self.is_active(view):
            return max((given - 50), TaskPriority.HIGHEST)

    def put(self, data, priority=TaskPriority.DEFAULT, view=None, block=True,
            timeout=None):
                with self.lock_put:
                    _logger.debug("putting in %s: %s", self.name, repr(data))
                    priority = self.calculate_priority(view, priority)
                    super().put((priority, json.dumps(data)), block, timeout)

    def get(self, block=True, timeout=None):
        with self.lock_get:
            prio, data = super().get(block, timeout)
            _logger.debug("getting in %s: %s", self.name, repr(data))
            return json.loads(data)
