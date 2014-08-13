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
from Dart.lib.analyzer import actions
from Dart.lib.analyzer import requests
from Dart.lib.analyzer.pipe_server import PipeServer
from Dart.lib.analyzer.response import Response
from Dart.lib.path import find_pubspec_path
from Dart.lib.path import is_active
from Dart.lib.path import is_view_dart_script
from Dart.lib.plat import supress_window
from Dart.lib.sdk import SDK


_logger = PluginLogger(__name__)


START_DELAY = 2500
_SIGNAL_STOP = object()


g_server = None

# maps:
#   req_type => view_id
#   view_id => valid token for this type of request
g_req_to_resp = {
    "search": {},
}


def init():
    global g_server
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
    g_server.requests.put({'_internal': _SIGNAL_STOP})
    g_server.responses.put({'_internal': _SIGNAL_STOP})
    g_server.stop()


class ActivityTracker(sublime_plugin.EventListener):
    """After ST has been idle for an interval, sends requests to the analyzer
    if the buffer has been saved or is dirty.
    """
    edits = defaultdict(lambda: 0)
    edits_lock = threading.RLock()

    def increment_edits(self, view):
        with ActivityTracker.edits_lock:
            ActivityTracker.edits[view.id()] += 1
            sublime.set_timeout(lambda: self.check_idle(view), 1000)

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
        # TODO(guillermooo): we need to send requests too if the buffer is
        # simply dirty but not yet saved.
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

    def on_activated(self, view):
        # TODO(guillermooo): We need to updateContent here if the file is
        # dirty on_activated.
        if not is_view_dart_script(view):
            # _logger.debug('on_activated - not a dart file %s',
            #               view.file_name())
            return

        if AnalysisServer.ping():
            g_server.add_root(view.file_name())
        else:
            # TODO(guillermooo): enqueue request
            sublime.set_timeout(
                lambda: g_server.add_root(view.file_name()),
                                          AnalysisServer.START_DELAY + 1000)


class StdoutWatcher(threading.Thread):
    def __init__(self, server, path):
        super().__init__()
        self.path = path
        self.server = server

    def start(self):
        _logger.info("starting StdoutWatcher")
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

            self.server.responses.put(json.loads(data))
        _logger.error('StdoutWatcher exited unexpectedly')


class AnalysisServer(object):
    server = None

    @property
    def stdout(self):
        return AnalysisServer.server.proc.stdout

    @property
    def stdin(self):
        return AnalysisServer.server.proc.stdin

    @staticmethod
    def ping():
        try:
            return AnalysisServer.server.is_running
        except AttributeError:
            return

    def __init__(self):
        self.roots = []
        # TODO(guillermooo): use priority queues?
        self.requests = queue.Queue()
        self.responses = queue.Queue()

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
        token = w.id(), v.id(), '{}:{}:{}'.format(w.id(), v.id(),
                                  now.minute * 60 + now.second)
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

        t = StdoutWatcher(self, sdk.path_to_sdk)
        # Thread dies with the main thread.
        t.daemon = True
        # TODO(guillermooo): do we need timeout async here?
        sublime.set_timeout_async(t.start, 0)

    def stop(self):
        # TODO(guillermooo): Use the server's own shutdown mechanism.
        self.server.stop()

    def send(self, data):
        # TODO(guillermooo): should be a request via queue?
        data = (json.dumps(data) + '\n').encode('utf-8')
        _logger.debug('sending %s', data)
        self.stdin.write(data)
        self.stdin.flush()

    def send_set_roots(self, included=[], excluded=[]):
        _, _, token = self.new_token()
        req = requests.set_roots(token, included, excluded)
        _logger.info('sending set_roots request')
        self.requests.put(req)

    def send_find_top_level_decls(self, pattern):
        w_id, v_id, token = self.new_token()
        req = requests.find_top_level_decls(token, pattern)
        _logger.info('sending top level decls request')
        # track this type of req as it may expire
        g_req_to_resp['search']["{}:{}".format(w_id, v_id)] = token
        self.requests.put(req)

    def send_add_content(self, view):
        w_id, v_id, token = self.new_token()
        data = {'type': 'add', 'content': view.substr(sublime.Region(0,
                                                            view.size()))}
        files = {view.file_name(): data}
        req = requests.update_content(token, files)
        _logger.info('sending update content request')
        # track this type of req as it may expire
        self.requests.put(req)

    def send_remove_content(self, view):
        w_id, v_id, token = self.new_token()
        files = {view.file_name(): {"type": "remove"}}
        req = requests.update_content(token, files)
        self.requests.put(req)


class ResponseHandler(threading.Thread):
    """ Handles responses from the response queue.
    """
    def __init__(self, server):
        super().__init__()
        self.server = server

    def run(self):
        _logger.info('starting ResponseHandler')
        while True:
            time.sleep(0.05)
            try:
                item = self.server.responses.get(0.1)

                if item.get('_internal') == _SIGNAL_STOP:
                    _logger.info(
                        'ResponseHandler is exiting by internal request')
                    continue

                try:
                    resp = Response(item)
                    if resp.type == '<unknown>':
                        _logger.info('received unknown type of response')
                        if resp.has_new_id:
                            _logger.debug('received new id for request: %s -> %s', resp.id, resp.new_id)
                            win_view = resp.id.index(":", resp.id.index(":") + 1)
                            g_req_to_resp["search"][resp.id[:win_view]] = \
                                                                resp.new_id

                        continue

                    if resp.type == 'search.results':
                        _logger.info('received search results')
                        _logger.debug('results: %s', resp.search_results)
                        continue

                    if resp.type == 'analysis.errors':
                        if resp.has_errors and len(resp.errors) > 0:
                            _logger.info('error data received from server')
                            sublime.set_timeout(
                                lambda: actions.display_error(resp.errors), 0)
                            continue
                        else:
                            v = sublime.active_window().active_view()
                            if resp.errors.file and (resp.errors.file == v.file_name()):
                                sublime.set_timeout(actions.clear_ui, 0)
                                continue

                    elif resp.type == 'server.status':
                        info = resp.status
                        sublime.set_timeout(lambda: sublime.status_message(
                                            "Dart: " + info.message))
                except Exception as e:
                    _logger.debug(e)
                    print('Dart: exception while handling response.')
                    print('========================================')
                    print(e.message)
                    print('========================================')

            except queue.Empty:
                pass


class RequestHandler(threading.Thread):
    """ Watches the requests queue and forwards them to the pipe server.
    """
    def __init__(self, server):
        super().__init__()
        self.server = server

    def run(self):
        _logger.info('starting RequestHandler')
        while True:
            try:
                item = self.server.requests.get(0.1)

                if item.get('_internal') == _SIGNAL_STOP:
                    _logger.info(
                        'RequestHandler is exiting by internal request')
                    return

                self.server.send(item)
            except queue.Empty:
                pass
