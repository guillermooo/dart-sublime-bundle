import sublime

import unittest
import os

from Dart.lib.sdk import SDK


class Test_SDK(unittest.TestCase):
    def setUp(self):
        self.view = sublime.active_window().new_file()

    def testUsesUserDefinedPath(self):
        sdk = SDK('/xxx/yyy')
        self.assertEqual(sdk.path_to_sdk, '/xxx/yyy')

    @unittest.skipUnless(os.name == 'nt', 'only for Windows')
    def testCanFindPathToDartInterpreterOnWindows(self):
        self.view.settings().set('dartsdk_path', 'c:/foo/bar')
        sdk = SDK()
        self.assertEqual(sdk.path_to_dart, r'c:\foo\bar\bin\dart.exe')

    @unittest.skipIf(os.name == 'nt', 'only for non-Windows platforms')
    def testCanFindPathToDartInterpreter(self):
        sdk = SDK('/foo/bar')
        self.assertEqual(sdk.path_to_dart, '/foo/bar/bin/dart')

    def tearDown(self):
        self.view.close()
