# Copyright (c) 2014, Guillermo López-Anglada. Please see the AUTHORS file for details.
# All rights reserved. Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.)

"""Responses from the analyzer.
"""

import queue

import sublime

from Dart.sublime_plugin_lib import PluginLogger
from Dart.sublime_plugin_lib.sublime import get_active_view

from Dart.lib.analyzer.api.protocol import AnalysisErrorsParams
from Dart.lib.analyzer.api.protocol import AnalysisNavigationParams
from Dart.lib.analyzer.api.protocol import CompletionGetSuggestionsResult
from Dart.lib.analyzer.api.protocol import CompletionResultsParams
from Dart.lib.analyzer.api.protocol import ServerGetVersionResult
from Dart.lib.analyzer.api.protocol import EditFormatResult


_logger = PluginLogger(__name__)


class ResponseMaker(object):
    '''
    Transforms raw notifications and responses into `Response`s.
    '''

    def __init__(self, server):
        self.server = server

    def make(self):
        '''Makes `ServerResponse`s forever.
        '''
        while True:
            try:
                data = self.server.responses.get()
            except queue.Empty:
                # unreachable?
                _logger.error('unexpected empty queue in ResponseMaker')
                yield
                continue
            else:
                if data.get('_internal'):
                    _logger.info('ResponseMaker exiting by internal request')
                    yield data
                    break

                view = get_active_view()
                if self.server.request_ids.validate(view, data):
                    yield self.make_request(view, data)
                    continue

                yield event_classifier(data)

    # TODO(guillermooo): change this name
    def make_request(self, view, data):
        view_id = view.id()
        request_id = data['id']
        response_type = self.server.request_ids.get_response_type(view, request_id)

        # TODO(guillermooo): encapsulate this in RequestIdManager too?
        if hasattr(response_type, 'from_json'):
            r = response_type.from_json(data.get('result'))
            return r.to_response(request_id)
        else:
            return response_type().to_response(request_id)

    def validate(self, view, data):
        return view and (data.get('id') in self.server.request_ids[view.id()])


def is_result_response(data):
    return data.get('event') == 'search.results'


def is_errors_response(data):
    return data.get('event') == 'analysis.errors'


def is_internal_response(data):
    return '_internal' in data


def is_navigation_notification(data):
    return 'analysis.navigation' == data.get('event')


def is_completion_results(data):
    return 'completion.results' == data.get('event')


def event_classifier(data):
    if is_errors_response(data):
        params = AnalysisErrorsParams.from_json(data['params'])
        return params.to_notification()

    if is_navigation_notification(data):
        result = AnalysisNavigationParams.from_json(data['params'])
        return result.to_notification()

    if is_completion_results(data):
        result = CompletionResultsParams.from_json(data['params'])
        return result.to_notification()

    return None
