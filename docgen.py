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


# TODO(guillermooo): This process cannot be killed with DartStopAll.
class DartAnalyzerCommand(sublime_plugin.WindowCommand):
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


        cmd = ["dartanalyzer", view.file_name()]
        if sublime.platform() == 'windows':
            cmd = ["dartanalyzer.bat", view.file_name()]
        elif sublime.platform() == 'osx':
            cmd = ["/bin/bash", "--login", "-c",
                   "dartanalyzer \"{}\"".format(view.file_name())]

        self.window.run_command('exec', {
            "cmd": cmd,
            "file_regex": "^(?:\\[(?:error|warning|hint)\\].*?)\\((.*?\\.dart), line (\\d*), col (\\d*)\\)$",
            "working_dir": path,
            })

# TODO(guillermooo): We have F7 and Ctrl+F7 -- do we need this too?
# Do we need a 'run' command?
# {
#     "name": "Dart: Run",
#     "cmd": ["dart", "--checked", "$file"],
#     "file_regex": "'file:///(.+)': error: line (\\d+) pos (\\d+): (.*)$",

#     "windows":
#     {
#         "cmd": ["dart.exe", "--checked", "$file"]
#     },
#     "osx":
#     {
#         "cmd": ["/bin/bash", "--login", "-c", "dart --checked $file"]
#     }
# }
