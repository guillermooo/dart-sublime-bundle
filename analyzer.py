# Copyright (c) 2014, Guillermo López-Anglada. Please see the AUTHORS file for details.
# All rights reserved. Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.)

from collections import defaultdict
from datetime import datetime
from subprocess import PIPE
from subprocess import Popen
import json
import os
import queue
import threading
import time

import sublime
import sublime_plugin

from Dart.sublime_plugin_lib import PluginLogger
from Dart.sublime_plugin_lib.panels import OutputPanel
from Dart.sublime_plugin_lib.path import is_active
from Dart.sublime_plugin_lib.plat import supress_window
from Dart.sublime_plugin_lib.sublime import after
from Dart.sublime_plugin_lib.sublime import get_active_view

from Dart._init_ import editor_context
from Dart.lib.analyzer import actions
from Dart.lib.analyzer import requests
from Dart.lib.analyzer.api.base import Notification
from Dart.lib.analyzer.api.base import Response
from Dart.lib.analyzer.api.protocol import AddContentOverlay
from Dart.lib.analyzer.api.protocol import AnalysisErrorsParams
from Dart.lib.analyzer.api.protocol import AnalysisNavigationParams
from Dart.lib.analyzer.api.protocol import AnalysisService
from Dart.lib.analyzer.api.protocol import AnalysisSetAnalysisRootsParams
from Dart.lib.analyzer.api.protocol import AnalysisSetAnalysisRootsResult
from Dart.lib.analyzer.api.protocol import AnalysisSetPriorityFilesParams
from Dart.lib.analyzer.api.protocol import AnalysisSetPriorityFilesResult
from Dart.lib.analyzer.api.protocol import AnalysisSetSubscriptionsParams
from Dart.lib.analyzer.api.protocol import ServerSetSubscriptionsResult
from Dart.lib.analyzer.api.protocol import AnalysisUpdateContentParams
from Dart.lib.analyzer.api.protocol import AnalysisUpdateContentResult
from Dart.lib.analyzer.api.protocol import CompletionGetSuggestionsParams
from Dart.lib.analyzer.api.protocol import CompletionGetSuggestionsResult
from Dart.lib.analyzer.api.protocol import CompletionResultsParams
from Dart.lib.analyzer.api.protocol import EditFormatParams
from Dart.lib.analyzer.api.protocol import EditFormatResult
from Dart.lib.analyzer.api.protocol import RemoveContentOverlay
from Dart.lib.analyzer.api.protocol import ServerGetVersionParams
from Dart.lib.analyzer.api.protocol import ServerGetVersionResult
from Dart.lib.analyzer.pipe_server import PipeServer
from Dart.lib.analyzer.queue import AnalyzerQueue
from Dart.lib.analyzer.queue import RequestsQueue
from Dart.lib.analyzer.queue import TaskPriority
from Dart.lib.analyzer.response import ResponseMaker
from Dart.lib.dart_project import DartProject
from Dart.lib.editor_context import EditorContext
from Dart.lib.error import ConfigError
from Dart.lib.path import find_pubspec_path
from Dart.lib.path import is_path_under
from Dart.lib.path import is_view_dart_script
from Dart.lib.path import only_for_dart_files
from Dart.lib.sdk import SDK


_logger = PluginLogger(__name__)


START_DELAY = 50
_SIGNAL_STOP = '__SIGNAL_STOP'


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
    sublime.set_timeout(init, START_DELAY)


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
        # Any ongoing searches must be invalidated.
        del editor_context.search_id

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


class StdoutWatcher(threading.Thread):
    def __init__(self, server, path):
        super().__init__()
        self.path = path
        self.server = server
        self.name = 'StdoutWatcher-thread'

    def start(self):
        _logger.info("starting StdoutWatcher")

        while True:
            try:
                data = self.server.stdout.readline().decode('utf-8')
            except Exception as e:
                msg = 'error in thread' + self.name + '\n'
                msg += str(e)
                _logger.error(msg)
                continue

            _logger.debug('data read from server: %s', repr(data))

            if not data:
                if self.server.stdin.closed:
                    _logger.info(
                        'StdoutWatcher is exiting by internal request')
                    return

                _logger.debug("StdoutWatcher - no data")
                return

            decoded = json.loads(data)
            # TODO(guillermooo): Some notifications need to have a HIGHEST
            # prio. For example, if we're getting a new search id.
            self.server.responses.put(decoded, view=decoded.get('file'),
                block=False)
        _logger.error('StdoutWatcher exited unexpectedly')


