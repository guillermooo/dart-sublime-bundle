# Copyright (c) 2014, Guillermo López-Anglada. Please see the AUTHORS file for details.
# All rights reserved. Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.)

from Dart import PluginLogger

_logger = PluginLogger(__name__)


class EventSource(object):
    ON_PUB_BUILD = 'on_pub_build_event'
    ON_DART_RUN = 'on_dart_run_event'
    ON_INSTALL = 'on_install_event'

    handlers = {
        ON_PUB_BUILD: [],
        ON_DART_RUN: [],        
    }
    
    def raise_event(self, source, name, *args, **kwargs):
        for handler in EventSource.handlers.get(name, []):
            handler(source.__class__.__qualname__, *args, **kwargs)

    def add_event_handler(self, name, func):
        if name not in EventSource.handlers:
            raise KeyError('unknown event "{}"'.format(name))
        if func not in EventSource.handlers[name]:
            EventSource.handlers[name].append(func)
