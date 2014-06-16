import sublime_plugin

import webbrowser

from .lib.sdk import SDK


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
