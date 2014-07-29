"""Responses from the analyzer.
"""

import sublime


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


def erase_errors():
    v = sublime.active_window().active_view()
    v.erase_regions('dart.errors')
    v.erase_regions('dart.warnings')
