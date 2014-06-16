import sublime

from Dart.lib.plat import is_windows
from Dart.lib.plat import to_platform_path
from Dart import PluginLogger

from subprocess import Popen
from subprocess import TimeoutExpired
from os.path import join
from os.path import realpath
from os.path import exists


_logger = PluginLogger(__name__)


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

        # TODO: Add path_to_editor property.
        path = realpath(join(self.path, '../{0}'.format(bin_name)))
        if not exists(path):
            print("Dart: Error - Cannot find Dart Editor binary.")
            print("            | Is `dartsdk_path` set?")
            print("            | Is the Dart Editor installed?")
            _logger.info('cannot find Dart Editor binary')
            _logger.info('using path to Dart SDK: %s', self.path)
            return

        # Don't wait for process to terminate so we don't block ST.
        proc = Popen([path])
        try:
            # Just see if we got an error sort of quickly.
            proc.wait(.500)
        except TimeoutExpired:
            pass
        else:
            if proc.returncode != 0:
                _logger.error('Dart Editor exited with error code %d', proc.returncode)

    @property
    def path_to_dart(self):
        """Returns path to dart interpreter.
        """
        bin_name = to_platform_path('dart', '.exe')
        return realpath(join(self.path, 'bin', bin_name))
