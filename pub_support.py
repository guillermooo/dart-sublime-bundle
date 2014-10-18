# Copyright (c) 2014, Guillermo López-Anglada. Please see the AUTHORS file for details.
# All rights reserved. Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.)

import sublime
import sublime_plugin

from os.path import join
import os
import subprocess
import threading

from . import PluginLogger
from .lib.panels import OutputPanel
from .lib.path import is_pubspec
from .lib.path import is_view_dart_script
from .lib.plat import is_windows
from .lib.plat import supress_window
from .lib.sdk import SDK
from Dart.lib import ga
from Dart.lib.build.base import DartBuildCommandBase
from Dart.lib.event import EventSource
from Dart.lib.sublime import after


_logger = PluginLogger(__name__)


class PubspecListener(sublime_plugin.EventListener):
    def __init__(self, *args, **kwargs):
        sublime_plugin.EventListener.__init__(self, *args, **kwargs)

    def on_post_save(self, view):
        if not is_pubspec(view):
            return

        _logger.debug("running pub with %s", view.file_name())
        RunPub(view, view.file_name())


def RunPub(view, file_name):
    # FIXME: Infefficient. We should store the path to the sdk away.
    dartsdk_path = SDK().path

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

        after(50, lambda: self.callback(data))

    def format_data(self, data):
        return data.replace('\r', '')

    def callback(self, data):
        panel = OutputPanel('dart.out')
        panel.write(self.format_data(data))
        panel.show()


# We need a command because we want to use analytics. We can't simply use a
# .sublime-build file.
class DartPubBuildCommand(DartBuildCommandBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_event_handler(EventSource.ON_PUB_BUILD,
                               DartPubBuildCommand.on_pub_build)

    def run(self, working_dir=None, **kwargs):
        assert working_dir is not None, 'wrong call'
        self.raise_event(self, EventSource.ON_PUB_BUILD)
        self.execute(**{'working_dir': working_dir,
                        'shell_cmd': 'pub build',
                        'preamble': 'Running pub build...\n',
                        })

    @classmethod
    def on_pub_build(self, *args, **kwargs):
        ga.Event(category='actions',
                 action='on_pub_build',
                 label='Running "pub build" command',
                 value=1,
                 ).send()
