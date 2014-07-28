import sublime

from Dart.lib.plat import is_windows
from Dart.lib.plat import to_platform_path
from Dart.lib.path import find_in_path
from Dart.lib.internal import cached_property
from Dart import PluginLogger

from subprocess import Popen
from subprocess import TimeoutExpired
from os.path import join
from os.path import realpath
from os.path import exists
import os


_logger = PluginLogger(__name__)


class SDK(object):
    """Wraps the Dart sdk.
    """

    def __init__(self, path=None):
        # TODO(guillermooo): What if the user passes the wrong path?
        if path is not None:
            self.__dict__['path_to_sdk'] = path

    @cached_property
    def path_to_sdk(self):
        return find_in_path('dart', '.exe')

    def start_editor(self, funiile_name=None, row=None, col=None):
        """Launches the Dart Editor.

        @file_name
          File to open in the editor.
        @row
          Text row to move the caret to.
        @col
          Column to move the caret to.
        """
        if not self.path_to_sdk:
            _logger.info('could not locate the dart sdk')
            return

        assert not any((file_name, row, col)), 'not implemented'
        bin_name = to_platform_path('DartEditor', '.exe')

        # TODO: Add path_to_editor property.
        path = realpath(join(self.path_to_sdk, '../{0}'.format(bin_name)))
        if not exists(path):
            print("Dart: Error - Cannot find Dart Editor binary.")
            print("              Is the Dart Editor installed?")
            _logger.info('cannot find Dart Editor binary')
            _logger.info('using path to Dart SDK: %s', self.path_to_sdk)
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
        if not self.path_to_sdk:
            _logger.info('could not locate dart sdk')
            return

        bin_name = to_platform_path('dart', '.exe')
        return realpath(join(self.path_to_sdk, 'bin', bin_name))
