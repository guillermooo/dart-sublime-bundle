import sublime

import unittest
from unittest import mock
import os
from subprocess import check_output

from Dart.lib.path import find_in_path
from Dart.lib.path import is_pubspec
from Dart.lib.path import extension_equals
from Dart.lib.path import join_exclusive_parts


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


class Test_join_exclusive_parts(unittest.TestCase):
    @unittest.skipIf(os.name == 'nt', 'only for Unix')
    def testReturnsFullPathIfPerfectMatchUnix(self):
        # TODO(guillermooo): Is OSX fsys case sensitive?
        a = '/Users/foo/dart-sdk/chromium/Chromium.app/Contents/MacOS/Chromium'
        b = 'Chromium.app/Contents/MacOS/Chromium'
        self.assertEqual(join_exclusive_parts(a, b), a)

    @unittest.skipIf(os.name == 'nt', 'only for Unix')
    def testReturnsJoined_Unix(self):
        # TODO(guillermooo): Is OSX fsys case sensitive?
        a = '/Users/foo/dart-sdk/chromium/Chromium.app/Contents/MacOS'
        b = 'Chromium.app/Contents/MacOS/Chromium'
        self.assertEqual(join_exclusive_parts(a, b), os.path.join(a, 'Chromium'))

    @unittest.skipUnless(os.name != 'nt', 'only for Unix')
    def testReturnsJoinedPartial1_Windows(self):
        # TODO(guillermooo): Is OSX fsys case sensitive?
        a = '/Users/foo/dart-sdk/chromium/Chromium.app/Contents'
        b = 'Chromium.app/Contents/MacOS/Chromium'
        self.assertEqual(join_exclusive_parts(a, b), os.path.join(a, 'MacOS/Chromium'))

    @unittest.skipUnless(os.name == 'nt', 'only for Windows')
    def testReturnsFullPathIfPerfectMatch_Win(self):
        # TODO(guillermooo): case sensitivity
        a = r'C:\dart-sdk\chromium\chromium.exe'
        b = r'chromium.exe'
        self.assertEqual(join_exclusive_parts(a, b), a)
        b = r'chromium\chromium.exe'
        self.assertEqual(join_exclusive_parts(a, b), a)

    @unittest.skipUnless(os.name == 'nt', 'only for Windows')
    def testReturnsJoined_Windows(self):
        # TODO(guillermooo): case sensitivity
        a = r'C:\dart-sdk\chromium\\'
        b = r'chromium.exe'
        self.assertEqual(join_exclusive_parts(a, b), os.path.join(a, b))

    @unittest.skipUnless(os.name == 'nt', 'only for Windows')
    def testReturnsJoinedPartial1_Windows(self):
        # TODO(guillermooo): case sensitivity
        a = r'C:\dart-sdk\\chromium'
        b = r'chromium\chromium.exe'
        self.assertEqual(join_exclusive_parts(a, b), os.path.join(a, 'chromium.exe'))
