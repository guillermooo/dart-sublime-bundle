import re

import sublime
import sublime_plugin

from Dart import editor_context
from Dart.lib.notifications import show_info
from Dart.lib.notifications import show_error


class DartGoToDeclaration(sublime_plugin.WindowCommand):
    def run(self):
        try:
            view = self.window.active_view()
            if not view:
                return
        except Exception as e:
            return

        sel = view.sel()[0]        
        self.get_navigation(view, sel)

    def get_navigation(self, view, r):
        # FIXME(guillermooo): we may have a race condition here, or get info
        # for the wrong file.
        navigation = editor_context.navigation

        if not navigation:
            sublime.status_message('Dart: No navigation available.')
            return

        sources = navigation.regions

        # TODO(guillermooo): move this check to the generated API.
        targets = [source for source in sources
                        if source.offset <= r.begin() <= (source.offset + source.length)]

        if not targets:
            # FIXME(guillermooo): the callback may close an unrelated popup.
            show_info(view, "No navigations available at this location.", timeout=3000)
            sublime.status_message('Dart: No navigations available for the current location.')
            return

        first_target = targets[0].targets[0]
        first_target = navigation.targets[first_target]
        
        fname = navigation.files[first_target.fileIndex]
        row = first_target.startLine
        col = first_target.startColumn

        # XXX(guillermooo): can we optimize this for the current view?
        self.window.open_file("{}:{}:{}".format(fname, row, col), sublime.ENCODED_POSITION)


class ErrorNavigator(object):
    pattern = re.compile(r'^\w+\|\w+\|(?P<fname>.+)\|(?P<row>\d+)\|(?P<col>\d+)\|(?P<message>.+)$')

    def __init__(self, editor_context):
        self.editor_context = editor_context

    def next(self):
        self.editor_context.increment_error_index()

        data = self.editor_context.errors[self.editor_context.errors_index]
        match = self.pattern.match(data)

        return match.groupdict()['message']

    def previous(self):
        self.editor_context.decrement_error_index()

        data = self.editor_context.errors[self.editor_context.errors_index]
        match = self.pattern.match(data)

        return match.groupdict()['message']


class DartGoToNextResult(sublime_plugin.WindowCommand):
    def run(self):
        self.window.run_command('next_result')
        
        # todo(guillermo): check that the errors affect the current file.
        if editor_context.errors:
            navi = ErrorNavigator(editor_context)
            try:
                message = navi.next()
            except IndexError:
                return
            else:
                show_error(self.window.active_view(), message)


class DartGoToPrevResult(sublime_plugin.WindowCommand):
    def run(self):
        self.window.run_command('prev_result')
        
        # todo(guillermo): check that the errors affect the current file.
        if editor_context.errors:
            navi = ErrorNavigator(editor_context)
            try:
                message = navi.previous()
            except IndexError:
                return
            else:
                show_error(self.window.active_view(), message)
