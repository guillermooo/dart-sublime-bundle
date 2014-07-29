"""Responses from the analyzer.
"""

import sublime
from Dart.lib.panels import OutputPanel


def display_error(errors):
    v = sublime.active_window().active_view()

    v.add_regions('dart.errors', list(errors.errors_to_regions()),
        scope='dartlint.mark.error',
        flags=sublime.DRAW_SQUIGGLY_UNDERLINE |
              sublime.DRAW_NO_FILL |
              sublime.DRAW_NO_OUTLINE)

    v.add_regions('dart.warnings', list(errors.warnings_to_regions()),
        scope='dartlint.mark.warning',
        flags=sublime.DRAW_SQUIGGLY_UNDERLINE |
              sublime.DRAW_NO_FILL |
              sublime.DRAW_NO_OUTLINE)

    panel = OutputPanel('dart.analyzer')
    errors_pattern = r'^\w+\|\w+\|(.+)\|(\d+)\|(\d+)\|(.+)'
    panel.set('result_file_regex', errors_pattern)
    panel.write('\n'.join(list(errors.to_compact_text())))
    # panel.show()


def erase_errors():
    v = sublime.active_window().active_view()
    v.erase_regions('dart.errors')
    v.erase_regions('dart.warnings')
