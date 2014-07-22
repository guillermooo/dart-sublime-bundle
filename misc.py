import sublime_plugin
import sublime

import webbrowser
import os

from . import PluginLogger
from .lib.sdk import SDK


_logger = PluginLogger(__name__)


class OpenBrowser(sublime_plugin.WindowCommand):
    """Opens API reference in default browser.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, url):
        webbrowser.open_new_tab(url)


class OpenDartEditor(sublime_plugin.TextCommand):
    """Opens the Dart Editor.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, edit):
        sdk = SDK()
        sdk.start_editor()


class OpenDartSettings(sublime_plugin.WindowCommand):
    """Opens Dart settings files.

    Default settings (that is, Packages/Dart/Support/Dart.sublime-settings)
    are displayed as a read-only view not meant for editing.

    User settings (that is, Packages/User/Dart.sublime-settings) are opened
    as a regular view and are meant for editing.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def user_file(self):
        return os.path.join(sublime.packages_path(),
                            'User/Dart.sublime-settings')

    def open_default(self):
        """Prints the default settings for Dart to a read-only view. The user
        should not edit their settings here, but use the 'user' file instead.
        """
        setts = sublime.load_resource(
            'Packages/Dart/Support/Dart.sublime-settings')

        v = self.window.new_file()
        v.run_command('append', {"characters": setts.replace('\r', '')})
        v.set_name('Dart Settings – Default (read-only)')
        # TODO(guillermooo): ST should detect that this is a JSON file by
        # looking at the extension, but it isn't the case. Check with
        # Sublime HQ. For now, set the syntax manually.
        v.set_syntax_file('Packages/JavaScript/JSON.tmLanguage')
        v.set_scratch(True)
        v.set_read_only(True)

    def run(self, kind='user'):
        """
        @kind: Any of (user, default).
        """
        if kind == 'default':
            _logger.debug('Opening default settings for viewing only.')
            self.open_default()
            return

        if kind != 'user':
            _logger.error('Unsupported settings type: %s', kind)
            return

        if not os.path.exists(self.user_file):
            _logger.debug('Creating user settings file at: %s',
                        self.user_file)
            with open(self.user_file, 'w') as f:
                f.write('{\n\t\n}')

        try:
            self.window.open_file(self.user_file)
        except OSError as e:
            _logger.error('Unexpected error while trying to open %s',
                self.user_file)
            _logger.error(e)
            _logger.error('=' * 80)
