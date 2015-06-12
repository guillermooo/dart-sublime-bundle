# Copyright (c) 2014, Guillermo López-Anglada. Please see the AUTHORS file for details.
# All rights reserved. Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.)

import sublime

from os.path import exists
from os.path import join
from os.path import realpath
from subprocess import check_output
from subprocess import PIPE

from subprocess import Popen
from subprocess import STDOUT
from subprocess import TimeoutExpired
import os
import re
import threading

from Dart.lib.error import ConfigError
from Dart.lib.error import FatalConfigError
from Dart.sublime_plugin_lib import PluginLogger
from Dart.sublime_plugin_lib.filter import TextFilter
from Dart.sublime_plugin_lib.io import AsyncStreamReader
from Dart.sublime_plugin_lib.path import join_on_win
from Dart.sublime_plugin_lib.path import to_platform_path
from Dart.sublime_plugin_lib.plat import is_windows
from Dart.sublime_plugin_lib.plat import supress_window
from Dart.sublime_plugin_lib.settings import FlexibleSettingByPlatform
from Dart.sublime_plugin_lib.subprocess import GenericBinary
from Dart.sublime_plugin_lib.subprocess import killwin32
from Dart.sublime_plugin_lib.text import decode_and_clean


_logger = PluginLogger(__name__)


class FlexibleDartSdkPathSettingByPlatform(FlexibleSettingByPlatform):
    '''
    Data descriptor.

    Reads a setting from Dart config file so that it can be a single value
    or a value keyed by platform. Usefult to easily retrieve a global setting
    for all platforms, or a per-platform setting.
    '''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def validate_sdk_path(self, value):
        try:
            expanded = os.path.expandvars(os.path.expanduser(value))
        except:
            raise FatalConfigError(
                'cannot resolve configured "%s" path to sdk folder: %s' % (self.name, value))
        else:
            full_path = os.path.join(expanded, 'bin',
                    join_on_win('dart', '.exe'))
            if not os.path.exists(full_path):
                raise FatalConfigError(
                    'configured "%s" folder does not contain dart binary: %s' % (self.name, value))
            return expanded

    def validate(self, value):
        value = super().validate(value)
        return self.validate_sdk_path(value)

    def get(self, name):
        self.setts = sublime.load_settings('Dart - Plugin Settings.sublime-settings')
        return self.setts.get(name)


class SDK(object):
    """Wraps the Dart SDK.
    """
    # TODO(guillermooo): make this class more test-friendly.
    def __init__(self):
        self.setts = sublime.load_settings('Dart - Plugin Settings.sublime-settings')

    @property
    def enable_analysis_server(self):
        return self.setts.get('dart_enable_analysis_server') is True

    @property
    def path_to_analysis_snapshot(self):
        if not self.enable_analysis_server:
            return None

        path = os.path.join(self.path_to_bin_dir, 'snapshots',
                'analysis_server.dart.snapshot')

        if not os.path.exists(path):
            raise ConfigError(
                'no analysis server found. Are you using a recent sdk?')

        return path

    def get_bin_tool(self, name, win_ext=''):
        """Returns the full path to the @name tool in the SDK's bin dir.

        @name
          The tool's name.
        @win_ext
          Extension to append to @name in Windows.
        """
        name = join_on_win(name, win_ext)
        return os.path.realpath(os.path.join(self.path_to_bin_dir, name))

    path = FlexibleDartSdkPathSettingByPlatform(name='dart_sdk_path', expected_type=str)

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
        return self.get_bin_tool('pub', '.bat')

    @property
    def path_to_dart2js(self):
        """Returns the full path to dartjs.
        """
        return self.get_bin_tool('dart2js', '.bat')

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

    @property
    def path_to_dartium(self):
        '''Returns the path to the `chrome` binary of the 'Dartium' Chrome
        build.

        May throw a ConfigError that the caller must prepare for.
        '''
        # Dartium will not always be available on the user's machine.
        bin_name = 'chrome.exe'
        if sublime.platform() == 'osx':
            bin_name = 'Contents/MacOS/Chromium'
        elif sublime.platform() == 'linux':
            bin_name = 'chrome'

        try:
            path = self.setts.get('dart_dartium_path')
        except (KeyError, TypeError) as e:
            raise ConfigError('could not find path to Dartium')

        try:
            full_path = os.path.join(path, bin_name)
            full_path = os.path.expandvars(os.path.expanduser(full_path))
            if not os.path.exists(full_path):
                raise ConfigError()
            return full_path
        except Exception as e:
            msg = 'could not find Dartium in directory: %s\n***\n' + full_path
            msg += str(e)
            _logger.error(msg)

    def check_for_critical_configuration_errors(self):
        # this will raise critical config errors if misconfigured
        return self.path

    @property
    def path_to_default_user_browser(self):
        '''Returns the full path to a default non-Dartium browser specified by
        the user.

        Returns a path or `None`.
        '''
        try:
            browsers = self.setts.get('dart_user_browsers')
            path = browsers[browsers['default']]
            path = os.path.expandvars(os.path.expanduser(path))
            if not os.path.exists(path):
                raise ConfigError('wrong path to browser')
            return path
        except Exception as e:
            _logger.debug('error while retrieving default browser %s', e)
            return None

    @path_to_default_user_browser.setter
    def path_to_default_user_browser(self, value):
        plat_browsers = self.user_browsers
        plat_browsers['default'] = value
        self.setts = sublime.load_settings('Dart - Plugin Settings.sublime-settings')
        self.setts.set('dart_user_browsers', plat_browsers)
        sublime.save_settings('Dart - Plugin Settings.sublime-settings')

    @property
    def user_browsers(self):
        '''Returns the full path to a non-Dartium browser specified by the
        user.

        Returns a dictionary of name -> path, or `None`.
        '''
        return self.setts.get('dart_user_browsers')

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
        return dart_fmt.filter(text).rstrip()


