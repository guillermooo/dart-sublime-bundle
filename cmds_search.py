# Copyright (c) 2014, Guillermo López-Anglada. Please see the AUTHORS file for details.
# All rights reserved. Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.)

'''Search commands.
'''

import sublime
import sublime_plugin

from Dart.sublime_plugin_lib import PluginLogger
from Dart import analyzer
from Dart.analyzer import g_editor_context

from Dart.lib.analyzer.api.api_types import NavigationTarget


_logger = PluginLogger(__name__)


class DartGoToDeclarationCommand(sublime_plugin.WindowCommand):
    '''Displays the top-level declarations.
    '''
    def run(self):
        _logger.info("finding top level decls")
        data = g_editor_context.navigation_info
        if not data:
            return

        pt = self.window.active_view().sel()[0].b
        regions = [r for r in data.regions if r.containsInclusive(pt)]

        if not regions:
            return

        if len(regions) > 1:
            print("XXX too many regions")
            return

        print ("RRR", regions[0].targets)
        # t = NavigationTarget.fromJson(regions[0].targets[0])
        # print (t.fileIndex) 


class DartFindReferences(sublime_plugin.WindowCommand):
    '''Displays the references of the given element.
    '''
    def run(self):
        if analyzer.g_server.ping():
            v = self.window.active_view()
            _logger.info("finding element references")
            analyzer.g_server.send_find_element_refs(v)
            return
