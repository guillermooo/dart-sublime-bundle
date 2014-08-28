import sublime
import sublime_plugin


class DartBuildCommandBase(sublime_plugin.WindowCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def execute(self, **kwargs):
        self.window.run_command('dart_exec', kwargs)
