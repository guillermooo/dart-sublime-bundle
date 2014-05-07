import sublime
import sublime_plugin
import os
import subprocess
import threading
import re
import locale
from xml.etree import ElementTree

locale.setlocale(locale.LC_ALL, '')

GUTTER_Icon = {}
ULINE_Color = {}

SCOPES_Dartlint = {
    'dartlint.mark.error': {
        'flags':
        sublime.DRAW_EMPTY |
        sublime.DRAW_NO_OUTLINE |
        sublime.DRAW_NO_FILL |
        sublime.DRAW_SQUIGGLY_UNDERLINE |
        sublime.DRAW_EMPTY_AS_OVERWRITE,
        'style': '''
        <dict>
            <key>name</key>
            <string>Dartlint Error</string>
            <key>scope</key>
            <string>dartlint.mark.error</string>
            <key>settings</key>
            <dict>
                <key>foreground</key>
                <string>#{}</string>
            </dict>
        </dict>

    '''
    },
    'dartlint.mark.warning': {
        'flags':
        sublime.DRAW_EMPTY |
        sublime.DRAW_NO_OUTLINE |
        sublime.DRAW_NO_FILL |
        sublime.DRAW_SQUIGGLY_UNDERLINE |
        sublime.DRAW_EMPTY_AS_OVERWRITE,
        'style': '''
        <dict>
            <key>name</key>
            <string>Dartlint Warning</string>
            <key>scope</key>
            <string>dartlint.mark.warning</string>
            <key>settings</key>
            <dict>
                <key>foreground</key>
                <string>#{}</string>
            </dict>
        </dict>

    '''
    },
    'dartlint.mark.info': {
        'flags':
        sublime.DRAW_EMPTY |
        sublime.DRAW_NO_OUTLINE |
        sublime.DRAW_NO_FILL |
        sublime.DRAW_SQUIGGLY_UNDERLINE |
        sublime.DRAW_EMPTY_AS_OVERWRITE,
        'style': '''
        <dict>
            <key>name</key>
            <string>Dartlint Info</string>
            <key>scope</key>
            <string>dartlint.mark.info</string>
            <key>settings</key>
            <dict>
                <key>foreground</key>
                <string>#{}</string>
            </dict>
        </dict>

    '''
    },
    'dartlint.mark.gutter': {
        'flags':
        sublime.DRAW_EMPTY |
        sublime.DRAW_NO_OUTLINE |
        sublime.DRAW_NO_FILL |
        sublime.DRAW_EMPTY_AS_OVERWRITE,
        'style': '''
        <dict>
            <key>name</key>
            <string>Dartlint Gutter Mark</string>
            <key>scope</key>
            <string>dartlint.mark.gutter</string>
        </dict>

    '''
    }
}

THEME_Head = ('<?xml version="1.0" encoding="{}"?>\n'
              '<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"'
              ' "http://www.apple.com/DTDs/PropertyList-1.0.dtd">')

SHOW_Levels = {
    'INFO': 0,
    'WARNING': 1,
    'ERROR': 2
}


