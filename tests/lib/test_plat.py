import sublime

import unittest
import os

from Dart.lib.path import to_platform_path


class Test_to_platform_path(unittest.TestCase):
    def setUp(self):
        self.view = sublime.active_window().new_file()

    @unittest.skipUnless(os.name == 'nt', 'only for Windows')
    def testAppendsExtensionOnWindows(self):
        actual = to_platform_path('foo', '.exe')
        self.assertEqual('foo.exe', actual)

    @unittest.skipUnless(os.name == 'nt', 'only for Windows')
    def testAppendsPathFragment(self):
        actual = to_platform_path('foo', 'bar')
        self.assertEqual('foo\\bar', actual)

    @unittest.skipIf(os.name == 'nt', 'only for non-Windows platforms')
    def testDoesNotAppendPathFragment(self):
        actual = to_platform_path('foo', 'bar')
        self.assertEqual('foo', actual)

    def tearDown(self):
        self.view.close()
