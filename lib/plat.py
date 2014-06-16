import sublime

from os.path import join

import subprocess


def is_windows():
    """Returns `True` if ST is running on Windows.
    """
    return sublime.platform() == 'windows'


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


def supress_window():
    """Returns a STARTUPINFO structure configured to supress windows.
    Useful, for example, to supress console windows.

    Works only on Windows.
    """
    if is_windows():
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE
        return startupinfo
    return None
