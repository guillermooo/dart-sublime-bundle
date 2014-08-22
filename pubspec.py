import sublime
import sublime_plugin

import os


PUBSPEC_TPL = '''# https://www.dartlang.org/tools/pub/pubspec.html

name: ${1:your_package_name}
version: ${2:0.1.0}
'''


class NewPubspecCommand(sublime_plugin.WindowCommand):
    '''Adds a pubspec file.
    '''
    def run(self):
        old_view = sublime.active_window().active_view()

        new_view = self.window.new_file()
        new_view.settings().set('syntax', 'Packages/YAML/YAML.tmLanguage')

        if old_view and old_view.file_name():
            new_view.settings().set('default_dir',
                                    os.path.dirname(old_view.file_name()))

        new_view.run_command('insert_snippet', {'contents': PUBSPEC_TPL})
