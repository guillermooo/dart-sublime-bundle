import os
from os.path import join

from Dart.lib.plat import is_windows


def extension_equals(path_or_view, extension):
    """Compares @path_or_view's extensions with @extension.

    Returns `True` if they are the same, `False` otherwise.
    Returns `False` if @path_or_view isn't saved on disk.
    """
    try:
        if path_or_view.file_name() is None:
            return False
        return extension_equals(path_or_view.file_name(), extension)
    except AttributeError:
        return os.path.splitext(path_or_view)[1] == extension


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
    bin_name = to_platform_path(name, win_ext)
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
    if os.path.exists(os.path.join(start, fname)):
        return os.path.join(start, fname)

    if os.path.dirname(start) == start:
        return

    if not os.path.exists(start):
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

