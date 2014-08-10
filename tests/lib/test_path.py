import sublime

import unittest
from unittest import mock
import os
from subprocess import check_output

from Dart.lib.path import extension_equals
from Dart.lib.path import find_in_path
from Dart.lib.path import is_dart_script
from Dart.lib.path import is_pubspec
from Dart.lib.path import is_view_dart_script


class Test_find_in_path(unittest.TestCase):
    def setUp(self):
        self.view = sublime.active_window().new_file()

    @unittest.skipUnless(os.name == 'nt', 'only for Windows')
    def testCanFindBinaryInPathWin(self):
        actual = find_in_path('cmd', '.exe')
        self.assertEqual(os.path.dirname(os.environ['COMSPEC']), actual)

    @unittest.skipIf(os.name == 'nt', 'only for non-Windows platforms')
    def testCanFindBinaryInPathLinux(self):
        expected = check_output(['which', 'grep']).decode('utf-8')
        actual = find_in_path('grep')
        self.assertEqual(os.path.dirname(expected), actual)

    def tearDown(self):
        self.view.close()


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


class Test_extension_equals_WithPaths(unittest.TestCase):
    def testCanDetectSameExtension(self):
        self.assertTrue(extension_equals("foo.dart", ".dart"))

    def testCanDetectDifferentExtension(self):
        self.assertFalse(extension_equals("foo.dart", ".txt"))


class Test_extension_equals_WithViews(unittest.TestCase):
    def setUp(self):
        self.view = sublime.active_window().new_file()

    def testFailsIfFileNotOnDisk(self):
        self.assertFalse(extension_equals(self.view, '.dart'))

    def testCanSucceed(self):
        self.view.file_name = mock.Mock(return_value='c:\\foo.dart')
        self.assertTrue(extension_equals(self.view, '.dart'))

    def tearDown(self):
        self.view.close()
