# Copyright (c) 2014, Guillermo López-Anglada. Please see the AUTHORS file for details.
# All rights reserved. Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.)

"""Actions performed using the analyzer's responses.
"""

import sublime

from Dart.sublime_plugin_lib import PluginLogger
from Dart.sublime_plugin_lib.panels import OutputPanel


_logger = PluginLogger(__name__)


_flags = (sublime.DRAW_SQUIGGLY_UNDERLINE | sublime.DRAW_NO_FILL |
          sublime.DRAW_NO_OUTLINE)


def show_errors(errors):
    '''Show errors in the ui.

    @errors
      An instance of `ErrorInfoCollection`.
    '''
    v = sublime.active_window().active_view()
    # TODO(guillermooo): Use tokens to identify requests:file.
    if errors.file != v.file_name():
        _logger.debug('different view active - aborting')
        return

    if len(errors) == 0:
        clear_ui()
        return

    _logger.debug('displaying errors to the user')

    v.add_regions('dart.infos', list(errors.infos_to_regions(v)),
        scope='dartlint.mark.info',
        icon="Packages/Dart/gutter/dartlint-simple-info.png",
        flags=_flags)

    v.add_regions('dart.warnings', list(errors.warnings_to_regions(v)),
        scope='dartlint.mark.warning',
        icon="Packages/Dart/gutter/dartlint-simple-warning.png",
        flags=_flags)

    v.add_regions('dart.errors', list(errors.errors_to_regions(v)),
        scope='dartlint.mark.error',
        icon='Packages/Dart/gutter/dartlint-simple-error.png',
        flags=_flags)

    # TODO(guillermooo): Add a logger attrib to the OutputPanel.
    panel = OutputPanel('dart.analyzer')
    errors_pattern = r'^\w+\|\w+\|(.+)\|(\d+)\|(\d+)\|(.+)$'
    panel.set('result_file_regex', errors_pattern)
    panel.write('\n'.join(set(errors.to_compact_text())))


def clear_ui():
    '''Remove UI decoration.
    '''
    _logger.debug('erasing errors from view')
    v = sublime.active_window().active_view()
    v.erase_regions('dart.errors')
    v.erase_regions('dart.warnings')
    v.erase_regions('dart.infos')