class RunDartWithObservatory(object):
    def __init__(self, path, cwd=None, listener=None):
        self.proc = None
        self.port = None
        self.path = path
        self.listener = listener
        self.cwd = cwd

    def start(self):
        _logger.debug('running through observatory: %s' % self.path)
        self.proc = Popen([SDK().path_to_dart, '--checked', '--observe=0',
                          self.path], stdout=PIPE, stderr=PIPE, cwd=self.cwd,
                          startupinfo=supress_window())

        # TODO(guillermooo): add names and log these threads.
        AsyncStreamReader(self.proc.stdout, self.on_data).start()
        AsyncStreamReader(self.proc.stderr, self.on_error).start()

    def stop(self):
        if self.proc:
            _logger.debug('stopping RunDartWithObservatory...')
            self.proc.kill()
            self.proc.stderr.close()
            self.proc.stdout.close()
            self.proc = None

    def on_data(self, data_bytes):
        text = decode_and_clean(data_bytes)
        if not self.port:
            m = re.match('^Observatory listening on http://.*?:(\d+)', text)
            self.port = int(m.groups()[0])
            _logger.debug('captured observatory port: %d' % self.port)

        if self.listener:
            self.listener.on_data(text)

    def on_error(self, data_bytes):
        if self.listener:
            self.listener.on_error(decode_and_clean(data_bytes))


class PubServe(object):
    def __init__(self, is_example=False, cwd=None, listener=None):
        self.proc = None
        self.port = None
        self.listener = listener
        self.is_example = is_example
        self.cwd = cwd

    def start(self):
        _logger.debug('running pub serve...')
        cmd = []
        if not self.is_example:
            cmd = [SDK().path_to_pub, 'serve', '--port=0']
        else:
            cmd = [SDK().path_to_pub, 'serve', 'example', '--port=0']
        self.proc = Popen(cmd,
                          stdout=PIPE,
                          stderr=PIPE,
                          cwd=self.cwd,
                          startupinfo=supress_window()
                          )

        # TODO(guillermooo): add names and log these threads.
        AsyncStreamReader(self.proc.stdout, self.on_data).start()
        AsyncStreamReader(self.proc.stderr, self.on_error).start()

    def stop(self):
        if self.proc:
            _logger.debug('stopping pub serve...')
            if os.name == 'nt':
                # self.proc.kill() won't work.
                killwin32(self.proc)
                self.proc = None
                return
            self.proc.kill()
            self.proc = None

    def on_data(self, data_bytes):
        text = decode_and_clean(data_bytes)
        if self.listener:
            self.listener.on_data(text)

    def on_error(self, data_bytes):
        if self.listener:
            self.listener.on_error(decode_and_clean(data_bytes))

class Dartium(object):
    '''Wraps Dartium.
    '''
    def __init__(self):
        user_home = os.path.expanduser("~")
        self.args = (
            '--checked',
            '--user-data-dir=' + os.path.join(user_home, '.dartium'),
            '--enable-experimental-web-platform-features',
            '--enable-html-imports',
            '--no-first-run',
            '--no-default-browser-check',
            '--no-process-singleton-dialog',
            '--enable-avfoundation',
            )
        try:
            self.path = SDK().path_to_dartium
        except ConfigError as e:
            _logger.error(e)

    def get_env(self, new={}):
        current = os.environ.copy()
        current.update(new)
        return current

    def start(self, *args):
        try:
            cmd = (self.path,) + self.args + args
            _logger.debug('Dartium cmd: %r' % (cmd,))
            Popen(cmd, startupinfo=supress_window())
        except Exception as e:
            _logger.error('=' * 80)
            _logger.error('could not start Dartium')
            _logger.error('-' * 80)
            _logger.error(e)
            _logger.error('=' * 80)
