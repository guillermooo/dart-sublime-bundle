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

from . import PluginLogger
from .lib.analyzer import actions
from .lib.analyzer import requests
from .lib.analyzer.response import Response
from .lib.path import find_pubspec
from .lib.path import is_view_dart_script
from .lib.plat import supress_window
from .lib.sdk import SDK


_logger = PluginLogger(__name__)


_SERVER_START_DELAY = 2500
_SIGNAL_STOP = object()


g_requests = queue.Queue()
# Responses from server.
g_responses = queue.Queue()
g_edits_lock = threading.Lock()
g_server = None
g_server_ready = threading.RLock()


def init():
    '''Start up core components of the analyzer plugin.
    '''
    global g_server
    _logger.debug('starting dart analyzer')

    try:
        reqh = RequestHandler()
        reqh.daemon = True
        reqh.start()

        resh = ResponseHandler()
        resh.daemon = True
        resh.start()

        with g_server_ready:
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
    sublime.set_timeout(init, _SERVER_START_DELAY)


def plugin_unloaded():
    # The worker threads handling requests/responses block when reading their
    # queue, so give them something.
    g_requests.put({'_internal': _SIGNAL_STOP})
    g_responses.put({'_internal': _SIGNAL_STOP})
    g_server.stop()


class ActivityTracker(sublime_plugin.EventListener):
    """After ST has been idle for an interval, sends requests to the analyzer
    if the buffer has been saved or is dirty.
    """
    edits = defaultdict(lambda: 0)

    def on_idle(self, view):
        _logger.debug("active view was idle; could send requests")
        now = datetime.now()
        token = "{0}:{1}".format(view.buffer_id(),
                                 str(now.minute * 60 + now.second))

    def check_idle(self, view):
        # TODO(guillermooo): we need to send requests too if the buffer is
        # simply dirty but not yet saved.
        with g_edits_lock:
            self.edits[view.buffer_id()] -= 1
            if self.edits[view.buffer_id()] == 0:
                self.on_idle(view)

    def on_post_save(self, view):
        if not is_view_dart_script(view):
            _logger.debug('on_post_save - not a dart file %s',
                          view.file_name())
            return

        with g_edits_lock:
            # TODO(guillermooo): does .buffer_id() uniquely identify buffers
            # across windows?
            ActivityTracker.edits[view.buffer_id()] += 1
            sublime.set_timeout(lambda: self.check_idle(view), 1000)

    def on_activated(self, view):
        if not is_view_dart_script(view):
            _logger.debug('on_activated - not a dart file %s',
                          view.file_name())
            return

        with g_server_ready:
            if g_server:
                g_server.add_root(view.file_name())
            else:
                sublime.set_timeout(
                    lambda: g_server.add_root(view.file_name()),
                                              _SERVER_START_DELAY + 1000)


class StdoutWatcher(threading.Thread):
    def __init__(self, proc, path):
        super().__init__()
        self.proc = proc
        self.path = path

    def start(self):
        _logger.info("starting StdoutWatcher")
        while True:
            data = self.proc.stdout.readline().decode('utf-8')
            _logger.debug('data read from server: %s', repr(data))

            if not data:
                if self.proc.stdin.closed:
                    _logger.info(
                        'StdoutWatcher is exiting by internal request')
                    return

                _logger.debug("StdoutWatcher - no data")
                time.sleep(.25)
                continue

            g_responses.put(json.loads(data))
        _logger.error('StdoutWatcher exited unexpectedly')


class AnalysisServer(object):
    def __init__(self, path=None):
        super().__init__()
        self.path = path
        self.proc = None
        self.roots = []
        # buffer id -> token
        self.tokens = {}
        self.tokens_lock = threading.Lock()

    def new_token(self):
        v = sublime.active_window().active_view()
        now = datetime.now()
        token = '{}:{}'.format(v.buffer_id(), now.minute * 60 + now.second)
        return token

    def add_root(self, path):
        """Adds `path` to the monitored roots if it is unknown.

        If a `pubspec.yaml` is found in the path, its parent is monitored.
        Otherwise the passed in path is monitored as is.

        @path
          Can be a directory or a file path.
        """
        if not path:
            _logger.debug('not a valid path: %s', path)
            return

        p, found = os.path.dirname(find_pubspec(path))
        if not found:
            _logger.debug('did not found pubspec.yaml in path: %s', path)

        if p not in self.roots:
            _logger.debug('adding new root: %s', p)
            self.roots.append(p)
            self.send_set_roots(self.roots)
            return

        _logger.debug('root already known: %s', p)

    def start(self):
        # TODO(guillermooo): create pushcd context manager in lib/path.py.
        old = os.curdir
        # TODO(guillermooo): catch errors
        sdk = SDK()
        os.chdir(sdk.path_to_sdk)
        _logger.info('starting AnalysisServer')
        self.proc = Popen(['dart',
                           sdk.path_to_analysis_snapshot,
                           '--sdk={0}'.format(sdk.path_to_sdk)],
                           stdout=PIPE, stdin=PIPE, stderr=PIPE,
                           startupinfo=supress_window())
        os.chdir(old)
        t = StdoutWatcher(self.proc, sdk.path_to_sdk)
        # Thread dies with the main thread.
        t.daemon = True
        sublime.set_timeout_async(t.start, 0)

    def stop(self):
        self.proc.stdin.close()
        self.proc.stdout.close()
        self.proc.kill()

    def send(self, data):
        data = (json.dumps(data) + '\n').encode('utf-8')
        _logger.debug('sending %s', data)
        self.proc.stdin.write(data)
        self.proc.stdin.flush()

    def send_set_roots(self, included=[], excluded=[]):
        token = self.new_token()
        req = requests.set_roots(token, included, excluded)
        _logger.info('sending set_roots request')
        g_requests.put(req)


class ResponseHandler(threading.Thread):
    """ Handles responses from the analysis server.
    """
    def __init__(self):
        super().__init__()

    def run(self):
        _logger.info('starting ResponseHandler')
        while True:
            time.sleep(.25)
            try:
                item = g_responses.get(0.1)
                _logger.info("processing response")

                if item.get('_internal') == _SIGNAL_STOP:
                    _logger.info(
                        'ResponseHandler is exiting by internal request')
                    return

                try:
                    resp = Response(item)
                    if resp.type == 'analysis.errors':
                        if resp.has_errors:
                            sublime.set_timeout(
                                lambda: actions.display_error(resp.errors), 0)
                        else:
                            sublime.set_timeout(actions.wipe_ui, 0)
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
    """ Handles requests to the analysis server.
    """
    def __init__(self):
        super().__init__()

    def run(self):
        _logger.info('starting RequestHandler')
        while True:
            time.sleep(.25)
            try:
                item = g_requests.get(0.1)

                if item.get('_internal') == _SIGNAL_STOP:
                    _logger.info(
                        'RequestHandler is exiting by internal request')
                    return

                g_server.send(item)
            except queue.Empty:
                pass
