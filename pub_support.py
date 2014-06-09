import sublime
import sublime_plugin

from os.path import join
import os
import subprocess
import threading

from .lib.plat import is_windows
from .lib.plat import supress_window
from .lib.panels import OutputPanel
from . import PluginLogger


_logger = PluginLogger(__name__)


class PubspecListener(sublime_plugin.EventListener):
    def __init__(self, *args, **kwargs):
        sublime_plugin.EventListener.__init__(self, *args, **kwargs)

    def on_post_save(self, view):
        name = view.file_name()

        if os.path.basename(name) == 'pubspec.yaml':
            _logger.debug("running pub with %s", name)
            RunPub(view, name)


def RunPub(view, file_name):
    dartsdk_path = view.settings().get('dartsdk_path')

    if not dartsdk_path:
        _logger.debug("`dartsdk_path` missing; aborting pub")
        return

    PubThread(view.window(), dartsdk_path, file_name).start()


# TODO(guillermooo): Perhaps we can replace this with Default.exec.AsyncProc.
class PubThread(threading.Thread):
    def __init__(self, window, dartsdk_path, file_name):
        super(PubThread, self).__init__()
        self.daemon = True
        self.window = window
        self.dartsdk_path = dartsdk_path
        self.file_name = file_name

    def run(self):
        working_directory = os.path.dirname(self.file_name)
        pub_path = join(self.dartsdk_path, 'bin', 'pub')

        if is_windows():
            pub_path += '.bat'

        print('pub install %s' % self.file_name)
        proc = subprocess.Popen([pub_path, 'install'],
                                cwd=working_directory,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT,
                                startupinfo=supress_window())

        out, errs = proc.communicate()
        data = out.decode('utf-8')

        if proc.returncode != 0:
            errs = errs.decode('utf-8')
            _logger.error("error running pub: %s\n%s", self.file_name, errs)
            data = 'error running pub: %s\n%s' % (self.file_name, errs)

        sublime.set_timeout(lambda: self.callback(data), 50)

    def format_data(self, data):
        return data.replace('\r', '')

    def callback(self, data):
        panel = OutputPanel('dart.pub')
        panel.write(self.format_data(data))
        panel.show()
