import sublime
import sublime_plugin

from Dart.lib.sdk import SDK


class DartCheckConfigCommand(sublime_plugin.WindowCommand):
    '''Displays current configuration information.
    '''
    def run(self):
        sdk = SDK()
        report = self.window.new_file()
        report.set_name('Dart - Configuration Report')
        report.set_scratch(True)

        self.append(report, 'Sublime Text Information\n')
        self.append(report, '=' * 80)
        self.add_newline(report)
        self.append(report, 'version: ')
        self.append(report, sublime.version())
        self.append(report, ' (')
        self.append(report, sublime.channel())
        self.append(report, ' channel)')
        self.add_newline(report)
        self.append(report, 'platform: ')
        self.append(report, sublime.platform())
        self.add_newline(report)
        self.append(report, 'architecture: ')
        self.append(report, sublime.arch())
        self.add_newline(report)
        self.add_newline(report)

        self.append(report, 'Dart SDK Information\n')
        self.append(report, '=' * 80)
        self.add_newline(report)

        self.append(report, 'version: ')
        dart_version = sdk.check_version()
        self.append(report, dart_version)

        self.append(report, 'path: ')
        self.append(report, sdk.path)
        self.add_newline(report)
        self.add_newline(report)

        self.append(report, 'Project Information\n')
        self.append(report, '=' * 80)
        self.add_newline(report)
        self.append(report, '<not implemented>')
        self.add_newline(report)

    def add_newline(self, view):
        self.append(view, '\n')

    def append(self, view, text):
       view.run_command('append', {'characters': text})

