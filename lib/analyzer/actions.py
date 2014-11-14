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

    analysis_errs = list(errors.errors)
    if analysis_errs == 0:
        clear_ui()
        return

    infos = [ae for ae in analysis_errs if ae.severity == 'INFO']
    warnings = [ae for ae in analysis_errs if ae.severity == 'WARNING']
    errs = [ae for ae in analysis_errs if ae.severity == 'ERROR']

    def to_region(view, data):
        pt = view.text_point(data.location['startLine'] - 1, data.location['startColumn'] - 1)
        return sublime.Region(pt, pt + data.location['length'])

    info_regs = [to_region(v, d) for d in infos]
    warnings_regs = [to_region(v, d) for d in warnings]
    errs_regs = [to_region(v, d) for d in errs]

    print("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF")
    print (info_regs)
    print (warnings_regs)
    print (errs_regs)

    _logger.debug('displaying errors to the user')

    v.add_regions('dart.infos', info_regs,
        scope='dartlint.mark.info',
        icon="Packages/Dart/gutter/dartlint-simple-info.png",
        flags=_flags)

    v.add_regions('dart.warnings', warnings_regs,
        scope='dartlint.mark.warning',
        icon="Packages/Dart/gutter/dartlint-simple-warning.png",
        flags=_flags)

    v.add_regions('dart.errors', errs_regs,
        scope='dartlint.mark.error',
        icon='Packages/Dart/gutter/dartlint-simple-error.png',
        flags=_flags)


    # def to_compact_text(data):
    #     return "{foo.severity}|{foo.type}|{foo.file}|{foo.row}|{foo.column}|{foo.message}".format(foo=data)

    # infos_patts = [to_compact_text(d) for d in infos]
    # warnings_patts = [to_compact_text(d) for d in warnings]
    # errs_patts = [to_compact_text(d) for d in errs]

    # all_errs = + errs_patts + warnings_patts + infos_patts 

    # # TODO(guillermooo): Add a logger attrib to the OutputPanel.
    # panel = OutputPanel('dart.analyzer')
    # errors_pattern = r'^\w+\|\w+\|(.+)\|(\d+)\|(\d+)\|(.+)$'
    # panel.set('result_file_regex', errors_pattern)
    # panel.write('\n'.join(set(all_errs)))


def clear_ui():
    '''Remove UI decoration.
    '''
    _logger.debug('erasing errors from view')
    v = sublime.active_window().active_view()
    v.erase_regions('dart.errors')
    v.erase_regions('dart.warnings')
    v.erase_regions('dart.infos')
