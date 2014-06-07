import sublime
import sublime_plugin

from os.path import join
import os
import subprocess
import threading

from .lib.plat import is_windows
from .lib.plat import supress_window
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
    dartsdk_path = view.settings.get('dartsdk_path')

    if not dartsdk_path:
        _logger.debug("`dartsdk_path` missing; aborting pub")
        return

    PubThread(view.window(), dartsdk_path, file_name).start()


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
        out, _ = proc.communicate()

        if proc.returncode != 0:
            _logger.error("error running pub: %s\n%s", self.file_name, out)
            self.output = 'error running pub: %s\n%s' % (self.file_name, out)
            sublime.set_timeout(self.callback, 0)

    def callback(self):
        output_panel = self.window.get_output_panel('pub')
        self.window.run_command('show_panel', {'panel': 'output.pub'})
        edit = output_panel.begin_edit()
        output_panel.insert(edit, output_panel.size(), self.output)
        output_panel.end_edit(edit)
