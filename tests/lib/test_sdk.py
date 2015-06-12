# Copyright (c) 2014, Guillermo López-Anglada. Please see the AUTHORS file for details.
# All rights reserved. Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.)

from unittest import mock
import os
import unittest

import sublime

from Dart.lib.sdk import FlexiblePlatformSettingReader


class TestFlexiblePlatformSettingsReader(unittest.TestCase):
    def testCanRetrieveSimpleSetting(self):
        getter = FlexiblePlatformSettingReader(name='doesnt_matter')
        getter.get_setting = mock.Mock()
        getter.get_setting.return_value = 'some/path'

        class dummy:
            my_path = getter

        d = dummy()

        self.assertEqual('some/path', d.my_path)

    def testCanRetrievePlatformSetting(self):
        getter = FlexiblePlatformSettingReader(name='doesnt_matter')
        getter.get_setting = mock.Mock()

        data = {
            'windows': 'some/windows/path',
            'linux': 'some/linux/path',
            'osx': 'some/osx/path',
        }

        getter.get_setting.return_value = data

        class dummy:
            my_path = getter

        d = dummy()

        self.assertEqual(data[sublime.platform()], d.my_path)

    def testThrowsIfPlatformUnknown(self):
        raise NotImplementedError
    def testThrowsIfValidationFailed(self):
        raise NotImplementedError
    def testCanPassValidation(self):
        raise NotImplementedError
