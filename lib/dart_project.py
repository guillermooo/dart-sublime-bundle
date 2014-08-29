import sublime

import os

from Dart.lib.path import find_file
from Dart.lib.out_there.yaml import load
from Dart.lib.path import is_view_dart_script


class DartProject(object):
    def __init__(self, pubspec):
        self.pubspec = pubspec

    def _get_top_level_dir(self, name):
        p = os.path.join(self.pubspec.parent, name)
        if os.path.exists(p):
            return p

    def make_top_level_dir(self, name):
        os.mkdir(os.path.join(self.pubspec.parent, name))

    def is_path_under(self, top_level, path):
        prefix = os.path.realpath(top_level)
        target = os.path.realpath(path)
        return target.startswith(prefix)

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


def find_pubspec(start):
    return find_file(start, 'pubspec.yaml')


class ViewInspector(object):
    def __init__(self, view):
        self.view = view

    def _get_top_lines(self):
        end = 80 * 50
        end = self.view.full_line(end).end()
        region = sublime.Region(0, end)
        assert isinstance(region, sublime.Region)
        lines = self.view.lines(region)
        yield from (self.view.substr(line) for line in lines)

    def _find_at_top(self, *sought_terms):
        for line in self._get_top_lines():
            for term in  sought_terms:
                if term in line:
                    return True

    @property
    def is_project_file(self):
        return any((self.is_dart_file,
                    self.is_pubspec))

    @property
    def is_dart_file(self):
        return is_view_dart_script(self.view)

    @property
    def is_server_app(self):
        return self._find_at_top("import 'dart:io'", 'import "dart:io"')

    @property
    def is_web_app(self):
        return self._find_at_top("import 'dart:html'", 'import "dart:html"')

    @property
    def is_pubspec(self):
        return os.path.basename(self.view.file_name()) == 'pubspec.yaml'
