import unittest

import sublime

from Dart.lib.analyzer.request_manager import RequestIdManager


class Test_RequestIdManager(unittest.TestCase):

    def testCanIncreaseId(self):
        rm = RequestIdManager()
        _id1 = rm.new_id(self.view, None)
        _id2 = rm.new_id(self.view, None)
        _id3 = rm.new_id(self.view, None)
        self.assertEqual(_id1, '0')
        self.assertEqual(_id2, '1')
        self.assertEqual(_id3, '2')

    def testIdsWrapAround(self):
        rm = RequestIdManager()
        rm._id = 1 << 10
        _id = rm.new_id(self.view, None)
        self.assertEqual(_id, '0')

    def testCanRetrieveResponseType(self):
        rm = RequestIdManager()
        _id = rm.new_id(self.view, int)
        self.assertEqual(rm.get_response_type(self.view, '0'), int)

    def testValidationCanSucceed(self):
        rm = RequestIdManager()
        _id = rm.new_id(self.view, int)
        self.assertTrue(rm.validate(self.view, {'id': '0'}))

    def testValidateCanFail(self):
        rm = RequestIdManager()
        _id = rm.new_id(self.view, int)
        self.assertFalse(rm.validate(self.view, {'id': '1'}))

    def setUp(self):
        self.view = sublime.active_window().new_file()

    def tearDown(self):
        self.view.close()
