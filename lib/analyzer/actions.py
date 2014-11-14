# Copyright (c) 2014, Guillermo López-Anglada. Please see the AUTHORS file for details.
# All rights reserved. Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.)

"""Actions performed using the analyzer's responses.
"""

import sublime

from Dart.lib.analyzer.api.types import AnalysisErrorSeverity
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

    analysis_errs = list(errors.errors)
    if analysis_errs == 0:
        clear_ui()
        return

    infos = [ae for ae in analysis_errs if (ae.severity == AnalysisErrorSeverity.INFO)]
    warns = [ae for ae in analysis_errs if (ae.severity == AnalysisErrorSeverity.WARNING)]
    erros = [ae for ae in analysis_errs if (ae.severity == AnalysisErrorSeverity.ERROR)]

    def error_to_region(view, error):
        '''Converts location data to region data.
        '''
        pt = view.text_point(error.location['startLine'] - 1,
                             error.location['startColumn'] - 1)
        return sublime.Region(pt, pt + error.location['length'])

    info_regs = [error_to_region(v, item) for item in infos]
    warn_regs = [error_to_region(v, item) for item in warns]
    errs_regs = [error_to_region(v, item) for item in erros]

    _logger.debug('displaying errors to the user')

    v.add_regions('dart.infos', info_regs,
        scope='dartlint.mark.info',
        icon="Packages/Dart/gutter/dartlint-simple-info.png",
        flags=_flags)

    v.add_regions('dart.warnings', warn_regs,
        scope='dartlint.mark.warning',
        icon="Packages/Dart/gutter/dartlint-simple-warning.png",
        flags=_flags)

    v.add_regions('dart.errors', errs_regs,
        scope='dartlint.mark.error',
        icon='Packages/Dart/gutter/dartlint-simple-error.png',
        flags=_flags)

    def to_compact_text(error):
        return ("{error.severity}|{error.type}|{loc[file]}|"
                "{loc[startLine]}|{loc[startColumn]}|{error.message}").format(
                                                error=error, loc=error.location)

    info_patts = [to_compact_text(item) for item in infos]
    warn_patts = [to_compact_text(item) for item in warnings]
    errs_patts = [to_compact_text(item) for item in errs]

    all_errs = set(errs_patts + warn_patts + info_patts)

    panel = OutputPanel('dart.analyzer')
    errors_pattern = r'^\w+\|\w+\|(.+)\|(\d+)\|(\d+)\|(.+)$'
    panel.set('result_file_regex', errors_pattern)
    panel.write('\n'.join(all_errs))


def clear_ui():
    '''Remove UI decoration.
    '''
    _logger.debug('erasing errors from view')
    v = sublime.active_window().active_view()
    v.erase_regions('dart.errors')
    v.erase_regions('dart.warnings')
    v.erase_regions('dart.infos')
