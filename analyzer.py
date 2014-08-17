import sublime
import sublime_plugin

from collections import defaultdict
from datetime import datetime
from subprocess import PIPE
from subprocess import Popen
import json
import os
import queue
import threading
import time

from Dart import PluginLogger
from Dart.lib.editor_context import EditorContext
from Dart.lib.analyzer import actions
from Dart.lib.analyzer import requests
from Dart.lib.analyzer.pipe_server import PipeServer
from Dart.lib.analyzer.response import Response
from Dart.lib.analyzer.response import ResponseMaker
from Dart.lib.analyzer.response import ResponseType
from Dart.lib.path import find_pubspec_path
from Dart.lib.path import is_active
from Dart.lib.path import is_view_dart_script
from Dart.lib.plat import supress_window
from Dart.lib.sdk import SDK
from Dart.lib.analyzer.queue import AnalyzerQueue
from Dart.lib.analyzer.queue import TaskPriority
from Dart.lib.panels import OutputPanel


_logger = PluginLogger(__name__)


START_DELAY = 2500
_SIGNAL_STOP = '__SIGNAL_STOP'


g_server = None
g_editor_context = EditorContext()

# maps:
#   req_type => view_id
#   view_id => valid token for this type of request
# Abstract this out into a class that provides its own synchronization.
g_req_to_resp = {
    "search": {},
}


def init():
    global g_server
    global g_editor_context
    _logger.debug('starting dart analyzer')

    try:
        g_server = AnalysisServer()
        g_server.start()
    except Exception as e:
        print('Dart: Exception occurred during init. Aborting')
        print('==============================================')
        print(e.message)
        print('==============================================')
        return

    print('Dart: Analyzer started.')


def plugin_loaded():
    # FIXME(guillermooo): Ignoring, then de-ignoring this package throws
    # errors.
    # Make ST more responsive on startup --- also helps the logger get ready.
    sublime.set_timeout(init, START_DELAY)


def plugin_unloaded():
    # The worker threads handling requests/responses block when reading their
    # queue, so give them something.
    # XXX: This handler loads at times I wouldn't expect it to and ends up
    # killing the plugin. Disable this for now.
    # g_server.stop()
    pass


class ActivityTracker(sublime_plugin.EventListener):
    """After ST has been idle for an interval, sends requests to the analyzer
    if the buffer has been saved or is dirty.
    """
    edits = defaultdict(lambda: 0)
    edits_lock = threading.RLock()

    def increment_edits(self, view):
        with ActivityTracker.edits_lock:
            ActivityTracker.edits[view.id()] += 1
        sublime.set_timeout(lambda: self.check_idle(view), 750)

    def decrement_edits(self, view):
        with ActivityTracker.edits_lock:
            ActivityTracker.edits[view.id()] -= 1

    def on_idle(self, view):
        # _logger.debug("active view was idle; could send requests")
        if view.is_dirty() and is_active(view):
            _logger.debug('sending overlay data for %s', view.file_name())
            g_server.send_add_content(view)

    # TODO(guillermooo): Use on_modified_async
    def on_modified(self, view):
        if not is_view_dart_script(view):
            # Don't log here -- it'd impact performance.
            # _logger.debug('on_modified - not a dart file; aborting: %s',
            #     view.file_name())
            return

        if not view.file_name():
            # Don't log here -- it'd impact performance.
            # _logger.debug(
            #     'aborting because file does not exist on disk: %s',
            #     view.file_name())
            return

        self.increment_edits(view)

    def check_idle(self, view):
        with ActivityTracker.edits_lock:
            self.decrement_edits(view)
            if self.edits[view.id()] == 0:
                self.on_idle(view)

    def on_post_save(self, view):
        if not is_view_dart_script(view):
            # _logger.debug('on_post_save - not a dart file %s',
            #               view.file_name())
            return

        with ActivityTracker.edits_lock:
            # TODO(guillermooo): does .id() uniquely identify views
            # across windows?
            ActivityTracker.edits[view.id()] += 1
        sublime.set_timeout(lambda: self.check_idle(view), 1000)

        # The file has been saved, so force use of filesystem content.
        g_server.send_remove_content(view)

    def on_deactivated(self, view):
        # Any ongoing searches must be invalidated.
        del g_editor_context.search_id

        if not is_view_dart_script(view):
            return


    def on_activated(self, view):
        if not is_view_dart_script(view):
            # _logger.debug('on_activated - not a dart file %s',
            #               view.file_name())
            return

        if AnalysisServer.ping():
            g_server.add_root(view.file_name())

            if is_active(view):
                g_server.send_set_priority_files([view.file_name()])

                if view.is_dirty():
                    g_server.send_add_content(view)
        else:
            sublime.set_timeout(
                lambda: g_server.add_root(view.file_name()),
                START_DELAY + 1000)

            if is_active(view):
                sublime.set_timeout(
                    lambda: g_server.send_set_priority_files(
                                                        [view.file_name()]),
                    START_DELAY + 1000)

                if view.is_dirty():
                    sublime.set_timeout(
                        lambda: g_server.send_add_content(view),
                        START_DELAY + 1000)


