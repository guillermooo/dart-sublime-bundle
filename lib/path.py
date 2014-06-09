import os


def view_extension_equals(view, extension):
    """Compares @view's extensions with @extension.

    Returns `True` if they are the same.
    Returns `False` if @view isn't saved on disk.
    """
    if view.file_name() is None:
        return False
    return extension_equals(view.file_name(), extension)


def extension_equals(path, extension):
    return os.path.splitext(path)[1] == extension


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
