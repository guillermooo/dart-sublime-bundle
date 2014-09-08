import sublime

from os.path import join

import subprocess


def is_windows():
    """Returns `True` if ST is running on Windows.
    """
    return sublime.platform() == 'windows'


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
