# Copyright (c) 2014, the Dart project authors.  Please see the AUTHORS file
# for details. All rights reserved. Use of this source code is governed by a
# BSD-style license that can be found in the LICENSE file.
#
# This file has been automatically generated.  Please do not edit it manually.
# To regenerate the file, use the script
# "pkg/analysis_server/tool/spec/generate_files".


from .api_types import *

class Notification(object):
   """
   Base class for all notifications.
   """

class ServerConnectedNotification(Notification):
  """
  Reports that the server is running. This notification is issued once after
  the server has started running but before any requests are processed to let
  the client know that it started correctly.

  It is not possible to subscribe to or unsubscribe from this notification.
  """

  def __init__(self, data):
    self.data = data

  @property
  def event(self):
    return self.data.get('event')

class ServerErrorNotification(Notification):
  """
  Reports that an unexpected error has occurred while executing the server.
  This notification is not used for problems with specific requests (which are
  returned as part of the response) but is used for exceptions that occur while
  performing other tasks, such as analysis or preparing notifications.

  It is not possible to subscribe to or unsubscribe from this notification.
  """

  def __init__(self, data):
    self.data = data

  @property
  def event(self):
    return self.data.get('event')

  @property
  def isFatal(self):
    return self.data['params'].get('isFatal')

  @property
  def message(self):
    return self.data['params'].get('message')

  @property
  def stackTrace(self):
    return self.data['params'].get('stackTrace')

class ServerStatusNotification(Notification):
  """
  Reports the current status of the server. Parameters are omitted if there has
  been no change in the status represented by that parameter.

  This notification is not subscribed to by default. Clients can subscribe by
  including the value "STATUS" in the list of services passed in a
  server.setSubscriptions request.
  """

  def __init__(self, data):
    self.data = data

  @property
  def analysis(self):
    return AnalysisStatus.fromJson(self.data['params'].get('analysis'))

  @property
  def event(self):
    return self.data.get('event')

  @property
  def pub(self):
    return PubStatus.fromJson(self.data['params'].get('pub'))

class AnalysisErrorsNotification(Notification):
  """
  Reports the errors associated with a given file. The set of errors included
  in the notification is always a complete list that supersedes any previously
  reported errors.

  It is only possible to unsubscribe from this notification by using the
  command-line flag --no-error-notification.
  """

  def __init__(self, data):
    self.data = data

  @property
  def errors(self):
    yield from [AnalysisError.fromJson(x) for x in self.data['params'].get('errors')]

  @property
  def event(self):
    return self.data.get('event')

  @property
  def file(self):
    return self.data['params'].get('file')

class AnalysisFlushResultsNotification(Notification):
  """
  Reports that any analysis results that were previously associated with the
  given files should be considered to be invalid because those files are no
  longer being analyzed, either because the analysis root that contained it is
  no longer being analyzed or because the file no longer exists.

  If a file is included in this notification and at some later time a
  notification with results for the file is received, clients should assume
  that the file is once again being analyzed and the information should be
  processed.

  It is not possible to subscribe to or unsubscribe from this notification.
  """

  def __init__(self, data):
    self.data = data

  @property
  def event(self):
    return self.data.get('event')

  @property
  def files(self):
    yield from [x for x in self.data['params'].get('files')]

class AnalysisFoldingNotification(Notification):
  """
  Reports the folding regions associated with a given file. Folding regions can
  be nested, but will not be overlapping. Nesting occurs when a foldable
  element, such as a method, is nested inside another foldable element such as
  a class.

  This notification is not subscribed to by default. Clients can subscribe by
  including the value "FOLDING" in the list of services passed in an
  analysis.setSubscriptions request.
  """

  def __init__(self, data):
    self.data = data

  @property
  def event(self):
    return self.data.get('event')

  @property
  def file(self):
    return self.data['params'].get('file')

  @property
  def regions(self):
    yield from [FoldingRegion.fromJson(x) for x in self.data['params'].get('regions')]

class AnalysisHighlightsNotification(Notification):
  """
  Reports the highlight regions associated with a given file.

  This notification is not subscribed to by default. Clients can subscribe by
  including the value "HIGHLIGHTS" in the list of services passed in an
  analysis.setSubscriptions request.
  """

  def __init__(self, data):
    self.data = data

  @property
  def event(self):
    return self.data.get('event')

  @property
  def file(self):
    return self.data['params'].get('file')

  @property
  def regions(self):
    yield from [HighlightRegion.fromJson(x) for x in self.data['params'].get('regions')]

