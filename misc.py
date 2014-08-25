import sublime_plugin
import sublime

import webbrowser
import os

from . import PluginLogger
from .lib.sdk import SDK


_logger = PluginLogger(__name__)


class OpenBrowserCommand(sublime_plugin.WindowCommand):
    """Opens API reference in default browser.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, url):
        webbrowser.open_new_tab(url)


class OpenDartEditorCommand(sublime_plugin.TextCommand):
    """Opens the Dart Editor.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, edit):
        sdk = SDK()
        sdk.start_editor()


class DartOpenSettingsCommand(sublime_plugin.WindowCommand):
    """Opens Dart settings files.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def user_file(self):
        return os.path.join(sublime.packages_path(),
                            'User/Dart.sublime-settings')

    def run(self, kind='user'):
        """
        @kind: Any of (user, default).
        """
        if kind != 'user':
            _logger.error('Unsupported settings type: %s', kind)
            return

        if not os.path.exists(self.user_file):
            _logger.debug('creating user settings file at: %s',
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
