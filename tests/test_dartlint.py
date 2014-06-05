import unittest

import sublime

from Dart.dartlint import is_dart_script
from Dart.dartlint import is_view_dart_script
from Dart.dartlint import extension_equals
from Dart.dartlint import view_extension_equals


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


class Test_extension_equals(unittest.TestCase):
    def testCanDetectSameExtension(self):
        self.assertTrue(extension_equals("foo.dart", ".dart"))

    def testCanDetectDifferentExtension(self):
        self.assertFalse(extension_equals("foo.dart", ".txt"))


class Test_view_extension_equals(unittest.TestCase):
    def setUp(self):
        self.view = sublime.active_window().new_file()

    def testFailsIfFileNotOnDisk(self):
        self.assertFalse(view_extension_equals(self.view, '.dart'))

    def tearDown(self):
        self.view.close()
