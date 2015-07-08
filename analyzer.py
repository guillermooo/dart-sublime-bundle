# Copyright (c) 2014, Guillermo López-Anglada. Please see the AUTHORS file for details.
# All rights reserved. Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.)

import os
import threading
import time

from collections import defaultdict

import sublime
import sublime_plugin

from Dart.sublime_plugin_lib import PluginLogger
from Dart.sublime_plugin_lib.path import is_active
from Dart.sublime_plugin_lib.sublime import after

from Dart.lib.analyzer.analyzer import AnalysisServer
from Dart.lib.error import ConfigError
from Dart.lib.path import is_view_dart_script
from Dart.lib.path import only_for_dart_files
from Dart.lib.sdk import SDK


_logger = PluginLogger(__name__)


g_server = None


def init():
    global g_server
    _logger.debug('starting dart analyzer')

    try:
        g_server = AnalysisServer()
        threading.Thread(target=g_server.start).run()
    except Exception as e:
        print('Dart: Exception occurred during init. Aborting')
        print('==============================================')
        print(e)
        print('==============================================')
        return

    print('Dart: Analyzer started.')


def plugin_loaded():
    sdk = SDK()

    if not sdk.enable_analysis_server:
        return
    try:
        sdk.check_for_critical_configuration_errors()
    except ConfigError as e:
        print("Dart: " + str(e))
        _logger.error(e)
        return

    # FIXME(guillermooo): Ignoring, then de-ignoring this package throws
    # errors. (Potential ST3 bug: https://github.com/SublimeTextIssues/Core/issues/386)
    # Make ST more responsive on startup.
    sublime.set_timeout(init, 500)


def plugin_unloaded():
    # The worker threads handling requests/responses block when reading their
    # queue, so give them something.
    # XXX: This handler loads at times I wouldn't expect it to and ends up
    # killing the plugin. Disable this for now.
    # g_server.stop()
    pass


class ActivityTracker(sublime_plugin.EventListener):
    """
    After ST has been idle for an interval, sends requests to the analyzer
    if the buffer has been saved or is dirty.
    """

    edits = defaultdict(lambda: 0)
    edits_lock = threading.RLock()

    def increment_edits(self, view):
        with ActivityTracker.edits_lock:
            ActivityTracker.edits[view.id()] += 1
        sublime.set_timeout(lambda: self.check_idle(view), 1200)

    def decrement_edits(self, view):
        with ActivityTracker.edits_lock:
            if ActivityTracker.edits[view.id()] > 0:
                ActivityTracker.edits[view.id()] -= 1

    @only_for_dart_files
    def on_load(self, view):
        with ActivityTracker.edits_lock:
            ActivityTracker.edits[view.id()] = 0

        if AnalysisServer.ping():
            g_server.send_remove_content(view)

    @only_for_dart_files
    def on_idle(self, view):
        if AnalysisServer.ping():
            if view.is_dirty() and is_active(view):
                _logger.debug('sending overlay data for %s', view.file_name())
                g_server.send_add_content(view)

    # TODO(guillermooo): Use on_modified_async
    @only_for_dart_files
    def on_modified(self, view):
        # if we've `revert`ed the buffer, it'll be clean
        if not view.is_dirty():
            self.on_load(view)
            return

        self.increment_edits(view)

    def check_idle(self, view):
        with ActivityTracker.edits_lock:
            self.decrement_edits(view)
            if self.edits[view.id()] == 0:
                self.on_idle(view)

    @only_for_dart_files
    def on_post_save(self, view):
        with ActivityTracker.edits_lock:
            # TODO(guillermooo): does .id() uniquely identify views
            # across windows?
            ActivityTracker.edits[view.id()] += 1
        sublime.set_timeout(lambda: self.check_idle(view), 1000)

        # The file has been saved, so force use of filesystem content.
        if AnalysisServer.ping():
            g_server.send_remove_content(view)

    @only_for_dart_files
    def on_deactivated(self, view):
        # FIXME: what's this supposed to do?
        if not is_view_dart_script(view):
            return

    @only_for_dart_files
    def on_activated(self, view):
        if AnalysisServer.ping() and not view.is_loading():
            g_server.add_root(view, view.file_name())

            if is_active(view):
                g_server.send_set_priority_files(view, [view.file_name()])

                if view.is_dirty():
                    g_server.send_add_content(view)
        else:
            after(250, self.on_activated, view)
