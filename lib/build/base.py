import sublime
import sublime_plugin

from Dart.lib.event import EventSource


class DartBuildCommandBase(sublime_plugin.WindowCommand, EventSource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def execute(self, **kwargs):
        self.window.run_command('dart_exec', kwargs)
