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
from .lib.sdk import SDK
from .lib.path import is_pubspec
from .lib.path import is_view_dart_script


_logger = PluginLogger(__name__)


class PubspecListener(sublime_plugin.EventListener):
    def __init__(self, *args, **kwargs):
        sublime_plugin.EventListener.__init__(self, *args, **kwargs)

    def on_activated(self, view):
        if not (is_pubspec(view) or is_view_dart_script(view)):
            return

        # TODO(guillermooo): I cannot get automatic detection of build sys
        # working. This code will make build systems change even if the user
        # has not enabled automatic detection of builds systems.
        if is_pubspec(view):
            _logger.debug('changing build system to "pubspec"')
            view.window().run_command('set_build_system', {
                "file": "Packages/Dart/Support/Dart - Pubspec.sublime-build"})
            return

        _logger.debug('changing build system to "dart"')
        view.window().run_command('set_build_system', {
            "file": "Packages/Dart/Support/Dart.sublime-build"})

    def on_post_save(self, view):
        if not is_pubspec(view):
            return

        _logger.debug("running pub with %s", view.file_name())
        RunPub(view, view.file_name())


def RunPub(view, file_name):
    # FIXME: Infefficient. We should store the path to the sdk away.
    dartsdk_path = SDK().path_to_sdk

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

        print('pub get %s' % self.file_name)
        proc = subprocess.Popen([pub_path, 'get'],
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
