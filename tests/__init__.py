# Copyright (c) 2014, Guillermo López-Anglada. Please see the AUTHORS file for details.
# All rights reserved. Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.)

import unittest

import sublime


class SyntaxTextCase(unittest.TestCase):
    def setUp(self):
        self.view = sublime.active_window().new_file()

    def append(self, text):
        self.view.run_command('append', {'characters': text})

    def setSyntax(self, path):
        self.view.set_syntax_file(path)

    def getScopeNameAt(self, pt):
        return self.view.scope_name(pt)

    def getScopeNameAtRowCol(self, row, col):
        pt = self.view.text_point(row, col)
        return self.getScopeNameAt(pt)

    def getNarrowestScopeNameAt(self, pt):
        name = self.getScopeNameAt(pt)
        return name.split()[-1]

    def getNarrowestScopeNameAtRowCol(self, row, col):
        pt = self.view.text_point(row, col)
        return self.getNarrowestScopeNameAt(pt)

    def tearDown(self):
        self.view.set_scratch(True)
        self.view.close()


class DartSyntaxTestCase(SyntaxTextCase):
    def setUp(self):
        super().setUp()
        self.setSyntax('Packages/Dart/Dart.tmLanguage')

