import os

from Dart.lib.path import find_file
from Dart.lib.out_there.yaml import load


class DartProject(object):
    def __init__(self, pubspec):
        self.pubspec = pubspec

    def _check_path(self, path):
        p = os.path.join(self.pubspec.parent, path)
        if os.path.exists(p):
            return p

    @property
    def path_to_web(self):
        return _check_path('web')

    @property
    def path_to_bin(self):
        return _check_path('bin')

    @property
    def path_to_test(self):
        return _check_path('test')

    @property
    def path_to_tool(self):
        return _check_path('tool')

    @property
    def path_to_benchmark(self):
        return _check_path('benchmark')

    @property
    def path_to_doc(self):
        return _check_path('doc')

    @property
    def path_to_example(self):
        return _check_path('example')

    @property
    def path_to_lib(self):
        return _check_path('lib')

    @classmethod
    def from_path(self, path):
        pubspec = PubspecFile.from_path(path)
        if pubspec is None:
            return
        return DartProject(pubspec)


class PubspecFile(object):
    '''Wraps a pubspec.yaml file.
    '''
    def __init__(self, path):
        self.path
        self._data = None

    @property
    def parent(self):
        return os.path.dirname(self.path)

    def _load(self):
        if self._data is not None:
            return
        self._data = load(open(self.path, 'rt'))

    def contains_dependency(self, name, version=None):
        self._load()
        return name in self._data['packages']

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
