# Copyright (c) 2014, Guillermo López-Anglada. Please see the AUTHORS file for details.
# All rights reserved. Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.)

from threading import Lock
import os

import sublime

from .sublime import after


class OutputPanel(object):
    _write_lock = Lock()

    """Manages an ST output panel.

    Can be used as a file-like object.
    """

    def __init__(self, name,
                 base_dir=None,
                 syntax='Packages/Text/Plain text.tmLanguage',
                 **kwargs):
        """
        @name
          This panel's name.
        @base_dir
          Directory used to look files matched by regular expressions.
        @syntax:
          This panel's syntax.
        @kwargs
          Any number of settings to set in the underlying view via `.set()`.

          Common settings:
            - result_file_regex
            - result_line_regex
            - word_wrap
            - line_numbers
            - gutter
            - scroll_past_end
        """

        self.name = name
        self.window = sublime.active_window()

        if not hasattr(self, 'view'):
            # Try not to call get_output_panel until the regexes are assigned
            self.view = self.window.create_output_panel(self.name)

        # Default to the current file directory
        if (not base_dir and
                self.window.active_view() and
                self.window.active_view().file_name()):
            base_dir = os.path.dirname(self.window.active_view().file_name())

        self.set('result_base_dir', base_dir)
        self.set('syntax', syntax)

        self.set('result_file_regex', '')
        self.set('result_line_regex', '')
        self.set('word_wrap', False)
        self.set('line_numbers', False)
        self.set('gutter', False)
        self.set('scroll_past_end', False)

    def set(self, name, value):
        self.view.settings().set(name, value)

    def _clean_text(self, text):
        return text.replace('\r', '')

    def write(self, text):
        assert isinstance(text, str), 'must pass decoded text data'
        with OutputPanel._write_lock:
            do_write = lambda: self.view.run_command('append', {
                'characters': self._clean_text(text),
                'force': True,
                'scroll_to_end': True,
                })
            # XXX: If we don't sync with the GUI thread here, the command above
            # won't work if this method is called from .set_timeout_async().
            # BUG?
            after(0, do_write)

    def flush(self):
        pass

    def hide(self):
        self.window.run_command('hide_panel', {
            'panel': 'output.' + self.name})

    def show(self):
        # Call create_output_panel a second time after assigning the above
        # settings, so that it'll be picked up as a result buffer
        self.window.create_output_panel(self.name)
        self.window.run_command('show_panel', {
            'panel': 'output.' + self.name})

    def close(self):
        pass


# TOOD: fix this
class ErrorPanel(object):
    def __init__(self):
        self.panel = OutputPanel('dart.info')
        self.panel.write('=' * 80)
        self.panel.write('\n')
        self.panel.write("Dart - Something's not quite right\n")
        self.panel.write('=' * 80)
        self.panel.write('\n')
        self.panel.write('\n')

    def write(self, text):
        self.panel.write(text)

    def show(self):
        self.panel.show()


# TODO: move this to common plugin lib.
class ErrorsPanel(object):
    """
    A panel that displays errors and enables error navigation.
    """
    _sublime_syntax_file = None
    _tm_language_file = None
    _errors_pattern = ''
    _errors_template = ''

    _lock = Lock()

    def __init__(self, name):
        """
        @name
          The name of the underlying output panel.
        """
        self.name = name
        self._errors = []

    @property
    def errors(self):
        with self._lock:
            return self._errors

    @errors.setter
    def errors(self, value):
        with self._lock:
            self._errors = value

    @property
    def errors_pattern(self):
        """
        Subclasses can override this to provide a more suitable pattern to
        capture errors.
        """
        return self._errors_pattern

    @property
    def errors_template(self):
        """
        Subclasses can override this to provide a more suitable template to
        display errors.
        """
        return self._errors_template

    def display(self):
        if len(self.errors) == 0:
            panel = OutputPanel(self.name)
            panel.hide()
            return

        # Like this to avoid deadlock. XXX: Maybe use RLock instead?
        formatted = self.format()
        with self._lock:
            # XXX: If we store this panel as an instance member, it won't work.
            # Revise implementation.
            panel = OutputPanel(self.name)
            panel.set('result_file_regex', self.errors_pattern)
            # TODO: remove this when we don't support tmLanguage any more.
            if sublime.version() > '3083':
                panel.view.set_syntax_file(self._sublime_syntax_file)
            else:
                panel.view.set_syntax_file(self._tm_language_file)
            panel.write(formatted)
            # TODO(guillermooo): Do not show now if other panel is showing;
            # for example, the console.
            panel.show()

    def clear(self):
        self.errors = []

    def update(self, errors, sort_key=None):
        self.errors = list(sorted(errors, key=sort_key))

    def get_item_result_data(self, item):
        """
        Subclasses must implement this method.

        Must return a dictionary to be used as data for `errors_template`.
        """
        return {}

    def format(self):
        formatted = (self.errors_template.format(**self.get_item_result_data(e))
                for e in self.errors)
        return '\n'.join(formatted)
