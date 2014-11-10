# Copyright (c) 2014, Guillermo López-Anglada. Please see the AUTHORS file for details.
# All rights reserved. Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.)

import sublime_plugin
import sublime

import webbrowser
import os

from Dart.sublime_plugin_lib import PluginLogger
from Dart.lib.sdk import SDK
from Dart.sublime_plugin_lib.panels import OutputPanel


_logger = PluginLogger(__name__)


# TODO(guillermooo): we probably don't need a new command; ST already includes
# one by default.
class DartOpenBrowserCommand(sublime_plugin.WindowCommand):
    """Opens API reference in default browser.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, url):
        webbrowser.open_new_tab(url)


class DartOpenSettingsCommand(sublime_plugin.WindowCommand):
    """Opens Dart settings files.

    a) Default settings (that is, Packages/Dart/Support/Dart - Plugin Settings.sublime-settings).
    b) User settings (that is, Packages/User/Dart - Plugin Settings.sublime-settings).
    c) Dart file type settings (that is, Packages/User/Dart.sublime-settings)

    (a) is read-only and users should not rely on it, as it can be overwritten
        by ST or this plugin at any time withouth notice. Provides defaults and
        documentation.
    (b) user-editable version of (a). This is where users should store their
        settings.
    (c) Controls aspects closely related to .dart files: white space, tab size,
        etc.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def file_type_settings(self):
        '''Returns the full path to the Dart fyle type settings file.

        Note: ST accepts file type settings files in many locations, so
        conflicts may arise. For example, if the user had both:
          - Packages/User/Dart.sublime-settings, and
          - Packages/User/SomeSubDir/Dart.sublime-settings
        '''
        path = os.path.join(sublime.packages_path(),
                            'User/Dart.sublime-settings')
        if not os.path.exists(path):
            _logger.debug('Creating user settings file at: %s', path)
            with open(path, 'w') as f:
                f.write('{\n\t\n}')
        return path

    def run(self, kind='user', scope='global'):
        """
        @kind:
          Any of (user, default).

        @scope:
          Any of (global, file_type).
        """
        if kind == 'default':
            if scope == 'global':
                _logger.debug('Opening default settings for viewing only.')
                self.open_default()
                return
            _logger(
                'Default file type settings file requested. Such file does not exist.')
            return

        if kind != 'user':
            _logger.error('Unsupported settings type: %s', kind)
            return

        # User settings (Packages/User/*.sublime-settings)

        if scope == 'file_type':
            try:
                self.window.open_file(self.file_type_settings)
                return
            except OSError as e:
                _logger.error(
                    'Unexpected error while trying to open User file type settings')
                _logger.error(e)
                _logger.error('=' * 80)
                return

        self.window.run_command('open_file', {
            "file": "${packages}/User/Dart - Plugin Settings.sublime-settings"
            })

    def open_default(self):
        """Prints the default settings for Dart to a read-only view. The user
        should not edit their settings here, but use the 'User' version instead.
        """
        setts = sublime.load_resource(
            'Packages/Dart/Support/Dart - Plugin Settings.sublime-settings')

        v = self.window.new_file()
        v.run_command('append', {'characters': setts.replace('\r', '')})
        v.set_name('Dart Settings - Default (read-only)')
        # TODO(guillermooo): ST should detect that this is a JSON file by
        # looking at the extension, but it isn't the case. Check with
        # Sublime HQ. For now, set the syntax manually.
        v.set_syntax_file('Packages/JavaScript/JSON.tmLanguage')
        v.set_scratch(True)
        v.set_read_only(True)


class InsertLineTerminator(sublime_plugin.TextCommand):
    def run(self, edit):
        meta = self.view.meta_info('shellVariables', 0)
        if not meta:
            return

        lt = ''
        for var in meta:
            if var['name'] == 'TM_LINE_TERMINATOR':
                lt = var['value']
                break
        if not lt:
            return

        eol = self.view.line(self.view.sel()[0].b).b
        s = self.view.substr(self.view.line(eol))
        try:
            lt_pos = s.rindex(lt)
        except ValueError:
            self.view.insert(edit, eol, lt)
