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
from Dart.lib.path import find_in_path
from Dart.lib.plat import is_windows
from Dart.lib.plat import supress_window
from Dart.lib.plat import to_platform_path
from Dart.lib.error import FatalConfigError


_logger = PluginLogger(__name__)


class SDK(object):
    """Wraps the Dart SDK.
    """
    def __init__(self):
        setts = sublime.load_settings('Preferences.sublime-settings')
        p = setts.get('dart_sdk_path')

        try:
            if not os.path.exists(
                os.path.join(p, 'bin', to_platform_path('dart', '.exe'))):
                    msg = 'wrong path in dart_sdk_path: {}'.format(p)
                    raise FatalConfigError(msg)
            self._path = p
        except TypeError:
            msg = 'invalid value of dart_sdk_path: {}'.format(p)
            raise FatalConfigError(msg)

    def get_bin_tool(self, name, win_ext=''):
        """Returns the full path to the @name tool in the SDK's bin dir.

        @name
          The tool's name.
        @win_ext
          Extension to append to @name in Windows.
        """
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
        if not self.path:
            _logger.info('could not locate the dart sdk')
            return

        assert not any((file_name, row, col)), 'not implemented'
        bin_name = to_platform_path('DartEditor', '.exe')

        # TODO: Add path_to_editor property.
        path = realpath(join(self.path, '../{0}'.format(bin_name)))
        if not exists(path):
            print("Dart: Error - Cannot find Dart Editor binary.")
            print("              Is the Dart Editor installed?")
            _logger.info('cannot find Dart Editor binary')
            _logger.info('using path to Dart SDK: %s', self.path)
            return

        # Don't wait for process to terminate so we don't block ST.
        proc = Popen([path])
        try:
            # Just see if we got an error sort of quickly.
            proc.wait(.5)
        except TimeoutExpired:
            pass
        else:
            if proc.returncode != 0:
                _logger.error('Dart Editor exited with error code %d', proc.returncode)

    @property
    def path(self):
        return self._path

    @property
    def path_to_bin_dir(self):
        return os.path.join(self.path, 'bin')

    @property
    def path_to_dart(self):
        """Returns the full path to the dart interpreter.
        """
        return self.get_bin_tool('dart', '.exe')

    @property
    def path_to_pub(self):
        """Returns the full path to pub.
        """
        return self.get_tool_path('pub', '.bat')

    @property
    def path_to_dart2js(self):
        """Returns the full path to dartjs.
        """
        return self.get_tool_path('dart2js', '.bat')

    @property
    def path_to_analyzer(self):
        """Returns the full path to the dart analyzer.
        """
        return self.get_bin_tool('dartanalyzer', '.bat')

    @property
    def path_to_docgen(self):
        """Returns the full path to docgen.
        """
        return self.get_bin_tool('docgen', '.bat')

    def check_version(self):
        return check_output([self.path_to_dart, '--version'],
                            stderr=STDOUT,
                            universal_newlines=True,
                            startupinfo=supress_window())


class DartFormat(object):
    '''Wraps the `dartfmt` tool.
    '''
    def __init__(self):
        self.path = SDK().get_bin_tool('dartfmt', '.bat')

    def format(self, text):
        dart_fmt = TextFilter([self.path])
        return dart_fmt.filter(text)