class StdoutWatcher(threading.Thread):
    def __init__(self, server, path):
        super().__init__()
        self.path = path
        self.server = server

    def start(self):
        _logger.info("starting StdoutWatcher")

        try:
            # Awaiting other threads...
            self.server.ready_barrier.wait()
        except threading.BrokenBarrierError:
            _logger.error('could not start StdoutWatcher properly')
            return

        while True:
            data = self.server.stdout.readline().decode('utf-8')
            _logger.debug('data read from server: %s', repr(data))

            if not data:
                if self.server.stdin.closed:
                    _logger.info(
                        'StdoutWatcher is exiting by internal request')
                    return

                _logger.debug("StdoutWatcher - no data")
                time.sleep(.1)
                continue

            decoded = json.loads(data)
            # TODO(guillermooo): Some notifications need to have a HIGHEST
            # prio. For example, if we're getting a new search id.
            self.server.responses.put(decoded, view=decoded.get('file'),
                block=False)
        _logger.error('StdoutWatcher exited unexpectedly')


class AnalysisServer(object):
    MAX_ID = 9999999
    # Halts all worker threads until the server is ready.
    _ready_barrier = threading.Barrier(4, timeout=5)

    _request_id_lock = threading.Lock()
    _op_lock = threading.Lock()
    _write_lock = threading.Lock()

    _request_id = -1

    server = None

    @property
    def ready_barrier(self):
        return AnalysisServer._ready_barrier

    @property
    def stdout(self):
        return AnalysisServer.server.proc.stdout

    @property
    def stdin(self):
        return AnalysisServer.server.proc.stdin

    @staticmethod
    def get_request_id():
        with AnalysisServer._request_id_lock:
            if AnalysisServer._request_id >= AnalysisServer.MAX_ID:
                AnalysisServer._request_id = -1
            AnalysisServer._request_id += 1
            return AnalysisServer._request_id

    @staticmethod
    def ping():
        try:
            return AnalysisServer.server.is_running
        except AttributeError:
            return

    def __init__(self):
        self.roots = []
        self.priority_files = []
        self.requests = AnalyzerQueue('requests')
        self.responses = AnalyzerQueue('responses')

        reqh = RequestHandler(self)
        reqh.daemon = True
        reqh.start()

        resh = ResponseHandler(self)
        resh.daemon = True
        resh.start()

    @property
    def proc(self):
        return AnalysisServer.server

    def new_token(self):
        w = sublime.active_window()
        v = w.active_view()
        now = datetime.now()
        # 'c' indicates that this id was created at the client-side.
        token = w.id(), v.id(), '{}:{}:c{}'.format(w.id(), v.id(),
                                  AnalysisServer.get_request_id())
        return token

    def add_root(self, path):
        """Adds `path` to the monitored roots if it is unknown.

        If a `pubspec.yaml` is found in the path, its parent is monitored.
        Otherwise the passed-in directory name is monitored.

        @path
          Can be a directory or a file path.
        """
        if not path:
            _logger.debug('not a valid path: %s', path)
            return

        p, found = find_pubspec_path(path)
        if not found:
            _logger.debug('did not found pubspec.yaml in path: %s', path)

        with AnalysisServer._op_lock:
            if p not in self.roots:
                _logger.debug('adding new root: %s', p)
                self.roots.append(p)
                self.send_set_roots(self.roots)
                return

        _logger.debug('root already known: %s', p)

    def start(self):
        if AnalysisServer.ping():
            return

        sdk = SDK()

        _logger.info('starting AnalysisServer')

        AnalysisServer.server = PipeServer(['dart',
                            sdk.path_to_analysis_snapshot,
                           '--sdk={0}'.format(sdk.path_to_sdk)])
        AnalysisServer.server.start(working_dir=sdk.path_to_sdk)

        self.start_stdout_watcher()

        try:
            # Server is ready.
            self.ready_barrier.wait()
        except threading.BrokenBarrierError:
            _logger.error('could not start server properly')
            return

    def start_stdout_watcher(self):
        sdk = SDK()
        t = StdoutWatcher(self, sdk.path_to_sdk)
        # Thread dies with the main thread.
        t.daemon = True
        # XXX: This is necessary. If we call t.start() directly, ST hangs.
        sublime.set_timeout_async(t.start, 0)

    def stop(self):
        req = requests.shut_down(AnalysisServer.MAX_ID + 100)
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

    def send_set_roots(self, included=[], excluded=[]):
        _, _, token = self.new_token()
        req = requests.set_roots(token, included, excluded)
        _logger.info('sending set_roots request')
        self.requests.put(req, block=False)

    def send_find_top_level_decls(self, view, pattern):
        w_id, v_id, token = self.new_token()
        req = requests.find_top_level_decls(token, pattern)
        _logger.info('sending top level decls request')
        # TODO(guillermooo): Abstract this out.
        # track this type of req as it may expire
        g_req_to_resp['search']["{}:{}".format(w_id, v_id)] = token
        g_editor_context.search_id = token
        self.requests.put(req,
                          view=view,
                          priority=TaskPriority.HIGHEST,
                          block=False)

    def send_find_element_refs(self, view, potential=False):
        if not view:
            return

        _, _, token = self.new_token()
        fname = view.file_name()
        offset = view.sel()[0].b
        req = requests.find_element_refs(token, fname, offset, potential)
        _logger.info('sending find_element_refs request')
        g_editor_context.search_id = token
        self.requests.put(req, view=view, priority=TaskPriority.HIGHEST,
                          block=False)

    def send_add_content(self, view):
        w_id, v_id, token = self.new_token()
        data = {'type': 'add', 'content': view.substr(sublime.Region(0,
                                                            view.size()))}
        files = {view.file_name(): data}
        req = requests.update_content(token, files)
        _logger.info('sending update content request - add')
        # track this type of req as it may expire
        self.requests.put(req, view=view, priority=TaskPriority.HIGH,
                          block=False)

    def send_remove_content(self, view):
        w_id, v_id, token = self.new_token()
        files = {view.file_name(): {"type": "remove"}}
        req = requests.update_content(token, files)
        _logger.info('sending update content request - delete')
        self.requests.put(req, view=view, priority=TaskPriority.HIGH,
                          block=False)

    def send_set_priority_files(self, files):
        if files == self.priority_files:
            return

        w_id, v_id, token = self.new_token()
        _logger.info('sending set priority files request')
        req = requests.set_priority_files(token, files)
        self.requests.put(req, priority=TaskPriority.HIGH, block=False)


