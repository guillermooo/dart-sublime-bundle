from .types import *

class SetSubscriptionsResponse(object):
    def __init__(self, data):
        self.data = data

    @property
    def response_id(self):
        return self.data['id']

    @property
    def error(self):
        return ResponseError(self.data['error'])

class GetErrorsResponse(object):
    def __init__(self, data):
        self.data = data

    @property
    def response_id(self):
        return self.data['id']

    @property
    def error(self):
        return ResponseError(self.data['error'])

    @property
    def errors(self):
        yield from [AnalysisError(d) for d in self.data['result']['errors']]

class GetHoverResponse(object):
    def __init__(self, data):
        self.data = data

    @property
    def response_id(self):
        return self.data['id']

    @property
    def error(self):
        return ResponseError(self.data['error'])

    @property
    def hovers(self):
        yield from [HoverInformation(d) for d in self.data['result']['hovers']]

class SetAnalysisRootsResponse(object):
    def __init__(self, data):
        self.data = data

    @property
    def response_id(self):
        return self.data['id']

    @property
    def error(self):
        return ResponseError(self.data['error'])

class SetPriorityFilesResponse(object):
    def __init__(self, data):
        self.data = data

    @property
    def response_id(self):
        return self.data['id']

    @property
    def error(self):
        return ResponseError(self.data['error'])

class SetSubscriptionsResponse(object):
    def __init__(self, data):
        self.data = data

    @property
    def response_id(self):
        return self.data['id']

    @property
    def error(self):
        return ResponseError(self.data['error'])

class UpdateContentResponse(object):
    def __init__(self, data):
        self.data = data

    @property
    def response_id(self):
        return self.data['id']

    @property
    def error(self):
        return ResponseError(self.data['error'])

class UpdateOptionsResponse(object):
    def __init__(self, data):
        self.data = data

    @property
    def response_id(self):
        return self.data['id']

    @property
    def error(self):
        return ResponseError(self.data['error'])

class GetSuggestionsResponse(object):
    def __init__(self, data):
        self.data = data

    @property
    def response_id(self):
        return self.data['id']

    @property
    def error(self):
        return ResponseError(self.data['error'])

    @property
    def id(self):
        return self.data['result']['id']

class FindElementReferencesResponse(object):
    def __init__(self, data):
        self.data = data

    @property
    def response_id(self):
        return self.data['id']

    @property
    def error(self):
        return ResponseError(self.data['error'])

    @property
    def id(self):
        return self.data['result']['id']

    @property
    def element(self):
        return self.data['result']['element']

class FindMemberDeclarationsResponse(object):
    def __init__(self, data):
        self.data = data

    @property
    def response_id(self):
        return self.data['id']

    @property
    def error(self):
        return ResponseError(self.data['error'])

    @property
    def id(self):
        return self.data['result']['id']

class FindMemberReferencesResponse(object):
    def __init__(self, data):
        self.data = data

    @property
    def response_id(self):
        return self.data['id']

    @property
    def error(self):
        return ResponseError(self.data['error'])

    @property
    def id(self):
        return self.data['result']['id']

class FindTopLevelDeclarationsResponse(object):
    def __init__(self, data):
        self.data = data

    @property
    def response_id(self):
        return self.data['id']

    @property
    def error(self):
        return ResponseError(self.data['error'])

    @property
    def id(self):
        return self.data['result']['id']

class GetTypeHierarchyResponse(object):
    def __init__(self, data):
        self.data = data

    @property
    def response_id(self):
        return self.data['id']

    @property
    def error(self):
        return ResponseError(self.data['error'])

    @property
    def hierarchyItems(self):
        yield from [TypeHierarchyItem(d) for d in self.data['result']['hierarchyItems']]

class GetAssistsResponse(object):
    def __init__(self, data):
        self.data = data

    @property
    def response_id(self):
        return self.data['id']

    @property
    def error(self):
        return ResponseError(self.data['error'])

    @property
    def assists(self):
        yield from [SourceChange(d) for d in self.data['result']['assists']]

class GetAvailableRefactoringsResponse(object):
    def __init__(self, data):
        self.data = data

    @property
    def response_id(self):
        return self.data['id']

    @property
    def error(self):
        return ResponseError(self.data['error'])

    @property
    def kinds(self):
        yield from [RefactoringKind(d) for d in self.data['result']['kinds']]

class GetFixesResponse(object):
    def __init__(self, data):
        self.data = data

    @property
    def response_id(self):
        return self.data['id']

    @property
    def error(self):
        return ResponseError(self.data['error'])

    @property
    def fixes(self):
        yield from [AnalysisErrorFixes(d) for d in self.data['result']['fixes']]

class GetRefactoringResponse(object):
    def __init__(self, data):
        self.data = data

    @property
    def response_id(self):
        return self.data['id']

    @property
    def error(self):
        return ResponseError(self.data['error'])

    @property
    def initialProblems(self):
        yield from [RefactoringProblem(d) for d in self.data['result']['initialProblems']]

    @property
    def optionsProblems(self):
        yield from [RefactoringProblem(d) for d in self.data['result']['optionsProblems']]

    @property
    def finalProblems(self):
        yield from [RefactoringProblem(d) for d in self.data['result']['finalProblems']]

    @property
    def feedback(self):
        return self.data['result']['feedback']

    @property
    def change(self):
        return self.data['result']['change']

    @property
    def potentialEdits(self):
        yield from self.data['result']['potentialEdits']

class SortMembersResponse(object):
    def __init__(self, data):
        self.data = data

    @property
    def response_id(self):
        return self.data['id']

    @property
    def error(self):
        return ResponseError(self.data['error'])

    @property
    def edit(self):
        return self.data['result']['edit']

class CreateContextResponse(object):
    def __init__(self, data):
        self.data = data

    @property
    def response_id(self):
        return self.data['id']

    @property
    def error(self):
        return ResponseError(self.data['error'])

    @property
    def id(self):
        return self.data['result']['id']

class DeleteContextResponse(object):
    def __init__(self, data):
        self.data = data

    @property
    def response_id(self):
        return self.data['id']

    @property
    def error(self):
        return ResponseError(self.data['error'])

class MapUriResponse(object):
    def __init__(self, data):
        self.data = data

    @property
    def response_id(self):
        return self.data['id']

    @property
    def error(self):
        return ResponseError(self.data['error'])

    @property
    def file(self):
        return self.data['result']['file']

    @property
    def uri(self):
        return self.data['result']['uri']

class SetSubscriptionsResponse(object):
    def __init__(self, data):
        self.data = data

    @property
    def response_id(self):
        return self.data['id']

    @property
    def error(self):
        return ResponseError(self.data['error'])

