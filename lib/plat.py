import sublime


def is_windows():
    """Returns `True` if ST is running on Windows.
    """
    return sublime.platform() == 'windows'

