# Copyright (c) 2014, Guillermo López-Anglada. Please see the AUTHORS file for details.
# All rights reserved. Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.)

import sublime

import os

from Dart import PluginLogger
from Dart.lib.out_there.yaml import load
from Dart.lib.path import find_file
from Dart.lib.path import is_prefix
from Dart.lib.path import is_view_dart_script
from Dart.lib.path import to_platform_path


_logger = PluginLogger(__name__)


def find_pubspec(start):
    try:
        return find_file(start, 'pubspec.yaml')
    except Exception as e:
        _logger.debug('error finding pubspec: %s', e)


class PubPackage(object):
    def __init__(self, pubspec):
        self.pubspec = pubspec

    def _get_top_level_dir(self, name):
        p = os.path.join(self.pubspec.parent, name)
        if os.path.exists(p):
            return p
        _logger.debug('path not found in project: %s', p)

    def make_top_level_dir(self, name):
        os.mkdir(os.path.join(self.pubspec.parent, name))

    def is_prefix(self, prefix, path):
        assert prefix and path, 'cannot call with None params'
        return is_prefix(prefix, path)

    @property
    def path_to_web(self):
        return self._get_top_level_dir('web')

    @property
    def path_to_bin(self):
        return self._get_top_level_dir('bin')

    @property
    def path_to_test(self):
        return self._get_top_level_dir('test')

    @property
    def path_to_tool(self):
        return self._get_top_level_dir('tool')

    @property
    def path_to_benchmark(self):
        return self._get_top_level_dir('benchmark')

    @property
    def path_to_doc(self):
        return self._get_top_level_dir('doc')

    @property
    def path_to_example(self):
        return self._get_top_level_dir('example')

    @property
    def path_to_lib(self):
        return self._get_top_level_dir('lib')

    def has_dependency(self, name, version=None):
        plock = self.pubspec.get_pubspec_lock()
        if not plock:
            return
        return plock.has_dependency(name, version)

    @classmethod
    def from_path(cls, path):
        pubspec = PubspecFile.from_path(path)
        if pubspec is None:
            return
        return cls(pubspec)


class PubspecLockFile(object):
    '''Wraps a pubspec.yaml file.
    '''
    def __init__(self, pubspec):
        self.path = os.path.join(pubspec.parent, 'pubspec.lock')
        self._data = None
    @property
    def path_to_web(self):
        return self._get_top_level_dir('web')

    @property
    def parent(self):
        return os.path.dirname(self.path)

    def _load(self):
        if self._data is not None:
            return
        self._data = load(open(self.path, 'rt'))

    def has_dependency(self, name, version=None):
        self._load()
        return name in self._data['packages']

    @classmethod
    def from_pubspec(cls, pubspec):
        '''Returns a `PubspecFile` ready for use, or `None` if no pubspec
        file was found.
        '''
        if os.path.exists(os.path.join(pubspec.parent, 'pubspec.lock')):
            return cls(pubspec)


class PubspecFile(object):
    '''Wraps a pubspec.yaml file.
    '''
    def __init__(self, path):
        self.path = path
        self._data = None

    @property
    def parent(self):
        return os.path.dirname(self.path)

    def _load(self):
        if self._data is not None:
            return
        self._data = load(open(self.path, 'rt'))

    def get_pubspec_lock(self):
        # TODO(guillermooo): cache this?
        return PubspecLockFile.from_pubspec(self)

    @classmethod
    def from_path(cls, path):
        '''Returns a `PubspecFile` ready for use, or `None` if no pubspec
        file was found.
        '''
        p = find_pubspec(path)
        if p:
            return cls(p)
        _logger.debug('no pubspec.yaml found')


class DartFile(object):
    '''Wraps a ST view or a file name and provides convenience methods if it's
    a Dart project file.
    '''
    def __init__(self, view):
        '''
        @view
          A ST view.
        '''
        self.view = None
        self.path = None
        if isinstance(view, sublime.View):
            self.view = view
            self.path = view.file_name()

    @classmethod
    def from_path(cls, path):
        '''
        @path
          A path to a file.
        '''
        assert isinstance(path, str), 'wrong call'
        dart_view = cls(None)
        dart_view.path = path
        return dart_view

    def _get_top_lines(self):
        end = self.view.full_line(80 * 50).end()
        region = sublime.Region(0, end)
        lines = self.view.lines(region)
        yield from (self.view.substr(line) for line in lines)

    def _find_at_top(self, *sought_terms):
        for line in self._get_top_lines():
            for term in  sought_terms:
                if term in line:
                    return True

    def has_prefix(self, prefix):
        assert prefix, 'cannot call with empty prefix'
        return is_prefix(prefix, self.path)

    @property
    def is_runnable(self):
        '''Returns `True` if the file is a pubspec.yaml or a .dart file, or if
        the file is under the following directories:
          - web
          - example

        If a file is under any of those dirs, we consider it runnable as part
        of a web app or a cli program.
        '''
        project = PubPackage.from_path(self.path)
        return any((self.is_dart_file,
                    self.is_pubspec,
                    (project and
                     project.path_to_web and
                     self.has_prefix(project.path_to_web)),
                    (project and
                     project.path_to_example and
                     self.has_prefix(project.path_to_example)),
                    ))

    @property
    def is_dart_file(self):
        return is_view_dart_script(self.view or self.path)

    @property
    def url_path(self):
        # TODO(guillermooo): Fix this; we should not have to check for both.
        if self.is_server_app or not self.is_web_app:
            return

        if not self.path.endswith('.html'):
            return

        project = PubPackage.from_path(self.path)
        path = None
        if self.is_example:
            path = self.path[len(project.path_to_example)+1:]
        else:
            path = self.path[len(project.path_to_web)+1:]
        return path.replace('\\', '/')

    @property
    def is_server_app(self):
        project = PubPackage.from_path(self.path)
        if not project:
            return False

        if project.path_to_bin and self.has_prefix(project.path_to_bin):
            return True

        if project.path_to_test and self.has_prefix(project.path_to_test):
            return True

        if (project.path_to_example and
            self.has_prefix(project.path_to_example)):
                # TODO(guillermooo): improve detection of cli apps under
                # 'example'.
                is_cli_script = self._find_at_top('dart:io')
                is_not_web_file = (self.is_dart_file and
                                   not self._find_at_top('import:html'))
                return (is_cli_script or is_not_web_file)

        return False

    @property
    def is_web_app(self):
        project = PubPackage.from_path(self.path)
        if not project:
            return False

        if project.path_to_web and self.has_prefix(project.path_to_web):
            return True

        # FIXME(guillermooo): This is wrong.
        # We're assuming that we've checked before whether this is
        # a cli app within 'example'.
        return bool(project.path_to_example and
                self.has_prefix(project.path_to_example))

    @property
    def is_pubspec(self):
        return os.path.basename(self.path) == 'pubspec.yaml'

    @property
    def is_example(self):
        '''Returns `True` if the view's path is under the 'example' dir.
        '''
        assert self.path, 'view has not been saved yet'
        project = PubPackage.from_path(self.path)
        if not (project and project.path_to_example):
            return False
        return self.has_prefix(project.path_to_example)