class ResponseHandler(threading.Thread):
    """ Handles responses from the response queue.
    """
    def __init__(self, server):
        super().__init__()
        self.server = server

    def run(self):
        _logger.info('starting ResponseHandler')

        try:
            # Awaiting other threads...
            self.server.ready_barrier.wait()
        except threading.BrokenBarrierError:
            _logger.error('could not start ResponseHandler properly')
            return

        response_maker = ResponseMaker(self.server.responses)

        try:
            for resp in response_maker.make():

                if resp is None:
                    # TODO(guillermooo): Is this necessary?
                    # Give ST a breath.
                    time.sleep(0.5)
                    continue

                if (resp.type == ResponseType.INTERNAL and
                    resp.internal_request == _SIGNAL_STOP):
                        _logger.info(
                            'ResponseHandler is exiting by internal request')
                        return

                # resp = Response(item)
                if resp.type == ResponseType.RESULT_ID:
                    _logger.debug('changing search id: %s -> %s', resp.id, resp.result_id)
                    g_editor_context.search_id = resp.result_id
                    if resp.result:
                        # out = OutputPanel('dart.results')
                        # g_editor_context.results_panel = out
                        # out.write(str(resp.result.to_encoded_pos()))
                        # out.show()
                        _logger.debug('^********************************************')
                        print("FOUND RESULT", resp.result.to_encoded_pos())
                        _logger.debug('^********************************************')
                    continue

                if resp.type == ResponseType.UNKNOWN:
                    _logger.debug('received unknown type of response: %s', resp)
                    continue

                if resp.type == 'search.results':
                    _logger.info('received search results')
                    # TODO(guillermooo): pass only result id.
                    if g_editor_context.check_token('search', resp.result_id):
                        _logger.debug('^********************************************')
                        _logger.debug('search results: %s', resp.search_results.results)
                        _logger.debug('^********************************************')
                    else:
                        _logger.debug('expired token')

                    continue

                if resp.type == ResponseType.ERRORS:
                    _logger.info('error data received from server')
                    # Make sure the right type is passed to the async
                    # code. `resp` may point to a different object when
                    # the lambda func finally has a chance to run.
                    errors = resp.copy()
                    sublime.set_timeout(lambda: actions.show_errors(errors),
                                        0)
                    continue

                elif resp.type == 'server.status':
                    info = resp.status
                    sublime.set_timeout(lambda: sublime.status_message(
                                        "Dart: " + info.message), 0)
                    continue

        except Exception as e:
            _logger.debug(e)
            print('Dart: exception while handling response.')
            print('========================================')
            print(e)
            print('========================================')


class RequestHandler(threading.Thread):
    """ Watches the requests queue and forwards them to the pipe server.
    """
    def __init__(self, server):
        super().__init__()
        self.server = server

    def run(self):
        _logger.info('starting RequestHandler')

        try:
            self.server.ready_barrier.wait()
        except threading.BrokenBarrierError:
            _logger.error('could not start RequestHandler properly')
            return

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
