# Copyright (c) 2014, Guillermo López-Anglada. Please see the AUTHORS file for details.
# All rights reserved. Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.)

import unittest
import os

from Dart.lib.collections import CircularArray


class Test_CompletionsList(unittest.TestCase):
    def testHasLength(self):
        ca = CircularArray([0, 1, 2, 3, 4])
        self.assertEqual(len(ca), 5)

    def testIsCircular(self):
        ca = CircularArray([0, 1, 2, 3, 4])
        self.assertEqual(next(ca), 0)
        self.assertEqual(next(ca), 1)
        self.assertEqual(next(ca), 2)
        self.assertEqual(next(ca), 3)
        self.assertEqual(next(ca), 4)
        self.assertEqual(next(ca), 0)
        self.assertEqual(next(ca), 1)
        self.assertEqual(next(ca), 2)
        self.assertEqual(next(ca), 3)
        self.assertEqual(next(ca), 4)
        self.assertEqual(next(ca), 0)
