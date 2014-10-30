# Copyright (c) 2014, Guillermo López-Anglada. Please see the AUTHORS file for details.
# All rights reserved. Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.)

import sublime_plugin
import sublime


class DartKillToEol(sublime_plugin.TextCommand):
    '''Kills text from caret to EOL.
    '''
    def run(self, edit):
        eol = self.view.size()
        self.view.erase(edit, sublime.Region(self.view.sel()[0].b, eol))
