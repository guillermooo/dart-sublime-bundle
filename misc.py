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
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def user_file(self):
        return os.path.join(sublime.packages_path(),
                            'User/Dart.sublime-settings')

    def run(self, kind='user'):
        if kind != 'user':
            sublime.status_message('Dart: Not supported settings kind: {0}'
                .format(kind))
            _logger.error('Not supported settings kind: %s', kind)
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
