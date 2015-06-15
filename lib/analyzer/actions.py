# Copyright (c) 2014, Guillermo López-Anglada. Please see the AUTHORS file for details.
# All rights reserved. Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.)

"""
Actions performed inside ST3 based on the analysis server's responses.
"""

import os

import sublime

from Dart.sublime_plugin_lib import PluginLogger
from Dart.sublime_plugin_lib.panels import OutputPanel
from Dart.sublime_plugin_lib.sublime import get_active_view
from Dart.sublime_plugin_lib.sublime import R

from Dart.lib.analyzer.api.protocol import AnalysisErrorSeverity
from Dart.lib.analyzer.api.protocol import AnalysisErrorType
from Dart.lib.analyzer.api.protocol import ElementKind
from Dart import editor_context


_logger = PluginLogger(__name__)


DAS_SCOPE_ERROR = 'invalid'
DAS_SCOPE_INFO = 'comment'
DAS_SCOPE_WARNING = 'constant.numeric'

DAS_UI_REGIONS_INFOS = 'dart.infos'
DAS_UI_REGIONS_WARNINGS = 'dart.warnings'
DAS_UI_REGIONS_ERRORS = 'dart.errors'


_flags = (sublime.DRAW_SQUIGGLY_UNDERLINE |
          sublime.DRAW_NO_FILL |
          sublime.DRAW_NO_OUTLINE)


def handle_navigation_data(navigation_params):
    editor_context.navigation = navigation_params


def show_errors(errors):
    '''Show errors in the ui.

    @errors
      An instance of `ErrorInfoCollection`.
    '''
    v = get_active_view()
    # TODO(guillermooo): Use tokens to identify requests:file.
    # todo (pp): notifications don't have id; process all
    if os.path.realpath(errors.file) != os.path.realpath(v.file_name()):
        _logger.debug('different view active - aborting')
        return

    analysis_errors = list(errors.errors)
    if analysis_errors == 0:
        clear_ui()
        return

    infos = [ae for ae in analysis_errors if
                (ae.severity == AnalysisErrorSeverity.INFO)
                and (ae.type != AnalysisErrorType.TODO)]
    warns = [ae for ae in analysis_errors if (ae.severity == AnalysisErrorSeverity.WARNING)]
    erros = [ae for ae in analysis_errors if (ae.severity == AnalysisErrorSeverity.ERROR)]

    def error_to_region(view, error):
        '''Converts location data to region data.
        '''
        pass
        loc = error.location
        pt = view.text_point(loc.startLine - 1,
                             loc.startColumn - 1)
        return R(pt, pt + loc.length)

    info_regs = [error_to_region(v, item) for item in infos]
    warn_regs = [error_to_region(v, item) for item in warns]
    errs_regs = [error_to_region(v, item) for item in erros]

    _logger.debug('displaying errors to the user')

    v.add_regions(DAS_UI_REGIONS_INFOS, info_regs,
        scope=DAS_SCOPE_INFO,
        icon="Packages/Dart/gutter/dartlint-simple-info.png",
        flags=_flags)

    v.add_regions(DAS_UI_REGIONS_WARNINGS, warn_regs,
        scope=DAS_SCOPE_WARNING,
        icon="Packages/Dart/gutter/dartlint-simple-warning.png",
        flags=_flags)

    v.add_regions(DAS_UI_REGIONS_ERRORS, errs_regs,
        scope=DAS_SCOPE_ERROR,
        icon='Packages/Dart/gutter/dartlint-simple-error.png',
        flags=_flags)

    def to_compact_text(error):
        return ("{error.severity}|{error.type}|{loc.file}|"
                "{loc.startLine}|{loc.startColumn}|{error.message}").format(
                                                error=error, loc=error.location)


    info_patts = [to_compact_text(item) for item in infos]
    warn_patts = [to_compact_text(item) for item in warns]
    errs_patts = [to_compact_text(item) for item in erros]

    all_errs = set(errs_patts + warn_patts + info_patts)

    panel = OutputPanel('dart.analyzer')

    if not all_errs:
        editor_context.errors = []
        panel.hide()
        return

    errors_pattern = r'^\w+\|\w+\|(.+)\|(\d+)\|(\d+)\|(.+)$'
    panel.set('result_file_regex', errors_pattern)
    # This will overwrite any previous text.
    panel.write('\n' + '\n'.join(all_errs))

    # FIXME: It appears that if ST dev find a .sublime-syntax and a .tmLanguage
    # file, it will load # the first one. But how do we refer to the file then?
    if sublime.version() >= '3084':
        panel.view.set_syntax_file('Packages/Dart/Support/Analyzer Output.sublime-syntax')
    else:
        panel.view.set_syntax_file('Packages/Dart/Support/Analyzer Output.tmLanguage')

    panel.view.settings().set('rulers', [])
    panel.show()

    try:
        v.show(v.sel()[0])
    except IndexError:
        pass

    sublime.status_message("Dart: Errors found")

    editor_context.errors = all_errs


def clear_ui():
    '''Remove UI decoration.
    '''
    _logger.debug('erasing errors from view')
    v = get_active_view()
    v.erase_regions(DAS_UI_REGIONS_ERRORS)
    v.erase_regions(DAS_UI_REGIONS_WARNINGS)
    v.erase_regions(DAS_UI_REGIONS_INFOS)


def handle_completions(results):
    show = False
    with editor_context.autocomplete_context as actx:

        _PROPERTY = '\u25CB {}'
        _FUNCTION = '\u25BA {}'
        _CONSTRUCTOR = '\u00A9 {}'
        _OTHER = '· {}'

        formatted = []
        item = ''
        for c in results.results:
            if not c.element:
                continue
            if c.element.kind == ElementKind.FUNCTION or c.element.kind == ElementKind.METHOD or c.element.kind == ElementKind.SETTER:
                formatted.append([_FUNCTION.format(c.completion) + c.element.parameters, c.completion + '(${1:%s})$0' % c.element.parameters[1:-1]])
            elif c.element.kind == ElementKind.GETTER or c.element.kind == ElementKind.FIELD:
                formatted.append([_PROPERTY.format(c.completion), c.completion])
            elif c.element.kind == ElementKind.CONSTRUCTOR:
                formatted.append([_CONSTRUCTOR.format(c.completion) + c.element.parameters, c.completion + '(${1:%s})$0' % c.element.parameters[1:-1]])
            else:
                formatted.append([_OTHER.format(c.completion), c.completion])

        actx.results = results.results
        actx.formatted_results = formatted

        if actx.results:
            show = True

    if not show:
        return

    v = get_active_view()
    if v:
        v.run_command('auto_complete')
