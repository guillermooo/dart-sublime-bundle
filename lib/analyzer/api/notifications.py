from .types import *

class ConnectedNotification(object):
    def __init__(self, data):
        self.data = data

    def event(self):
        return 'connected'

    def longEvent(self):
        return 'server.connected'

class ErrorNotification(object):
    def __init__(self, data):
        self.data = data

    def event(self):
        return 'error'

    def longEvent(self):
        return 'server.error'

    @property
    def isFatal(self):
        return self.data['params']['isFatal']

    @property
    def message(self):
        return self.data['params']['message']

    @property
    def stackTrace(self):
        return self.data['params']['stackTrace']

class StatusNotification(object):
    def __init__(self, data):
        self.data = data

    def event(self):
        return 'status'

    def longEvent(self):
        return 'server.status'

    @property
    def analysis(self):
        return self.data['params']['analysis']

class ErrorsNotification(object):
    def __init__(self, data):
        self.data = data

    def event(self):
        return 'errors'

    def longEvent(self):
        return 'analysis.errors'

    @property
    def file(self):
        return self.data['params']['file']

    @property
    def errors(self):
        yield from [AnalysisError(d) for d in self.data['params']['errors']]

class FlushResultsNotification(object):
    def __init__(self, data):
        self.data = data

    def event(self):
        return 'flushResults'

    def longEvent(self):
        return 'analysis.flushResults'

    @property
    def files(self):
        yield from [FilePath(d) for d in self.data['params']['files']]

class FoldingNotification(object):
    def __init__(self, data):
        self.data = data

    def event(self):
        return 'folding'

    def longEvent(self):
        return 'analysis.folding'

    @property
    def file(self):
        return self.data['params']['file']

    @property
    def regions(self):
        yield from [FoldingRegion(d) for d in self.data['params']['regions']]

class HighlightsNotification(object):
    def __init__(self, data):
        self.data = data

    def event(self):
        return 'highlights'

    def longEvent(self):
        return 'analysis.highlights'

    @property
    def file(self):
        return self.data['params']['file']

    @property
    def regions(self):
        yield from [HighlightRegion(d) for d in self.data['params']['regions']]

class NavigationNotification(object):
    def __init__(self, data):
        self.data = data

    def event(self):
        return 'navigation'

    def longEvent(self):
        return 'analysis.navigation'

    @property
    def file(self):
        return self.data['params']['file']

    @property
    def regions(self):
        yield from [NavigationRegion(d) for d in self.data['params']['regions']]

class OccurrencesNotification(object):
    def __init__(self, data):
        self.data = data

    def event(self):
        return 'occurrences'

    def longEvent(self):
        return 'analysis.occurrences'

    @property
    def file(self):
        return self.data['params']['file']

    @property
    def occurrences(self):
        yield from [Occurrences(d) for d in self.data['params']['occurrences']]

class OutlineNotification(object):
    def __init__(self, data):
        self.data = data

    def event(self):
        return 'outline'

    def longEvent(self):
        return 'analysis.outline'

    @property
    def file(self):
        return self.data['params']['file']

    @property
    def outline(self):
        return self.data['params']['outline']

class OverridesNotification(object):
    def __init__(self, data):
        self.data = data

    def event(self):
        return 'overrides'

    def longEvent(self):
        return 'analysis.overrides'

    @property
    def file(self):
        return self.data['params']['file']

    @property
    def overrides(self):
        yield from [Override(d) for d in self.data['params']['overrides']]

class ResultsNotification(object):
    def __init__(self, data):
        self.data = data

    def event(self):
        return 'results'

    def longEvent(self):
        return 'completion.results'

    @property
    def id(self):
        return self.data['params']['id']

    @property
    def replacementOffset(self):
        return self.data['params']['replacementOffset']

    @property
    def replacementLength(self):
        return self.data['params']['replacementLength']

    @property
    def results(self):
        yield from [CompletionSuggestion(d) for d in self.data['params']['results']]

    @property
    def isLast(self):
        return self.data['params']['isLast']

class ResultsNotification(object):
    def __init__(self, data):
        self.data = data

    def event(self):
        return 'results'

    def longEvent(self):
        return 'search.results'

    @property
    def id(self):
        return self.data['params']['id']

    @property
    def results(self):
        yield from [SearchResult(d) for d in self.data['params']['results']]

    @property
    def isLast(self):
        return self.data['params']['isLast']

class LaunchDataNotification(object):
    def __init__(self, data):
        self.data = data

    def event(self):
        return 'launchData'

    def longEvent(self):
        return 'execution.launchData'

    @property
    def file(self):
        return self.data['params']['file']

    @property
    def kind(self):
        return self.data['params']['kind']

    @property
    def referencedFiles(self):
        yield from [FilePath(d) for d in self.data['params']['referencedFiles']]

