import sublime

import unittest
import os
from subprocess import check_output

from Dart.lib.path import find_in_path


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
