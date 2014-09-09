import sublime
import sublime_plugin

import os

from Dart.lib.pub_package import DartProject
from Dart.lib.base_cmds import PolymerCommand
from Dart import PluginLogger


_logger = PluginLogger(__name__)


# TODO(guillermooo): try adding is_active or whatever method returns
# availability status.
class DartGeneratePolymerElementCommand(PolymerCommand):
    '''
    pub run polymer:new_element
    '''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self):
        super().run('Element Name:')

    def on_done(self, name):
        view = self.window.active_view()
        project = DartProject.from_path(view.file_name())
        cmd = "pub run polymer:new_element {} -o \"{}\""

        # TODO(guillermooo): we cannot access the ouput panel used by exec.
        # This means we cannot print friendlier status output. Replace exec
        # with our own async process execution so that we can control its
        # output panel.
        self.execute(cmd.format(name, self.get_target_path(view)),
                     project.pubspec.parent)


# TODO(guillermooo): try adding is_active or whatever method returns
# availability status.
class DartAddPolymerEntryPointCommand(PolymerCommand):
    '''
    pub run polymer:new_entry
    '''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self):
        super().run('Entry Point Name:')

    def on_done(self, name):
        view = self.window.active_view()
        project = DartProject.from_path(view.file_name())
        cmd = "pub run polymer:new_entry {}".format(name)

        # TODO(guillermooo): we cannot access the ouput panel used by exec.
        # This means we cannot print friendlier status output. Replace exec
        # with our own async process execution so that we can control its
        # output panel.
        self.execute(cmd, project.pubspec.parent)
