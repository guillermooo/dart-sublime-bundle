import sublime

import unittest
from unittest import mock
import os


from Dart.lib.sdk import SDK


class Test_SDK(unittest.TestCase):
    def setUp(self):
        self.view = sublime.active_window().new_file()

    def testUsesUserDefinedPath(self):
        with mock.patch('os.path.exists', lambda x: True):
            sdk = SDK('/xxx/yyy')
            self.assertEqual(sdk.path_to_sdk, '/xxx/yyy')

    @unittest.skipIf(os.name == 'nt', 'only for non-Windows platforms')
    def testCanFindPathToDartInterpreter(self):
        with mock.patch('os.path.exists', lambda x: True):
            sdk = SDK('/foo/bar')
            self.assertEqual(sdk.path_to_dart, '/foo/bar/bin/dart')

    @unittest.skipIf(os.name == 'nt', 'only for non-Windows platforms')
    def testCanFindPathToDartAnalyzer(self):
        with mock.patch('os.path.exists', lambda x: True):
            sdk = SDK('/foo/bar')
            self.assertEqual(sdk.path_to_analyzer, '/foo/bar/bin/dartanalyzer')

    def tearDown(self):
        self.view.close()
