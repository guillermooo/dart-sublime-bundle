'''This module is intended to run first when the different plugins load.

It should perform a basic status check so that we can catch severe
configuration errors early on and report them to the user.
'''

import sublime
import sublime_plugin

from Dart.lib.sdk import SDK
from Dart.lib.panels import OutputPanel


HEADING = '''
  ___                        _
 / _ \  ___   ___  _ __  ___| |
| | | |/ _ \ / _ \| '_ \/ __| |
| |_| | (_) | (_) | |_) \__ \_|
 \___/ \___/ \___/| .__/|___(_)
                  |_|

Something went wrong... :-[

This is an automatic report from the Sublime Text Dart package.

If you're having trouble to run this package, please open an issue in our
issue tracker[1] and paste as much information as possible from the report
below.

[1] https://github.com/dart-lang/dart-sublime-bundle/issues

'''


def check():
    errs = SDK().check()
    if errs:
        sublime.active_window().run_command('_dart_report_config_errors', {
            'errors': errs
            })


def plugin_loaded():
    check()


class _dart_report_config_errors(sublime_plugin.WindowCommand):
    def run(self, errors):
        v = OutputPanel('dart.config.check')
        text = HEADING + '\n'
        text += ('=' * 80) + '\n'
        for err in errors:
            text += 'MESSAGE:\n'
            text += err['message'] + '\n'
            text += '\n'

            text += 'CONFIGURATION:\n'
            text += ('-' * 80) + '\n'
            for name, value in err['configuration'].items():
                text += '{}: {}\n'.format(name, value)
                text += ('-' * 80) + '\n'

            text += '=' * 80

        v.write(text)
        v.show()
