# Copyright (c) 2014, Guillermo López-Anglada. Please see the AUTHORS file for details.
# All rights reserved. Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.)

from subprocess import Popen

from Dart import PluginLogger
from Dart.lib.plat import supress_window


_logger = PluginLogger(__name__)


class GenericBinary(object):
    '''Starts a process.
    '''
    def __init__(self, *args, show_window=True):
        '''
        @show_window
          Windows only. Whether to show a window.
        '''
        self.args = args
        self.startupinfo = None
        if not show_window:
            self.startupinfo = supress_window()

    def start(self, args=[], env={}, shell=False, cwd=None):
        cmd = self.args + tuple(args)
        _logger.debug('running cmd line (GenericBinary): %s', cmd)
        Popen(cmd, startupinfo=self.startupinfo, env=env, shell=shell,
              cwd=cwd)
