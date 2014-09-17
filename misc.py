import sublime_plugin
import sublime

import webbrowser
import os

from . import PluginLogger
from .lib.sdk import SDK
from .lib.panels import OutputPanel


_logger = PluginLogger(__name__)

def plugin_loaded():
    # TODO(guillermooo): Remove this by 1.0
    transplant_settings('Preferences.sublime-settings',
                        'Dart - Plugin Settings.sublime-settings')


# TODO(guillermooo): Remove this by 1.0
omg_message = '''
 ____                              _
/ ___| _   _  ___ ___ ___  ___ ___| |
\___ \| | | |/ __/ __/ _ \/ __/ __| |
 ___) | |_| | (_| (_|  __/\__ \__ \_|
|____/ \__,_|\___\___\___||___/___(_)
'''


# TODO(guillermooo): Remove this by 1.0
def transplant_settings(old_fname, new_fname):
    '''Copies settings from @old_fname to @new_fname. Leaves obsolete settings
    in @old_fname intact.

    @old_fname
      Basename of a .sublime-settings file.

    @new_fname
      Basename of a .sublime-settings file.
    '''
    if os.path.exists(os.path.join(sublime.packages_path(), 'User',
                      new_fname)):
        _logger.debug('new User settings file found, not transplating old settings')
        return

    _logger.debug('Transplanting old settings to new settings file...')

    KNOWN_SETTINGS =  {
    "dart_sdk_path": None,
    "dart_dartium_path": None,

    "dart_user_browsers": { },

    "dart_linter_active": False,
    "dart_linter_on_load": True,
    "dart_linter_on_save": True,
    "dart_linter_show_popup_level": "WARNING",

    "dart_linter_gutter_icon_error": "Packages/Dart/gutter/dartlint-simple-error.png",
    "dart_linter_gutter_icon_warning": "Packages/Dart/gutter/dartlint-simple-warning.png",
    "dart_linter_gutter_icon_info": "Packages/Dart/gutter/dartlint-simple-info.png",

    "dart_linter_underline_color_error": "C7321C",
    "dart_linter_underline_color_warning": "F18512",
    "dart_linter_underline_color_info": "0000FC",

    "dart_log_level": "error"
    }

    try:
        old_settings = sublime.load_settings(old_fname)
        new_settings = sublime.load_settings(new_fname)
        for name, default in KNOWN_SETTINGS.items():
            value = old_settings.get(name, default)
            _logger.info("Transplanting: %s: %s", name, default)
            new_settings.set(name, value)
        sublime.save_settings(new_fname)
    except Exception as e:
        _logger.error('something went wrong while transplanting old settings')
        _logger.error(e)
        print("Dart: Something went wrong while transplanting old settings :_[")
        print("=" * 80)
        print(e)
        print("=" * 80)
    else:
        _logger.debug("old settings transplanted from %s to %s", old_fname, new_fname)
        print("Dart: Old settings transplanted from %s to %s" % (old_fname,
              new_fname))
        message = OutputPanel("dart.message")
        message.write("Dart Package for Sublime Text - Message\n")
        message.write("=" * 80)
        message.write(omg_message)
        message.write('\n')
        message.write("The Dart package for Sublime Text now uses different settings files.\n")
        message.write('\n')
        message.write("Your old Dart settings have been copied to '%s'." % new_fname)
        message.write(" We'll use this new file from now on.\n")
        message.write("Old settings have not been cleaned up. Please do so in '%s'" % old_fname)
        message.write(" if you want.\n")
        message.write('\n')
        message.write('Check our wiki for more information:\n')
        message.write('    https://github.com/dart-lang/dart-sublime-bundle/wiki\n')
        message.write('\n')
        message.write("Now please restart Sublime Text and we're all done!\n")
        message.write('\n')
        message.write("Thanks! :-)")
        message.show()


# TODO(guillermooo): we probably don't need a new command; ST already includes
# one by default.
class DartOpenBrowserCommand(sublime_plugin.WindowCommand):
    """Opens API reference in default browser.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, url):
        webbrowser.open_new_tab(url)


class DartOpenSettingsCommand(sublime_plugin.WindowCommand):
    """Opens Dart settings files.

    a) Default settings (that is, Packages/Dart/Support/Dart - Plugin Settings.sublime-settings).
    b) User settings (that is, Packages/User/Dart - Plugin Settings.sublime-settings).
    c) Dart file type settings (that is, Packages/User/Dart.sublime-settings)

    (a) is read-only and users should not rely on it, as it can be overwritten
        by ST or this plugin at any time withouth notice. Provides defaults and
        documentation.
    (b) user-editable version of (a). This is where users should store their
        settings.
    (c) Controls aspects closely related to .dart files: white space, tab size,
        etc.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def file_type_settings(self):
        '''Returns the full path to the Dart fyle type settings file.

        Note: ST accepts file type settings files in many locations, so
        conflicts may arise. For example, if the user had both:
          - Packages/User/Dart.sublime-settings, and
          - Packages/User/SomeSubDir/Dart.sublime-settings
        '''
        path = os.path.join(sublime.packages_path(),
                            'User/Dart.sublime-settings')
        if not os.path.exists(path):
            _logger.debug('Creating user settings file at: %s', path)
            with open(path, 'w') as f:
                f.write('{\n\t\n}')
        return path

    def run(self, kind='user', scope='global'):
        """
        @kind:
          Any of (user, default).

        @scope:
          Any of (global, file_type).
        """
        if kind == 'default':
            if scope == 'global':
                _logger.debug('Opening default settings for viewing only.')
                self.open_default()
                return
            _logger(
                'Default file type settings file requested. Such file does not exist.')
            return

        if kind != 'user':
            _logger.error('Unsupported settings type: %s', kind)
            return

        # User settings (Packages/User/*.sublime-settings)

        if scope == 'file_type':
            try:
                self.window.open_file(self.file_type_settings)
                return
            except OSError as e:
                _logger.error(
                    'Unexpected error while trying to open User file type settings')
                _logger.error(e)
                _logger.error('=' * 80)
                return

        self.window.run_command('open_file', {
            "file": "${packages}/User/Dart - Plugin Settings.sublime-settings"
            })

    def open_default(self):
        """Prints the default settings for Dart to a read-only view. The user
        should not edit their settings here, but use the 'User' version instead.
        """
        setts = sublime.load_resource(
            'Packages/Dart/Support/Dart - Plugin Settings.sublime-settings')

        v = self.window.new_file()
        v.run_command('append', {'characters': setts.replace('\r', '')})
        v.set_name('Dart Settings - Default (read-only)')
        # TODO(guillermooo): ST should detect that this is a JSON file by
        # looking at the extension, but it isn't the case. Check with
        # Sublime HQ. For now, set the syntax manually.
        v.set_syntax_file('Packages/JavaScript/JSON.tmLanguage')
        v.set_scratch(True)
        v.set_read_only(True)
