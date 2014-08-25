'''This module is intended to run first when the different plugins load.

It should perform a basic status check so that we can catch severe
configuration errors early on and report them to the user.
'''

import sublime
import sublime_plugin

from Dart.lib.sdk import SDK
from Dart.lib.panels import OutputPanel
from Dart.lib.error import FatalConfigError


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
    try:
        SDK()
    except FatalConfigError as e:
        sublime.active_window().run_command('_dart_report_config_errors', {
            'message': str(e)
            })


def plugin_loaded():
    check()


class _dart_report_config_errors(sublime_plugin.WindowCommand):
    def run(self, message):
        v = OutputPanel('dart.config.check')
        text = HEADING + '\n'
        text += ('=' * 80) + '\n'
        text += 'MESSAGE:\n'
        text += message + '\n'
        text += '\n'
        text += 'CONFIGURATION:\n'
        text += ('-' * 80) + '\n'
        text += "editor version: {} ({})".format(sublime.version(),
                                               sublime.channel())
        text += '\n'
        text += ('-' * 80) + '\n'
        text += "os: {} ({})".format(sublime.platform(),
                                   sublime.arch())
        text += '\n'
        text += ('-' * 80) + '\n'

        setts = sublime.load_settings('Preferences.sublime-settings')
        text += "dart_sdk_path: {}".format(setts.get('dart_sdk_path'))
        text += '\n'

        text += '=' * 80

        v.write(text)
        v.show()