class AnalysisServer(object):
    MAX_ID = 9999999

    _request_id_lock = threading.Lock()
    _op_lock = threading.Lock()
    _write_lock = threading.Lock()

    _request_id = -1

    server = None

    @property
    def stdout(self):
        return AnalysisServer.server.proc.stdout

    @property
    def stdin(self):
        return AnalysisServer.server.proc.stdin

    @staticmethod
    def get_request_id(view, response_type):
        with AnalysisServer._request_id_lock:
            if AnalysisServer._request_id >= AnalysisServer.MAX_ID:
                AnalysisServer._request_id = -1
            AnalysisServer._request_id += 1
            editor_context.request_ids[view.id()][str(AnalysisServer._request_id)] = response_type
            return str(AnalysisServer._request_id)

    @staticmethod
    def ping():
        try:
            return AnalysisServer.server.is_running
        except AttributeError:
            return

    def __init__(self):
        self.roots = []
        self.priority_files = []
        self.requests = RequestsQueue('requests')
        self.responses = AnalyzerQueue('responses')


    def start_handlers(self):
        reqh = RequestHandler(self)
        reqh.daemon = True
        reqh.start()

        resh = ResponseHandler(self)
        resh.daemon = True
        resh.start()

    @property
    def proc(self):
        return AnalysisServer.server

    def add_root(self, view, path):
        """
        Adds `path` to the monitored roots if it is unknown.

        If a `pubspec.yaml` is found in the path, its parent is monitored.
        Otherwise the passed-in directory name is monitored.

        @path
          Can be a directory or a file path.
        """

        if not path:
            _logger.debug('not a valid path: %s', path)
            return

        new_root_path = find_pubspec_path(path)
        if not new_root_path:
            # It seems we're not in a pub package, so we're probably looking
            # at a loose .dart file.
            new_root_path = os.path.dirname(path)
            _logger.debug('did not find pubspec.yaml in path: %s', path)
            _logger.debug('set root to: %s', new_root_path)

        with AnalysisServer._op_lock:
            if new_root_path not in self.roots:
                _logger.debug('adding new root: %s', new_root_path)
                self.roots.append(new_root_path)
                self.send_set_roots(view, self.roots)
                return

        _logger.debug('root already known: %s', new_root_path)

    def start(self):
        if AnalysisServer.ping():
            return

        self.send_get_version(get_active_view())

        sdk = SDK()

        _logger.info('starting AnalysisServer')

        AnalysisServer.server = PipeServer([sdk.path_to_dart,
                            sdk.path_to_analysis_snapshot,
                           '--sdk={0}'.format(sdk.path)])

        def do_start():
            try:
                AnalysisServer.server.start(working_dir=sdk.path)
                self.start_handlers()
                self.start_stdout_watcher()
            except Exception as e:
                _logger.error('could not start server properly')
                _logger.error(e)
                return

        threading.Thread(target=do_start).start()

    def start_stdout_watcher(self):
        sdk = SDK()
        t = StdoutWatcher(self, sdk.path)
        # Thread dies with the main thread.
        t.daemon = True
        t.start()

    def stop(self):
        req = requests.shut_down(str(AnalysisServer.MAX_ID + 100))
        self.requests.put(req, priority=TaskPriority.HIGHEST, block=False)
        self.requests.put({'_internal': _SIGNAL_STOP}, block=False)
        self.responses.put({'_internal': _SIGNAL_STOP}, block=False)
        # self.server.stop()

    def write(self, data):
        with AnalysisServer._write_lock:
            data = (json.dumps(data) + '\n').encode('utf-8')
            _logger.debug('writing to stdin: %s', data)
            self.stdin.write(data)
            self.stdin.flush()

    def send_set_roots(self, view, included=[], excluded=[]):
        included = [f for f in included if not self.should_ignore_file(f)]

        if not (included or excluded):
            return

        req = AnalysisSetAnalysisRootsParams(included, excluded)
        _logger.info('sending set_roots request')
        self.requests.put(req.to_request(self.get_request_id(view,
                AnalysisSetAnalysisRootsResult)), block=False)

    def send_get_version(self, view):
        req = ServerGetVersionParams().to_request(
                self.get_request_id(view, ServerGetVersionResult))
        _logger.info('sending get version request')
        self.requests.put(req, block=False)

    def send_add_content(self, view):
        if self.should_ignore_file(view.file_name()):
            return

        content = view.substr(sublime.Region(0, view.size()))
        req = AnalysisUpdateContentParams({view.file_name(): AddContentOverlay(content)})
        _logger.info('sending update content request - add')
        # track this type of req as it may expire
        # TODO: when this file is saved, we must remove the overlays.
        self.requests.put(req.to_request(self.get_request_id(view, AnalysisUpdateContentResult)),
                          view=view,
                          priority=TaskPriority.HIGH,
                          block=False)

    def send_remove_content(self, view):
        if self.should_ignore_file(view.file_name()):
            return

        req = AnalysisUpdateContentParams({view.file_name(): RemoveContentOverlay()})
        _logger.info('sending update content request - delete')
        self.requests.put(req.to_request(self.get_request_id(view, AnalysisUpdateContentResult)),
                view=view,
                priority=TaskPriority.HIGH,
                block=False)

    def send_set_priority_files(self, view, files):
        if files == self.priority_files:
            return

        definite_files = [f for f in files if not self.should_ignore_file(f)]
        if not definite_files:
            return

        req = AnalysisSetPriorityFilesParams(definite_files)
        self.requests.put(req.to_request(self.get_request_id(view, AnalysisSetPriorityFilesResult)),
                priority=TaskPriority.HIGH, block=False)

        req2 = AnalysisSetSubscriptionsParams({AnalysisService.NAVIGATION: definite_files})
        self.requests.put(req2.to_request(self.get_request_id(view,
                ServerSetSubscriptionsResult)),
                priority=TaskPriority.HIGH,
                block=False)

    def send_get_suggestions(self, view, file, offset):
        new_id = self.get_request_id(view, CompletionGetSuggestionsResult)

        with editor_context.autocomplete_context as actx:
            actx.invalidate()
            actx.request_id = new_id

        req = CompletionGetSuggestionsParams(file, offset)
        req = req.to_request(new_id)

        self.requests.put(req, priority=TaskPriority.HIGH, block=False)

    def send_format_file(self, view):
        new_id = self.get_request_id(view, EditFormatResult)

        if not view.file_name():
            _logger.info("aborting sending request for formatting - no file name")
            return

        r0 = None
        try:
            r0 = view.sel()[0]
        except IndexError:
            r0 = sublime.Region(0)

        # TODO: Implement lineLength parameter.
        req = EditFormatParams(view.file_name(), r0.begin(), r0.size())
        req = req.to_request(new_id)

        _logger.info("now sending request for formatting")
        self.requests.put(req, priority=TaskPriority.HIGH, block=False)

    def should_ignore_file(self, path):
        project = DartProject.from_path(path)
        is_a_third_party_file = (project and is_path_under(project.path_to_packages, path))

        if is_a_third_party_file:
            return True

        sdk = SDK()
        return is_path_under(sdk.path, path)


