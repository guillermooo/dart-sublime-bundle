'''Base commands.
'''
import sublime_plugin

import os

from Dart.lib.dart_project import DartProject
from Dart.lib.panels import ErrorPanel


# TODO(guillermooo): try adding is_active or whatever method returns
# availability status.
class PolymerCommand(sublime_plugin.WindowCommand):
    # TODO(guillermooo): generalize class so it can run any polymer command.

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, message):
        '''
        @message
          The message that will be displayed to the user when collecting their
            input.
        '''
        v = self.window.active_view()

        project = DartProject.from_path(v.file_name())
        if not project:
            # TODO(guillermooo): add logging.
            info = ErrorPanel()
            info.write('Could not locate pubspec.yaml file for: {}\n'
                                                    .format(v.file_name()))
            info.write('Cannot run Polymer command.')
            info.show()
            return

        if not project.has_dependency('polymer'):
            # TODO(guillermooo): add logging.
            info = ErrorPanel()
            info.write("Polymer isn't a dependency in this project.")
            info.write('Cannot run Polymer command.')
            info.show()
            return

        if not project.path_to_web:
            # TODO(guillermooo): add logging
            project.make_top_level_dir('web')

        self.window.show_input_panel(message, '',
                                     self.on_done, None, None)

    def get_target_path(self, view):
        '''Returns the path in which the generated files belong.
        '''
        project = DartProject.from_path(view.file_name())

        target_path = project.path_to_web
        if project.is_path_under(project.path_to_web, view.file_name()):
            target_path = os.path.dirname(view.file_name())

        return target_path

    def execute(self, shell_cmd, working_dir):
        # TODO(guillermooo): we cannot access the ouput panel used by exec.
        # This means we cannot print friendlier status output. Replace exec
        # with our own async process execution so that we can control its
        # output panel.
        self.window.run_command('exec', {
            'shell_cmd': shell_cmd,
            'working_dir': working_dir
            })
