import sublime
import sublime_plugin
import os
import subprocess
import threading
import re


class DartLint(sublime_plugin.EventListener):
    def __init__(self, *args, **kwargs):
        sublime_plugin.EventListener.__init__(self, *args, **kwargs)
        print("Dart lint active.")

    def on_post_save(self, view):
        fileName = view.file_name()
        isDart = fileName.find('.dart')

        if isDart == -1:
            return
        # now we are pretty sure that this a .dart file
        print("Dart lint: Running dartanalyzer on ", fileName)
        # run dartanalyzer in its own thread
        RunDartanalyzer(view, fileName)


def RunDartanalyzer(view, fileName):
    settings = view.settings()
    dartsdk_path = settings.get('dartsdk_path')

    if dartsdk_path:
        DartLintThread(view.window(), dartsdk_path, fileName).start()


class DartLintThread(threading.Thread):
    def __init__(self, window, dartsdk_path, fileName):
        super(DartLintThread, self).__init__()
        self.daemon = True
        self.window = window
        self.dartsdk_path = dartsdk_path
        self.fileName = fileName

    def get_startupinfo(self):
        if IsWindows():
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE
            return startupinfo
        return subprocess.STARTUPINFO()

    def run(self):
        # working_directory = os.path.dirname(self.fileName)
        analyzer_path = os.path.join(self.dartsdk_path, 'bin', 'dartanalyzer')
        if IsWindows():
            analyzer_path += '.bat'

        print('\ndartanalyzer %s\n' % self.fileName)
        proc = subprocess.Popen([analyzer_path, self.fileName],
                                stdout=subprocess.PIPE)
        while not proc.poll():
            # Wait for it...
            pass

        pattern = re.compile(r'^(?:((?P<error>(\[error\]))|(?P<warning>(\[warning\]))))\s(?P<message>.*)\s\((?P<file>.*)\,\sline\s(?P<line>\d*)\, col\s(?P<col>\d*)')

        lines = proc.stdout.read().decode("utf-8").split('\n')

        lines_out = ''
        for line in lines:
            line_groups = pattern.match(line)

            if line_groups is not None:
                if line_groups.group('file') != self.fileName:
                    # output is for a different file
                    continue
                if line_groups.group('error'):
                    lines_out += 'Error '
                elif line_groups.group('warning'):
                    lines_out += 'Warning '
                lines_out += 'on line %s, col %s: %s\n' % (line_groups.group('line'), line_groups.group('col'), line_groups.group('message'))

        self.output = lines_out
        print(self.output)
        # annoying: sublime.message_dialog(self.output)
        # Output to a popup
        # Mark the gutter
        # Underline Errors / Warnings


def IsWindows():
    return sublime.platform() == 'windows'
