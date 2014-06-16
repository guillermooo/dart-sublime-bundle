import sublime

from Dart.lib.plat import is_windows
from Dart.lib.plat import to_platform_path

from subprocess import call
from os.path import join
from os.path import realpath
from os.path import exists


class SDK(object):
    """Wraps the Dart sdk.
    """

    def __init__(self, path=None):
        self.path = path
        if self.path is None:
            setts = sublime.active_window().active_view().settings()
            self.path = setts.get('dartsdk_path')

    def start_editor(self, file_name=None, row=None, col=None):
        """Launches the Dart Editor.

        @file_name
          File to open in the editor.
        @row
          Text row to move the caret to.
        @col
          Column to move the caret to.
        """
        assert not any((file_name, row, col)), 'not implemented'
        bin_name = to_platform_path('DartEditor', '.exe')

        path = realpath(join(self.path, '../{0}'.format(bin_name)))
        if not exists(path):
            raise IOError('cannot find DartEditor binary')

        call([path])

    @property
    def path_to_dart(self):
        """Returns path to dart interpreter.
        """
        bin_name = to_platform_path('dart', '.exe')
        return realpath(join(self.path, bin_name))
