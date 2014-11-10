# Copyright (c) 2014, Guillermo López-Anglada. Please see the AUTHORS file for details.
# All rights reserved. Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.)

import sublime

from subprocess import check_output
from unittest import mock
import os
import unittest

from Dart.lib.path import is_dart_script
from Dart.lib.path import is_pubspec
from Dart.lib.path import is_view_dart_script


class Test_is_pubspec(unittest.TestCase):
    def setUp(self):
        self.view = sublime.active_window().new_file()

    def testCanDetectPubspecFile(self):
        view = mock.Mock()
        view.file_name = mock.Mock(return_value='xxx/pubspec.yaml')
        self.assertTrue(is_pubspec(view))

    def testCanDetectPubspecFileAsPath(self):
        self.assertTrue(is_pubspec('xxx/pubspec.yaml'))

    def testFailsIfNotAPubspecFile(self):
        self.assertFalse(is_pubspec(self.view))

    def tearDown(self):
        self.view.close()


class Test_is_dart_script(unittest.TestCase):
    def testSucceedsIfDartScript(self):
        self.assertTrue(is_dart_script("/some/path/foo.dart"))

    def testFailsIfNotDartScript(self):
        self.assertFalse(is_dart_script("/some/path/foo.txt"))

    def testFailsWithEmtpyPath(self):
        self.assertFalse(is_dart_script(""))


class Test_is_view_dart_script(unittest.TestCase):
    def setUp(self):
        self.view = sublime.active_window().new_file()

    def testFailsIfFileNotOnDisk(self):
        self.assertFalse(is_view_dart_script(self.view))

    def tearDown(self):
        self.view.close()
