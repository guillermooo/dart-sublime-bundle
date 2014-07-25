import sublime
import sublime_plugin

import os
from collections import defaultdict
import json
from datetime import datetime
import queue
import threading
import time
from subprocess import Popen
from subprocess import PIPE

from . import PluginLogger
from .lib.sdk import SDK
from .lib.plat import supress_window
from .lib.path import is_view_dart_script


_logger = PluginLogger(__name__)


g_shut_down_event = threading.Event()
g_requests = queue.Queue()
# Responses from server.
g_responses = queue.Queue()
g_edits_lock = threading.Lock()
g_server = None


def init():
    '''Start up core components of the analyzer plugin.
    '''
    global g_server
    _logger.debug('starting dart analyzer')

    reqh = RequestHandler()
    reqh.daemon = True
    reqh.start()
    resh = ResponseHandler()
    resh.daemon = True
    resh.start()

    g_server = AnalysisServer()
    g_server.start()


def plugin_loaded():
    # TODO(guillermooo): Enable graceful shutdown of threads.
    # Make ST more responsive on startup --- also helps the logger get ready.
    sublime.set_timeout(init, 2000)


class ActivityTracker(sublime_plugin.EventListener):
    """After ST has been idle for an interval, sends requests to the analyzer
    if the buffer has been saved or is dirty.
    """
    edits = defaultdict(lambda: 0)

    def on_idle(self, view):
        _logger.debug("active view was idle; sending requests")
        now = datetime.now()
        token = "{0}:{1}".format(view.buffer_id(),
                                 str(now.minute * 60 + now.second))
        g_requests.put({'id': token, 'method': 'server.getVersion'})

    def check_idle(self, view):
        # TODO(guillermooo): we need to send requests too if the buffer is
        # simply dirty but not yet saved.
        with g_edits_lock:
            self.edits[view.buffer_id()] -= 1
            if self.edits[view.buffer_id()] == 0:
                self.on_idle(view)

    def on_post_save(self, view):
        if not is_view_dart_script(view):
            _logger.debug('not a dart file %s', view.file_name())
            return

        with g_edits_lock:
            # TODO(guillermooo): does .buffer_id() uniquely identify buffers
            # across windows?
            ActivityTracker.edits[view.buffer_id()] += 1
            sublime.set_timeout(lambda: self.check_idle(view), 1000)


class StdoutWatcher(threading.Thread):
    def __init__(self, proc, path):
        super().__init__()
        self.proc = proc
        self.path = path

    def start(self):
        _logger.debug("starting StdoutWatcher")
        while True:
            data = self.proc.stdout.readline().decode('utf-8')
            _logger.debug('data read from server: %s', data)
            if not data:
                _logger.debug("StdoutWatcher - no data")
                time.sleep(.25)
                continue

            g_responses.put(json.loads(data))
        _logger.debug('StdoutWatcher exited unexpectedly')


class AnalysisServer(object):
    def __init__(self, path=None):
        super().__init__()
        self.path = path
        self.proc = None

    def start(self):
        # TODO(guillermooo): create pushcd context manager in lib/path.py.
        old = os.curdir
        # TODO(guillermooo): catch errors
        sdk = SDK()
        os.chdir(sdk.path_to_sdk)
        _logger.debug('starting AnalysisServer')
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
        self.proc.kill()

    def send(self, data):
        data = (json.dumps(data) + '\n').encode('utf-8')
        _logger.debug('sending %s', data)
        self.proc.stdin.write(data)
        self.proc.stdin.flush()


class ResponseHandler(threading.Thread):
    """ Handles responses from the analysis server.
    """
    def __init__(self):
        super().__init__()

    def run(self):
        _logger.debug('starting ResponseHandler')
        while True:
            time.sleep(.25)
            try:
                item = g_responses.get(0.1)
                _logger.debug("processing response: %s", item)
            except queue.Empty:
                pass


class RequestHandler(threading.Thread):
    """ Handles requests to the analysis server.
    """
    def __init__(self):
        super().__init__()

    def run(self):
        _logger.debug('starting RequestHandler')
        while True:
            time.sleep(.25)
            try:
                item = g_requests.get(0.1)
                g_server.send(item)
            except queue.Empty:
                pass
