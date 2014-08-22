import sublime

from subprocess import Popen
from subprocess import STDOUT
from subprocess import check_output
from subprocess import TimeoutExpired
from os.path import join
from os.path import realpath
from os.path import exists
import os

from Dart import PluginLogger
from Dart.lib.filter import TextFilter
from Dart.lib.internal import cached_property
from Dart.lib.path import find_in_path
from Dart.lib.plat import is_windows
from Dart.lib.plat import supress_window
from Dart.lib.plat import to_platform_path


_logger = PluginLogger(__name__)


class SDK(object):
    """Wraps the Dart sdk.
    """

    def check(self):
        '''Reports whether the Dart SDK can be located and used from Python.
        '''
        if not self.can_find_dart():
            return [{
                    'message': 'cannot find dart binary',
                    'configuration': {
                        'PATH': os.environ['PATH'],
                        'editor version': '{}-{}'.format(sublime.version(),
                                                         sublime.channel()),
                        'os': sublime.platform(),
                        'arch': sublime.arch(),
                    }
                }]

    def can_find_dart(self):
        return find_in_path('dart', '.exe')

    def get_tool_path(self, name, win_ext=''):
        """Returns the full path to the @name tool in the SDK's bin dir.
        """
        if not self.path_to_sdk:
            _logger.info('could not locate dart sdk')
            return

        name = to_platform_path(name, win_ext)
        return os.path.realpath(os.path.join(self.path_to_bin_dir, name))

    def start_editor(self, file_name=None, row=None, col=None):
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

    @cached_property
    def path_to_sdk(self):
        return os.path.dirname(find_in_path('dart', '.exe'))

    @property
    def path_to_bin_dir(self):
        return os.path.join(self.path_to_sdk, 'bin')

    @property
    def path_to_dart(self):
        """Returns the full path to the dart interpreter.
        """
        return self.get_tool_path('dart', '.exe')

    @property
    def path_to_analyzer(self):
        """Returns the full path to the dart analyzer.
        """
        return self.get_tool_path('dartanalyzer', '.bat')

    @property
    def path_to_docgen(self):
        """Returns the full path to the dart analyzer.
        """
        return self.get_tool_path('docgen', '.bat')

    def check_version(self):
        # TODO(guillermooo): robustify the SDK code. Especially if we cannot
        # locate de dart binary.
        return check_output([self.path_to_dart, '--version'],
                            stderr=STDOUT,
                            universal_newlines=True,
                            startupinfo=supress_window())


class DartFormat(object):
    '''Wraps the `dartfmt` tool.
    '''
    def __init__(self):
        self.path = SDK().get_tool_path('dartfmt', '.bat')

    def format(self, text):
        dart_fmt = TextFilter([self.path])
        text = dart_fmt.filter(text)
        return text

    def format_file(self, path):
        raise NotImplementedError('not immplemented')