class DartLint(sublime_plugin.EventListener):
    def __init__(self, *args, **kwargs):
        sublime_plugin.EventListener.__init__(self, *args, **kwargs)
        print("Dartlint plugin loaded.")

    def on_post_save(self, view):
        self.check_theme(view)

        # Is the linter disabled?
        if not self.do_lint or not self.do_save:
            return

        fileName = view.file_name()
        if view.file_name().endswith('.dart') is False:
            return
        print("Dart lint: Running dartanalyzer on ", fileName)
        # run dartanalyzer in its own thread
        RunDartanalyzer(view, fileName, self.settings, True)

    def on_load(self, view):
        self.check_theme(view)

        # Is the linter or function disabled?
        if not self.do_lint or not self.do_load:
            return

        fileName = view.file_name()
        if view.file_name().endswith('.dart') is False:
            return
        print("Dart lint: Running dartanalyzer on ", fileName)
        # run dartanalyzer in its own thread
        RunDartanalyzer(view, fileName, self.settings, False)

    def check_theme(self, view):
        # Get some settings
        self.settings = view.settings()
        self.do_lint = self.settings.get('dartlint_active')
        self.do_save = self.settings.get('dartlint_on_save')
        self.do_load = self.settings.get('dartlint_on_load')
        self.do_modify = self.settings.get('dartlint_on_modify')
        error_color = self.settings.get('dartlint_underline_color_error')
        warn_color = self.settings.get('dartlint_underline_color_warning')
        info_color = self.settings.get('dartlint_underline_color_info')
        error_icon = self.settings.get('dartlint_gutter_icon_error')
        warn_icon = self.settings.get('dartlint_gutter_icon_warning')
        info_icon = self.settings.get('dartlint_gutter_icon_info')
        # Set the icons and colors in the file scope
        GUTTER_Icon.update({
            'dartlint_ERROR': error_icon,
            'dartlint_WARNING': warn_icon,
            'dartlint_INFO': info_icon})
        ULINE_Color.update({
            'dartlint.mark.error': error_color,
            'dartlint.mark.warning': warn_color,
            'dartlint.mark.info': info_color,
            'dartlint.mark.gutter': 'not used'})

        # Get the current theme
        system_prefs = sublime.load_settings('Preferences.sublime-settings')
        theme = system_prefs.get('color_scheme')
        theme_xml = sublime.load_resource(theme)
        append_xml = False
        append_scopes = []

        # Check for required scopes
        for scopes in SCOPES_Dartlint:
            if theme_xml.find(scopes) is -1:
                # append to xml
                append_xml = True
                append_scopes.append(scopes)
                print('%s not found in theme' % scopes)
        plist = ElementTree.XML(theme_xml)
        styles = plist.find('./dict/array')

        # Add missing elements
        if append_xml:
            for s2append in append_scopes:
                styles.append(
                    ElementTree.fromstring(
                        SCOPES_Dartlint[s2append]['style'].format(
                            ULINE_Color[s2append])))
        else:
            # No need to do anything
            return

        # write back to 'Packages/User/<theme> DL.tmTheme'
        original_name = os.path.splitext(os.path.basename(theme))[0]
        new_name = original_name + ' DL'
        theme_path = os.path.join(sublime.packages_path(),
                                  'User', new_name + '.tmTheme')
        with open(theme_path, 'w', encoding='utf8') as f:
            f.write(THEME_Head.format('UTF-8'))
            f.write(ElementTree.tostring(plist, encoding='unicode'))

        # Set the amended color scheme to the current color scheme
        path = os.path.join('User', os.path.basename(theme_path))
        prep_path = FormRelativePath(path)
        if prep_path is not False:
            system_prefs.set('color_scheme', prep_path)
            sublime.save_settings('Preferences.sublime-settings')
            print('Created: %s' % prep_path)


def FormRelativePath(path):
    new_path = '/'
    # Dir exists?
    if os.path.isabs(path) and \
            os.path.exists(os.path.dirname(path)) is False:
        print('%s Does not exist' % path)
        return False
    elif os.path.exists(os.path.join(sublime.packages_path(),
                        os.path.dirname(path))) is False:
        print('%s Does not exist' % os.path.join(sublime.packages_path(),
              os.path.dirname(path)))
        return False
    if os.path.isabs(path):
        new_path = os.path.relpath(path, sublime.packages_path())
    else:
        new_path = path
    # Preferences requires 'Packages' in the path
    new_path = os.path.join('Packages', new_path)
    return new_path


def RunDartanalyzer(view, fileName, our_settings, show_popup=True):
    dartsdk_path = our_settings.get('dartsdk_path')

    if dartsdk_path:
        DartLintThread(view, fileName, our_settings, show_popup).start()