class ResponseHandler(threading.Thread):
    """ Handles responses from the response queue.
    """
    def __init__(self, server):
        super().__init__()
        self.server = server
        self.name = 'ResponseHandler-thread'

    def run(self):
        _logger.info('starting ResponseHandler')

        response_maker = ResponseMaker(self.server.responses)

        try:
            for resp in response_maker.make():

                if resp is None:
                    continue

                if isinstance(resp, dict):
                    if resp.get('_internal') == _SIGNAL_STOP:
                        _logger.info('ResponseHandler exiting by internal request.')
                        return

                if isinstance(resp, Notification):
                    if isinstance(resp.params, AnalysisErrorsParams):
                        # Make sure the right type is passed to the async
                        # code. `resp` may point to a different object when
                        # the async code finally has a chance to run.
                        after(0, actions.show_errors,
                              AnalysisErrorsParams.from_json(resp.params.to_json().copy())
                              )
                        continue

                    if isinstance(resp.params, AnalysisNavigationParams):
                        after(0, actions.handle_navigation_data,
                              AnalysisNavigationParams.from_json(resp.params.to_json().copy())
                              )
                        continue

                    if isinstance(resp.params, CompletionResultsParams):
                        with editor_context.autocomplete_context as actx:
                            if actx.request_id or (resp.params.id != actx.id):
                                actx.invalidate_results()
                                continue
                        after(0, actions.handle_completions,
                              CompletionResultsParams.from_json(resp.params.to_json().copy())
                              )

                if isinstance(resp, Response):
                    if isinstance(resp.result, ServerGetVersionResult):
                        print('Dart: Analysis Server version:', resp.result.version)
                        continue

                    if isinstance(resp.result, CompletionGetSuggestionsResult):
                        with editor_context.autocomplete_context as actx:
                            if resp.id != actx.request_id:
                                continue

                            actx.id = resp.result.id
                            actx.request_id = None

                    if isinstance(resp.result, EditFormatResult):
                        after(0, actions.handle_formatting, EditFormatResult.from_json(resp.result.to_json().copy()))
                        continue

        except Exception as e:
            msg = 'error in thread' + self.name + '\n'
            msg += str(e)
            _logger.error(msg)


class RequestHandler(threading.Thread):
    """ Watches the requests queue and forwards them to the pipe server.
    """
    def __init__(self, server):
        super().__init__()
        self.server = server
        self.name = 'RequestHandler-thread'

    def run(self):
        _logger.info('starting RequestHandler')

        while True:
            try:
                item = self.server.requests.get(timeout=0.1)

                if item.get('_internal') == _SIGNAL_STOP:
                    _logger.info(
                        'RequestHandler is exiting by internal request')
                    return

                self.server.write(item)
            except queue.Empty:
                pass
            except Exception as e:
                msg = 'error in thread ' + self.name + '\n'
                msg += str(e)
                _logger.error(msg)
