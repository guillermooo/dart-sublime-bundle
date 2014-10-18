# Copyright (c) 2014, Guillermo López-Anglada. Please see the AUTHORS file for details.
# All rights reserved. Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.)

import sublime
import sublime_plugin

from Dart.lib.event import EventSource


class DartBuildCommandBase(sublime_plugin.WindowCommand, EventSource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def execute(self, **kwargs):
        self.window.run_command('dart_exec', kwargs)
