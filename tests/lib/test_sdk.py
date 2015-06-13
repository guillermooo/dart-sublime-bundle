# Copyright (c) 2014, Guillermo López-Anglada. Please see the AUTHORS file for details.
# All rights reserved. Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.)

from unittest import mock
import os
import unittest

import sublime

from Dart.lib.error import FatalConfigError
from Dart.lib.sdk import DartSdkPathSetting
from Dart.lib.sdk import FlexibleSetting


class TestFlexiblePlatformSettingsReader(unittest.TestCase):
    def testCanRetrieveSimpleSetting(self):
        getter = DartSdkPathSetting(name='doesnt_matter')
        getter.get = mock.Mock()
        getter.validate_sdk_path = mock.Mock()
        getter.get.return_value = 'some/path'
        getter.validate_sdk_path = lambda x: x

        class dummy:
            my_path = getter

        d = dummy()

        self.assertEqual('some/path', d.my_path)

    def testCanRetrievePlatformSetting(self):
        getter = DartSdkPathSetting(name='doesnt_matter')
        getter.get = mock.Mock()
        getter.validate_sdk_path = mock.Mock()

        data = {
            'windows': 'some/windows/path',
            'linux': 'some/linux/path',
            'osx': 'some/osx/path',
        }

        getter.get.return_value = data
        getter.validate_sdk_path = lambda x: x

        class dummy:
            my_path = getter

        d = dummy()

        self.assertEqual(data[sublime.platform()], d.my_path)

    def testThrowsIfPlatformUnknown(self):
        getter = DartSdkPathSetting(name='doesnt_matter')
        getter.get = mock.Mock()
        getter.validate_sdk_path = mock.Mock()

        data = {
                'windows': 'some/windows/path',
                'linux': 'some/linux/path',
                'osx': 'some/osx/path',
            }

        getter.get.return_value = data
        getter.validate_sdk_path = lambda x: x

        with mock.patch('sublime.platform') as mocked:
            mocked.return_value = "winux"

            class dummy:
                my_path = getter

            d = dummy()

            self.assertRaises(ValueError, lambda: d.my_path)

    def testThrowsIfValidationFailed(self):
        getter = DartSdkPathSetting(name='doesnt_matter', expected_type=str)
        getter.get = mock.Mock()

        getter.get.return_value = 10

        class dummy:
            my_path = getter

        d = dummy()

        self.assertRaises(AssertionError, lambda: d.my_path)

    def testThrowsIfSdkPathDoesNotValidate(self):
        getter = DartSdkPathSetting(name='doesnt_matter')
        getter.get = mock.Mock()

        getter.get.return_value = 'xxx'

        class dummy:
            my_path = getter

        d = dummy()

        self.assertRaises(FatalConfigError, lambda: d.my_path)

    def testCanPassValidation(self):
        getter = DartSdkPathSetting(name='doesnt_matter', expected_type=str)
        getter.get = mock.Mock()
        getter.validate_sdk_path = mock.Mock()

        getter.get.return_value = 'diez'
        getter.validate_sdk_path = lambda x: x

        class dummy:
            my_path = getter

        d = dummy()

        self.assertEqual('diez', d.my_path)

    def testCanImplementPostValidate(self):
        getter = DartSdkPathSetting(name='doesnt_matter')
        getter.get = mock.Mock()
        getter.validate_sdk_path = mock.Mock()
        getter.post_validate = mock.Mock()

        getter.get.return_value = 'chorizo'
        getter.validate_sdk_path = lambda x: x
        getter.post_validate.return_value = 'morcilla'

        class dummy:
            my_setting = getter

        d = dummy()

        self.assertEqual('morcilla', d.my_setting)

    def testCanReturnDefaultValue(self):
        getter = DartSdkPathSetting(name='doesnt_matter', default="fabada")
        getter.get = mock.Mock()
        getter.validate_sdk_path = mock.Mock()

        getter.get.return_value = None
        getter.validate_sdk_path = lambda x: x

        class dummy:
            my_path = getter

        d = dummy()

        self.assertEqual('fabada', d.my_path)
