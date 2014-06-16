import sublime_plugin

import webbrowser


class OpenBrowser(sublime_plugin.WindowCommand):
    def run(self, url):
        webbrowser.open_new_tab(url)
