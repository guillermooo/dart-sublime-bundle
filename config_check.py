# Copyright (c) 2014, Guillermo López-Anglada. Please see the AUTHORS file for details.
# All rights reserved. Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.)

import sublime
import sublime_plugin

import pprint

from Dart.lib.sdk import SDK
from Dart.lib.pub_package import PubspecFile


class DartCheckConfigCommand(sublime_plugin.WindowCommand):
    '''Displays current configuration information.
    '''
    def run(self):
        sdk = SDK()
        previous_view = self.window.active_view()
        report = self.window.new_file()
        report.set_name('Dart - Configuration Report')
        report.set_scratch(True)

        self.append(report, 'Sublime Text Information\n')
        self.append(report, '=' * 80)
        self.add_newline(report)
        self.append(report, 'version: ')
        self.append(report, sublime.version())
        self.append(report, ' (')
        self.append(report, sublime.channel())
        self.append(report, ' channel)')
        self.add_newline(report)
        self.append(report, 'platform: ')
        self.append(report, sublime.platform())
        self.add_newline(report)
        self.append(report, 'architecture: ')
        self.append(report, sublime.arch())
        self.add_newline(report)
        self.add_newline(report)

        self.append(report, 'Dart SDK Information\n')
        self.append(report, '=' * 80)
        self.add_newline(report)

        self.append(report, 'version: ')
        dart_version = sdk.check_version()
        self.append(report, dart_version)
        self.add_newline(report)

        self.append(report, 'Dart Package Settings\n')
        self.append(report, '=' * 80)
        self.add_newline(report)
        self.append(report, 'dart_sdk_path: ')
        self.append(report, sdk.path)
        self.add_newline(report)
        self.append(report, 'dart_dartium_path: ')
        self.append(report, sdk.path_to_dartium)
        self.add_newline(report)
        self.append(report, 'dart_user_browsers: ')
        self.add_newline(report)
        self.append(report, pprint.pformat(sdk.user_browsers))
        self.add_newline(report)
        self.add_newline(report)

        self.append(report, 'Project Information\n')
        self.append(report, '=' * 80)
        self.add_newline(report)
        if previous_view:
            try:
                self.append(
                    report,
                    str(PubspecFile.from_path(
                                            previous_view.file_name()).path)
                    )
            except Exception as e:
                self.append(report, 'No pubspec found\n')

        self.add_newline(report)

    def add_newline(self, view):
        self.append(view, '\n')

    def append(self, view, text):
       view.run_command('append', {'characters': text})

