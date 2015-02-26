# Copyright (c) 2014, Guillermo López-Anglada. Please see the AUTHORS file for details.
# All rights reserved. Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.)

import sublime
import sublime_plugin

from os.path import join
import os
import subprocess
import threading

from Dart.lib import ga
from Dart.lib.build.base import DartBuildCommandBase
from Dart.lib.event import EventSource
from Dart.lib.path import is_pubspec
from Dart.lib.path import is_view_dart_script
from Dart.lib.pub_package import PubPackage
from Dart.lib.sdk import SDK
from Dart.sublime_plugin_lib import PluginLogger
from Dart.sublime_plugin_lib.panels import OutputPanel
from Dart.sublime_plugin_lib.plat import is_windows
from Dart.sublime_plugin_lib.plat import supress_window
from Dart.sublime_plugin_lib.sublime import after


_logger = PluginLogger(__name__)


class PubspecListener(sublime_plugin.EventListener):
    def __init__(self, *args, **kwargs):
        sublime_plugin.EventListener.__init__(self, *args, **kwargs)

    def on_post_save(self, view):
        if not is_pubspec(view):
            return

        # XXX: This event handler seems to run twice at least on Windows. This
        #      apparently causes an error in pub. Issue has been reported to
        #      SublimeHq just in case.
        _logger.debug("running pub with %s", view.file_name())
        view.window().run_command('dart_pub_get', {
            'file_name': view.file_name()
            })


# TODO(guillermooo): unify Pub commands.
class DartPubGetCommand(DartBuildCommandBase):

    def run(self, file_name=None, command='get'):
        if command == 'get':
            self.dart_pub_get(file_name)

    def dart_pub_get(self, path_to_pubspec):
        path_to_pubspec = path_to_pubspec or self.window.active_view().file_name()
        if not path_to_pubspec:
            _logger.error('no pubspec specified for "pub get"')
            return

        package = PubPackage.from_path(path_to_pubspec)
        if not package:
            _logger.info("can't 'pub get' if project hasn't a pubspec.yaml file")
            return
        path_to_pubspec = package.pubspec.path

        sdk = SDK()

        if not sdk.path_to_pub:
            _logger.debug("`sdk.path_to_pub` missing; aborting pub")
            return

        self.execute(**{'working_dir': os.path.dirname(path_to_pubspec),
                        'cmd': [sdk.path_to_pub, 'get'],
                        'preamble': 'Running pub get...\n',
                        })


# We need a command because we want to use analytics. We can't simply use a
# .sublime-build file.
class DartPubBuildCommand(DartBuildCommandBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_event_handler(EventSource.ON_PUB_BUILD,
                               DartPubBuildCommand.on_pub_build)

    def run(self, working_dir=None, **kwargs):
        assert working_dir is not None, 'wrong call'
        self.raise_event(self, EventSource.ON_PUB_BUILD)
        sdk = SDK()
        self.execute(**{'working_dir': working_dir,
                        'cmd': [sdk.path_to_pub, 'build'],
                        'preamble': 'Running pub build...\n',
                        })

    @classmethod
    def on_pub_build(self, *args, **kwargs):
        ga.Event(category='actions',
                 action='on_pub_build',
                 label='Running "pub build" command',
                 value=1,
                 ).send()
