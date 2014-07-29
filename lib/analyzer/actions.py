"""Responses from the analyzer.
"""

import sublime
from Dart.lib.panels import OutputPanel

from Dart import PluginLogger


_logger = PluginLogger(__name__)


def display_error(errors):
    v = sublime.active_window().active_view()

    if len(errors) == 0:
        _logger.debug('no errors - aborting')
        return

    # TODO(guillermooo): Use tokens to identify requests:file.
    if errors.file != v.file_name():
        _logger.debug('different view active - aborting')
        return

    _logger.debug('displaying errors to the user')

    v.add_regions('dart.errors', list(errors.errors_to_regions(v)),
        scope='dartlint.mark.error',
        flags=sublime.DRAW_SQUIGGLY_UNDERLINE |
              sublime.DRAW_NO_FILL |
              sublime.DRAW_NO_OUTLINE)

    v.add_regions('dart.warnings', list(errors.warnings_to_regions(v)),
        scope='dartlint.mark.warning',
        flags=sublime.DRAW_SQUIGGLY_UNDERLINE |
              sublime.DRAW_NO_FILL |
              sublime.DRAW_NO_OUTLINE)

    v.add_regions('dart.infos', list(errors.infos_to_regions(v)),
        scope='dartlint.mark.info',
        flags=sublime.DRAW_SQUIGGLY_UNDERLINE |
              sublime.DRAW_NO_FILL |
              sublime.DRAW_NO_OUTLINE)


    panel = OutputPanel('dart.analyzer')
    errors_pattern = r'^\w+\|\w+\|(.+)\|(\d+)\|(\d+)\|(.+)$'
    panel.set('result_file_regex', errors_pattern)
    panel.write('\n'.join(set(errors.to_compact_text())))


def erase_errors():
    _logger.debug('erasing errors from view')
    v = sublime.active_window().active_view()
    v.erase_regions('dart.errors')
    v.erase_regions('dart.warnings')
    v.erase_regions('dart.infos')
