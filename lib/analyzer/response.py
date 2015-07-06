# Copyright (c) 2014, Guillermo López-Anglada. Please see the AUTHORS file for details.
# All rights reserved. Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.)

"""Responses from the analyzer.
"""

import queue

import sublime

from Dart.sublime_plugin_lib import PluginLogger

from Dart._init_ import editor_context
from Dart.lib.analyzer.api.protocol import AnalysisErrorsParams
from Dart.lib.analyzer.api.protocol import ServerGetVersionResult
from Dart.lib.analyzer.api.protocol import AnalysisNavigationParams
from Dart.lib.analyzer.api.protocol import CompletionGetSuggestionsResult
from Dart.lib.analyzer.api.protocol import CompletionResultsParams


_logger = PluginLogger(__name__)


class ResponseMaker(object):
    '''Transforms raw notifications and responses into `ServerResponse`s.
    '''

    def __init__(self, source):
        self.source = source

    def make(self):
        '''Makes `ServerResponse`s forever.
        '''
        while True:
            try:
                data = self.source.get()
            except queue.Empty:
                # unreachable?
                _logger.error('unexpected empty queue in ResponseMaker')
                yield
                continue

            if data.get('_internal'):
                _logger.info('ResponseMaker exiting by internal request')
                yield data
                break

            r = response_classifier(data)

            yield r


def is_result_id_response(data):
    return data.get('result', {}).get('id')


def is_server_version_response(data):
    return data.get('result', {}).get('version')


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


def is_completions_suggestions_result(data):
    return 'id' in data.get('result', {})


def response_classifier(data):
    # XXX: replace here XXX
    if is_errors_response(data):
        params = AnalysisErrorsParams.from_json(data['params'])
        return params.to_notification()

    if is_server_version_response(data):
        result = ServerGetVersionResult.from_json(data['result'])
        return result.to_response(data['id'])

    if is_navigation_notification(data):
        result = AnalysisNavigationParams.from_json(data['params'])
        return result.to_notification()

    if is_completion_results(data):
        result = CompletionResultsParams.from_json(data['params'])
        return result.to_notification()

    if is_completions_suggestions_result(data):
        result = CompletionGetSuggestionsResult.from_json(data['result'])
        return result.to_response(data['id'])

    return None
