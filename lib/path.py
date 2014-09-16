'''Helper functions for path management.
'''

import os
from os.path import join
from contextlib import contextmanager

from Dart.lib.plat import is_windows


def extension_equals(path_or_view, extension):
    """Compares @path_or_view's extensions with @extension.

    Returns `True` if they are the same, `False` otherwise.
    Returns `False` if @path_or_view is a view and isn't saved on disk.
    """
    try:
        if path_or_view.file_name() is None:
            return False
        return extension_equals(path_or_view.file_name(), extension)
    except AttributeError:
        try:
            return os.path.splitext(path_or_view)[1] == extension
        except Exception:
            raise TypeError('string or view required, got {}'
                            .format(type(path_or_view)))


def is_view_dart_script(view):
    """Checks whether @view looks like a Dart script file.

    Returns `True` if @view's file name ends with '.dart'.
    Returns `False` if @view isn't saved on disk.
    """
    if view.file_name() is None:
        return False
    return is_dart_script(view.file_name())


def is_pubspec(path_or_view):
    """Returns `True` if @path_or_view is 'pubspec.yaml'.
    """
    try:
        if path_or_view.file_name() is None:
            return
        return path_or_view.file_name().endswith('pubspec.yaml')
    except AttributeError:
        return path_or_view.endswith('pubspec.yaml')


def is_dart_script(path):
    return extension_equals(path, '.dart')


def find_in_path(name, win_ext=''):
    '''Searches PATH for @name.

    Returns the path containing @name or `None` if not found.

    @name
      Binary to search for.

    @win_ext
      An extension that will be added to @name on Windows.
    '''
    bin_name = join_on_win(name, win_ext)
    for path in os.environ['PATH'].split(os.path.pathsep):
        path = os.path.expandvars(os.path.expanduser(path))
        if os.path.exists(os.path.join(path, bin_name)):
            return os.path.realpath(path)


def find_file(start, fname):
    '''Finds a file in a directory hierarchy starting from @start and
    walking backwards.

    @start
      The directory to start from.

    @fname
      Sought file.
    '''
    if not os.path.exists(start):
        return

    if os.path.exists(os.path.join(start, fname)):
        return os.path.join(start, fname)

    if os.path.dirname(start) == start:
        return

    return find_file(os.path.dirname(start), fname)


def is_prefix(prefix, path):
    prefix = os.path.realpath(prefix)
    path = os.path.realpath(path)
    return path.startswith(prefix)


def to_platform_path(original, append):
    """
    Useful to add .exe to @original, .bat, etc if ST is running on Windows.

    @original
      Original path.
    @append
      Fragment to append to @original on Windows.
    """
    if is_windows():
        if append.startswith('.'):
            return original + append
        return join(original, append)
    return original


def find_pubspec_path(path, original=None):
    """Locates the directory containing a pubspec.yaml file.

    Returns (str, bool): A path, and whether a pubspec.yaml was found. If no
    pubspec.yaml was found, the path will be passed-in path.
    """
    if os.path.exists(os.path.join(path, 'pubspec.yaml')):
        return (path, True)

    if original is None:
        original = path

    p = os.path.dirname(path)

    # Reached drive unit; stop.
    if p == os.path.dirname(p):
        if not os.path.isdir(original):
            p = os.path.dirname(original)
        return (p, False)

    return find_pubspec_path(p, original)


def is_active_path(path):
    """Returns `True` if the current view's path equals @path.
    """
    group_id = view.window().active_group()
    group_view = view.window().active_view_in_group(group_id)
    return os.path.realpath(group_view.file_name()) == os.path.realpath(path)


def is_active(view):
    """Returns `True` if @view is the view being currently edited.
    """
    group_id = view.window().active_group()
    group_view = view.window().active_view_in_group(group_id)
    return group_view.id() == view.id()


@contextmanager
def pushd(to):
    old = os.getcwd()
    os.chdir(to)
    yield to
    os.chdir(old)


def join_on_win(original, append):
    """ Useful to add .exe, .bat, etc. to @original if ST is running on
    Windows.

    @original
      Original path.

    @append
      Fragment to append to @original on Windows. If it's an extension
      (the fragment begins with '.'), it's tucked at the end of @original.
      Otherwise, it's joined as a path.
    """
    if is_windows():
        if append.startswith('.'):
            return original + append
        return os.path.join(original, append)
    return original
