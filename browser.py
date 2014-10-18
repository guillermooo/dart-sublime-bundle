# Copyright (c) 2014, Guillermo López-Anglada. Please see the AUTHORS file for details.
# All rights reserved. Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.)

import sublime
import sublime_plugin


from Dart.lib.sdk import SDK


class DartShowUserBrowsersCommand(sublime_plugin.WindowCommand):

    @property
    def browsers(self):
        sdk = SDK()
        browsers = sdk.user_browsers
        self.BROWSERS = [k for k in sorted(browsers.keys()) if
                               k != 'default']
        final = []
        for k in self.BROWSERS:
            final.append([k, '' if k != browsers['default'] else 'default'])
        return final

    def run(self):
        self.window.show_quick_panel(self.browsers, self.on_done)

    def on_done(self, idx):
        if idx == -1:
            return
        name = self.browsers[idx][0]

        sdk = SDK()
        sdk.path_to_default_user_browser = name
