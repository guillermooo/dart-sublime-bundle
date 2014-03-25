import sublime
import sublime_plugin
import os
import subprocess
import threading
import re
import pprint


class DartLint(sublime_plugin.EventListener):
    def __init__(self, *args, **kwargs):
        sublime_plugin.EventListener.__init__(self, *args, **kwargs)
        print("Dart lint active.")

    def on_post_save(self, view):
        fileName = view.file_name()
        isDart = fileName.find('.dart')

        if isDart == -1:
            return

        print("Dart lint: Running dartanalyzer on ", fileName)
        # run dartanalyzer in its own thread
        RunDartanalyzer(view, fileName)


def RunDartanalyzer(view, fileName):
    settings = view.settings()
    dartsdk_path = settings.get('dartsdk_path')

    if dartsdk_path:
        DartLintThread(view, dartsdk_path, fileName).start()


class DartLintThread(threading.Thread):
    def __init__(self, view, dartsdk_path, fileName):
        super(DartLintThread, self).__init__()
        self.daemon = True
        # self.view = view
        self.window = view.window()
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

        msg_pattern = re.compile(
            r'^(?:((?P<error>(\[error\]))|(?P<warning>(\[warning\]))))\s(?P<message>.*)\s\((?P<file>.*)\,\sline\s(?P<line>\d*)\, col\s(?P<col>\d*)')
        culprit_pattern = re.compile(
            r'^.+\'(?:(?P<culprit>(.+)))\'')

        # TODO: use proper locale instead of "utf-8"
        lines = proc.stdout.read().decode("utf-8").split('\n')

        # Collect data needed to generate error messages
        lint_data = []
        lines_out = ''
        for line in lines:
            line_out = ''
            line_data = {}
            line_groups = msg_pattern.match(line)

            if line_groups is not None:
                if line_groups.group('file') != self.fileName:
                    # output is for a different file
                    continue
                if line_groups.group('error'):
                    line_out += 'Error '
                    line_data['type'] = 'error'
                elif line_groups.group('warning'):
                    line_out += 'Warning '
                    line_data['type'] = 'warning'
                line_out += 'on line %s, col %s: %s\n' % \
                    (line_groups.group('line'),
                     line_groups.group('col'),
                     line_groups.group('message'))

                line_data['col'] = line_groups.group('col')
                line_data['line'] = line_groups.group('line')
                line_data['msg'] = line_groups.group('message')
                line_data['lint_out'] = line_out
                line_data['culprit'] = ''

                # Get the culprit:
                culp_group = culprit_pattern.match(line_groups.group('message'))
                if culp_group is not None:
                    line_data['culprit'] = culp_group.group('culprit')

                lines_out += line_out
                lint_data.append(line_data)

        if lines_out is '':
            self.output = None
            print('No errors.')
        else:
            self.output = lint_data
            pp = pprint.PrettyPrinter(indent=4)
            # Print to the console
            pp.pprint(self.output)
            print('\n' + lines_out)
            # Output to a popup
            PopupErrors(self.window, self.output)
            # Mark the gutter
            # Underline Errors / Warnings


def PopupErrors(window, ErrorData):
    # Process data into a list of errors
    dd_list = []
    for entry in ErrorData:
        dd_list.append(entry['lint_out'])
    DisplayInQuickPanel(window, dd_list, GotoError, GotoError)


def GotoError(index):
    pass


def MarkGutter(view, line_num):
    pass


def SelectText(view, line_num, target):
    # Should return a range obj I think
    pass


def Underline(view, line_num, u_type, target):
    pass


def DisplayInQuickPanel(window, dd_list, select_fn, highlight_fn):
    window.show_quick_panel(
        dd_list,
        on_select=select_fn,
        on_highlight=highlight_fn)


def IsWindows():
    return sublime.platform() == 'windows'
