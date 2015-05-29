# Copyright (c) 2014, Guillermo López-Anglada. Please see the AUTHORS file for details.
# All rights reserved. Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.)

import os
from Dart.sublime_plugin_lib.path import extension_equals


def is_view_dart_script(view):
    """Checks whether @view looks like a Dart script file.

    Returns `True` if @view's file name ends with '.dart'.
    Returns `False` if @view isn't saved on disk.
    """
    try:
        if view.file_name() is None:
            return False
        return is_dart_script(view.file_name())
    except AttributeError:
        # view is a path
        return is_dart_script(view)


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


# TODO(guillermooo): duplicated (find_pubspec)?
def find_pubspec_path(path, original=None):
    """Locates the directory containing a pubspec.yaml file.

    Returns (str, bool): A path, and whether a pubspec.yaml was found. If no
    pubspec.yaml was found, the path will be passed-in path.
    """
    if os.path.exists(os.path.join(path, 'pubspec.yaml')):
        return path

    if original is None:
        original = path

    p = os.path.dirname(path)

    # Reached drive unit; stop.
    if p == os.path.dirname(p):
        return

    return find_pubspec_path(p, original)


def is_path_under(top_level, path):
    prefix = os.path.realpath(top_level)
    target = os.path.realpath(path)
    return target.startswith(prefix)
