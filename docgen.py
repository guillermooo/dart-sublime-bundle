# Copyright (c) 2014, Guillermo López-Anglada. Please see the AUTHORS file for details.
# All rights reserved. Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.)

import sublime
import sublime_plugin

import os

from Dart.lib.pub_package import find_pubspec


# TODO(guillermooo): This process cannot be killed with DartStopAll.
class DartGenerateDocsCommand(sublime_plugin.WindowCommand):
    def run(self):
        view = self.window.active_view()
        if not view:
            return

        if not view.file_name():
            return

        path = find_pubspec(view.file_name())
        if not path:
            return
        path = os.path.dirname(path)

        cmd = ["docgen", "--no-include-sdk", path]
        if sublime.platform() == 'windows':
            cmd = ["docgen.bat", "--no-include-sdk", path]
        elif sublime.platform() == 'osx':
            cmd = ["/bin/bash", "--login", "-c",
                    "docgen --no-include-sdk " + path]

        self.window.run_command('exec', {
            "cmd": cmd,
            "working_dir": path,
            })


# TODO(guillermooo): This process cannot be killed with DartStopAll.
class DartServeDocsCommand(sublime_plugin.WindowCommand):
    def run(self):
        view = self.window.active_view()
        if not view:
            return

        if not view.file_name():
            return

        path = find_pubspec(view.file_name())
        if not path:
            return
        path = os.path.dirname(path)

        cmd = ["docgen", "--no-include-sdk", "--serve", path]
        if sublime.platform() == 'windows':
            cmd = ["docgen.bat", "--no-include-sdk", "--serve", path]
        elif sublime.platform() == 'osx':
            cmd = ["/bin/bash", "--login", "-c",
                    "docgen --no-include-sdk --serve " + path]

        self.window.run_command('exec', {
            "cmd": cmd,
            "working_dir": path,
            })
