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


class ShowErrorsImpl(object):
    def compare_paths(self, path1, path2):
        return os.path.realpath(path1) == os.path.realpath(path2)

    def group(self, analysis_errors):
        infos = [ae for ae in analysis_errors if
                    (ae.severity == AnalysisErrorSeverity.INFO)
                    and (ae.type != AnalysisErrorType.TODO)]
        warns = [ae for ae in analysis_errors if (ae.severity == AnalysisErrorSeverity.WARNING)]
        erros = [ae for ae in analysis_errors if (ae.severity == AnalysisErrorSeverity.ERROR)]
        return infos, warns, erros

    def add_regions(self, v, info_regs, warn_regs, errs_regs):
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

    def error_to_region(self, view, error):
        '''Converts location data to region data.
        '''
        loc = error.location
        pt = view.text_point(loc.startLine - 1,
                             loc.startColumn - 1)
        return R(pt, pt + loc.length)

    def to_compact_text(self, error):
        return ("{error.severity}|{error.type}|{loc.file}|"
                "{loc.startLine}|{loc.startColumn}|{error.message}").format(
                                                error=error, loc=error.location)

    def __call__(self, errors):
        '''Show errors in the ui.

        @errors
          An instance of `ErrorInfoCollection`.
        '''
        view = get_active_view()

        # TODO(guillermooo): Use tokens to identify requests:file.
        if not self.compare_paths(errors.file, view.file_name()):
            _logger.debug('different view active - aborting')
            return

        panel = OutputPanel('dart.analyzer')

        analysis_errors = list(errors.errors)
        infos, warns, erros = self.group(analysis_errors)

        if not len(infos + warns + erros) > 0:
            clear_ui()
            panel.hide()
            return

        info_regs = [self.error_to_region(view, item) for item in infos]
        warn_regs = [self.error_to_region(view, item) for item in warns]
        errs_regs = [self.error_to_region(view, item) for item in erros]

        _logger.debug('displaying errors to the user')

        self.add_regions(view, info_regs, warn_regs, errs_regs)

        info_patts = [self.to_compact_text(item) for item in infos]
        warn_patts = [self.to_compact_text(item) for item in warns]
        errs_patts = [self.to_compact_text(item) for item in erros]

        all_errs = set(errs_patts + warn_patts + info_patts)

        # TODO(guillermooo): abstract out the panel stuff into a DartErrorPanel class.
        panel = OutputPanel('dart.analyzer')

        # Tried to use .sublime-settings for this, but it won't work well.
        errors_pattern = r'^\w+\|\w+\|(.+)\|(\d+)\|(\d+)\|(.+)$'
        panel.set('result_file_regex', errors_pattern)
        # Overwrite any previous text in the panel.
        panel.write('\n'.join(all_errs))

        # TODO(guillermooo): remove this when .sublime-syntax has been fully
        # adopted.
        if sublime.version() >= '3084':
            panel.view.set_syntax_file('Packages/Dart/Support/Analyzer Output.sublime-syntax')
        else:
            panel.view.set_syntax_file('Packages/Dart/Support/Analyzer Output.tmLanguage')

        editor_context.errors = all_errs
        panel.show()

        try:
            view.show(view.sel()[0])
        except IndexError:
            pass

        sublime.status_message("Dart: Errors found")


show_errors = ShowErrorsImpl()


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