class AnalysisInvalidateNotification(Notification):
  """
  Reports that the navigation information associated with a region of a single
  file has become invalid and should be re-requested.

  This notification is not subscribed to by default. Clients can subscribe by
  including the value "INVALIDATE" in the list of services passed in an
  analysis.setSubscriptions request.
  """

  def __init__(self, data):
    self.data = data

  @property
  def delta(self):
    return self.data['params'].get('delta')

  @property
  def event(self):
    return self.data.get('event')

  @property
  def file(self):
    return self.data['params'].get('file')

  @property
  def length(self):
    return self.data['params'].get('length')

  @property
  def offset(self):
    return self.data['params'].get('offset')

class AnalysisNavigationNotification(Notification):
  """
  Reports the navigation targets associated with a given file.

  This notification is not subscribed to by default. Clients can subscribe by
  including the value "NAVIGATION" in the list of services passed in an
  analysis.setSubscriptions request.
  """

  def __init__(self, data):
    self.data = data

  @property
  def event(self):
    return self.data.get('event')

  @property
  def file(self):
    return self.data['params'].get('file')

  @property
  def files(self):
    yield from [x for x in self.data['params'].get('files')]

  @property
  def regions(self):
    yield from [NavigationRegion.fromJson(x) for x in self.data['params'].get('regions')]

  @property
  def targets(self):
    yield from [NavigationTarget.fromJson(x) for x in self.data['params'].get('targets')]

class AnalysisOccurrencesNotification(Notification):
  """
  Reports the occurrences of references to elements within a single file.

  This notification is not subscribed to by default. Clients can subscribe by
  including the value "OCCURRENCES" in the list of services passed in an
  analysis.setSubscriptions request.
  """

  def __init__(self, data):
    self.data = data

  @property
  def event(self):
    return self.data.get('event')

  @property
  def file(self):
    return self.data['params'].get('file')

  @property
  def occurrences(self):
    yield from [Occurrences.fromJson(x) for x in self.data['params'].get('occurrences')]

class AnalysisOutlineNotification(Notification):
  """
  Reports the outline associated with a single file.

  This notification is not subscribed to by default. Clients can subscribe by
  including the value "OUTLINE" in the list of services passed in an
  analysis.setSubscriptions request.
  """

  def __init__(self, data):
    self.data = data

  @property
  def event(self):
    return self.data.get('event')

  @property
  def file(self):
    return self.data['params'].get('file')

  @property
  def outline(self):
    return Outline.fromJson(self.data['params'].get('outline'))

class AnalysisOverridesNotification(Notification):
  """
  Reports the overridding members in a file.

  This notification is not subscribed to by default. Clients can subscribe by
  including the value "OVERRIDES" in the list of services passed in an
  analysis.setSubscriptions request.
  """

  def __init__(self, data):
    self.data = data

  @property
  def event(self):
    return self.data.get('event')

  @property
  def file(self):
    return self.data['params'].get('file')

  @property
  def overrides(self):
    yield from [Override.fromJson(x) for x in self.data['params'].get('overrides')]

class CompletionResultsNotification(Notification):
  """
  Reports the completion suggestions that should be presented to the user. The
  set of suggestions included in the notification is always a complete list
  that supersedes any previously reported suggestions.
  """

  def __init__(self, data):
    self.data = data

  @property
  def event(self):
    return self.data.get('event')

  @property
  def id(self):
    return CompletionId.fromJson(self.data['params'].get('id'))

  @property
  def isLast(self):
    return self.data['params'].get('isLast')

  @property
  def replacementLength(self):
    return self.data['params'].get('replacementLength')

  @property
  def replacementOffset(self):
    return self.data['params'].get('replacementOffset')

  @property
  def results(self):
    yield from [CompletionSuggestion.fromJson(x) for x in self.data['params'].get('results')]

class SearchResultsNotification(Notification):
  """
  Reports some or all of the results of performing a requested search. Unlike
  other notifications, this notification contains search results that should be
  added to any previously received search results associated with the same
  search id.
  """

  def __init__(self, data):
    self.data = data

  @property
  def event(self):
    return self.data.get('event')

  @property
  def id(self):
    return SearchId.fromJson(self.data['params'].get('id'))

  @property
  def isLast(self):
    return self.data['params'].get('isLast')

  @property
  def results(self):
    yield from [SearchResult.fromJson(x) for x in self.data['params'].get('results')]

class ExecutionLaunchDataNotification(Notification):
  """
  Reports information needed to allow a single file to be launched.

  This notification is not subscribed to by default. Clients can subscribe by
  including the value "LAUNCH_DATA" in the list of services passed in an
  execution.setSubscriptions request.
  """

  def __init__(self, data):
    self.data = data

  @property
  def event(self):
    return self.data.get('event')

  @property
  def file(self):
    return self.data['params'].get('file')

  @property
  def kind(self):
    return self.data['params'].get('kind')

  @property
  def referencedFiles(self):
    yield from [x for x in self.data['params'].get('referencedFiles')]

