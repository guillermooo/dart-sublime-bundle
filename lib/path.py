import os

from Dart.lib.plat import to_platform_path


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


def is_dart_script(path):
    return extension_equals(path, '.dart')


def find_in_path(what, win_ext=''):
    '''Searches PATH for @what.

    Returns the path containing @what or `None` if not found.

    @what
      Binary to search for.

    @win_ext
      An extension that will be added to @what on Windows.
    '''
    bin_name = to_platform_path(what, win_ext)
    for path in os.environ['PATH'].split(os.path.pathsep):
        if os.path.exists(os.path.join(path, bin_name)):
            return os.path.realpath(path)

