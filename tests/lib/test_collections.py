# Copyright (c) 2014, Guillermo López-Anglada. Please see the AUTHORS file for details.
# All rights reserved. Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.)

import unittest
import os

from Dart.lib.collections import CircularArray


class Test_CircularList(unittest.TestCase):
    def testCanInstantiate(self):
        ca = CircularArray(list(range(0, 5)))
        self.assertEqual(len(ca), 5)

    def testForward(self):
        ca = CircularArray(list(range(0, 5)))
        self.assertEqual(ca.forward(), 0)
        self.assertEqual(ca.forward(), 1)
        self.assertEqual(ca.forward(), 2)
        self.assertEqual(ca.forward(), 3)
        self.assertEqual(ca.forward(), 4)
        self.assertEqual(ca.forward(), 0)

    def testBackward(self):
        ca = CircularArray(list(range(0, 5)))
        self.assertEqual(ca.backward(), 4)
        self.assertEqual(ca.backward(), 3)
        self.assertEqual(ca.backward(), 2)
        self.assertEqual(ca.backward(), 1)
        self.assertEqual(ca.backward(), 0)
        self.assertEqual(ca.backward(), 4)

    def xtestBidirectionality(self):
        ca = CircularArray(list(range(0, 5)))
        self.assertEqual(ca.backward(), 4)
        self.assertEqual(ca.forward(), 0)
        self.assertEqual(ca.backward(), 4)
        self.assertEqual(ca.forward(), 0)
        self.assertEqual(ca.forward(), 1)
        self.assertEqual(ca.forward(), 2)
        self.assertEqual(ca.forward(), 3)
        self.assertEqual(ca.forward(), 4)
        self.assertEqual(ca.backward(), 3)
        self.assertEqual(ca.backward(), 2)
        self.assertEqual(ca.backward(), 1)
        self.assertEqual(ca.backward(), 0)
