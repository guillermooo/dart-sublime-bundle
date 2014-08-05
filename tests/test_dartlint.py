import sublime

import unittest

from Dart.lib.path import is_dart_script
from Dart.lib.path import is_view_dart_script


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