class DartLintThread(threading.Thread):
    def __init__(self, view, fileName, our_settings, show_popup):
        super(DartLintThread, self).__init__()
        self.settings = our_settings
        self.show_popup = show_popup
        self.daemon = True
        self.view = view
        self.window = view.window()
        self.dartsdk_path = our_settings.get('dartsdk_path')
        self.fileName = fileName

    def run(self):
        analyzer_path = os.path.join(self.dartsdk_path, 'bin', 'dartanalyzer')
        # Clear all regions
        self.clear_all()
        if IsWindows():
            analyzer_path += '.bat'
        options = '--machine'
        proc = subprocess.Popen([analyzer_path, options, self.fileName],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            outs, errs = proc.communicate(timeout=15)
        except TimeoutExpired:
            proc.kill()
            outs, errs = proc.communicate()

        msg_pattern_machine = re.compile(
            r'^(?P<severity>\w+)\|(?P<type>\w+)\|(?P<code>\w+)\|'
            '(?P<file_name>.+)\|(?P<line>\d+)\|(?P<col>\d+)\|'
            '(?P<err_length>\d+)\|(?P<message>.+)')

        lines = errs.decode('UTF-8').split('\n')

        # Collect data needed to generate error messages
        lint_data = []
        lines_out = ''
        err_count = 0
        culp_regions = {}
        for line in lines:
            line_out = ''
            line_data = {}
            line_groups = msg_pattern_machine.match(line)
            if line_groups is not None:
                if line_groups.group('file_name') != self.fileName:
                    # output is for a different file
                    continue
                line_out = '%s: %s on line %s, col %s: %s\n' % \
                    (line_groups.group('severity'),
                     line_groups.group('code'),
                     line_groups.group('line'),
                     line_groups.group('col'),
                     line_groups.group('message'))

                line_data['severity'] = line_groups.group('severity')
                line_data['col'] = line_groups.group('col')
                line_data['line'] = line_groups.group('line')
                line_data['msg'] = line_groups.group('message')
                line_data['code'] = line_groups.group('code')
                line_data['type'] = line_groups.group('type')
                line_data['err_length'] = line_groups.group('err_length')
                line_data['lint_out'] = line_out
                line_data['line_pt'] = self.view.text_point(
                    int(line_data['line']) - 1, 0)
                line_data['point'] = self.view.text_point(
                    int(line_data['line']) - 1, int(line_data['col']))
                next_line = self.view.text_point(int(line_data['line']), 0)

                # Add a region (gutter mark and underline)
                if int(line_data['err_length']) > 0 and \
                        int(line_data['point']) + \
                        (int(line_data['err_length']) - 1) < next_line:
                    # Set the error region
                    line_data['culp_region'] = sublime.Region(
                        int(line_data['point']) - 1,
                        int(line_data['point']) +
                        (int(line_data['err_length']) - 1))
                else:
                    # Set the line as the error region
                    line_data['culp_region'] = self.view.line(
                        line_data['line_pt'])
                # Add the region to the apropriate region collection
                if ('dartlint_' + line_data['severity']) not in \
                        culp_regions.keys():
                    culp_regions['dartlint_%s' % line_data['severity']] = []
                culp_regions['dartlint_%s' % line_data['severity']].append(
                    line_data['culp_region'])
                lines_out += line_out
                lint_data.append(line_data)
                err_count += 1
        for reg_id in culp_regions.keys():
            # set the scope name
            reg_list = culp_regions[reg_id]
            this_scope = 'dartlint.mark.warning'
            if reg_id.endswith('ERROR') is True:
                this_scope = 'dartlint.mark.error'
            if reg_id.endswith('INFO') is True:
                this_scope = 'dartlint.mark.info'
            # Seperate gutter and underline regions
            gutter_reg = []
            for reg in reg_list:
                gutter_reg.append(self.view.line(reg.begin()))
            self.view.add_regions(
                reg_id + '_gutter',
                gutter_reg,
                # set this to this_scope for tinted gutter icons
                'dartlint.mark.gutter',
                icon=GUTTER_Icon[reg_id],
                flags=SCOPES_Dartlint['dartlint.mark.gutter']['flags'])
            self.view.add_regions(
                reg_id,
                reg_list,
                this_scope,
                flags=SCOPES_Dartlint[this_scope]['flags'])
            # Set icon presidence?
        if lines_out is '':
            self.output = None
            print('No errors.')
            self.view.set_status('dartlint', 'Dartlint: No errors')
        else:
            # Sort list
            idx = 0
            err_keys = []
            for entry in lint_data:
                line_val = '{0:{fill}{align}16}'.format(
                    entry['line'], fill='0', align='>')
                col_val = '{0:{fill}{align}16}'.format(
                    entry['col'], fill='0', align='>')
                list_val = '%s-%s-%s' % (line_val, col_val, str(idx))
                err_keys.append(list_val)
                idx += 1
            new_err_list = []
            err_keys.sort()
            for ek in err_keys:
                new_err_list.append(lint_data[int(ek.split('-')[2])])
            self.output = new_err_list
            # Out to console
            print('\n' + lines_out)
            # Output to a popup
            if self.show_popup:
                self.popup_errors(self.window, self.view, self.output)

    def popup_errors(self, window, view, ErrorData):
        # Process data into a list of errors
        window.focus_view(view)
        dd_list = []
        show_this = False
        show_level = self.settings.get('dartlint_show_popup_level')
        level_value = 1000
        if show_level in SHOW_Levels:
            level_value = SHOW_Levels[show_level]

        for entry in ErrorData:
            this_level = -1
            if entry['severity'] in SHOW_Levels:
                this_level = SHOW_Levels[entry['severity']]
            if this_level >= level_value:
                show_this = True
            dd_list.append(entry['lint_out'])
        if show_this:
            window.show_quick_panel(
                dd_list,
                on_select=self.goto_error,
                on_highlight=self.show_error)

    def show_error(self, index):
        this_error = self.output[index]
        self.view.show_at_center(this_error['point'])

    def goto_error(self, index):
        this_error = self.output[index]
        self.view.sel().clear()
        end_point = int(this_error['point']) + \
            int(this_error['err_length']) - 1
        self.view.sel().add(sublime.Region(end_point, end_point))
        self.view.show_at_center(this_error['point'])

    def clear_all(self):
        for region_name in \
                ('dartlint_INFO', 'dartlint_WARNING', 'dartlint_ERROR'):
            self.view.erase_regions(region_name)
            self.view.erase_regions(region_name + '_gutter')


def IsWindows():
        return sublime.platform() == 'windows'
