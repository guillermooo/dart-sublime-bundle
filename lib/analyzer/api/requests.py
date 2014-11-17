class GetVersionRequest(object):
    def __init__(self, request_id, **kwargs):
        self.method = "server.getVersion"
        self.request_id = request_id

class ShutdownRequest(object):
    def __init__(self, request_id, **kwargs):
        self.method = "server.shutdown"
        self.request_id = request_id

class SetSubscriptionsRequest(object):
    def __init__(self, request_id, **kwargs):
        self.method = "server.setSubscriptions"
        self.request_id = request_id
        self.subscriptions = kwargs['subscriptions']

    def to_dict(self):
        return {
            "id": self.request_id,
            "method": self.method,
            "params": {
                "subscriptions": self.subscriptions,
                }
            }

class GetErrorsRequest(object):
    def __init__(self, request_id, **kwargs):
        self.method = "analysis.getErrors"
        self.request_id = request_id
        self.file = kwargs['file']

    def to_dict(self):
        return {
            "id": self.request_id,
            "method": self.method,
            "params": {
                "file": self.file,
                }
            }

class GetHoverRequest(object):
    def __init__(self, request_id, **kwargs):
        self.method = "analysis.getHover"
        self.request_id = request_id
        self.file = kwargs['file']
        self.offset = kwargs['offset']

    def to_dict(self):
        return {
            "id": self.request_id,
            "method": self.method,
            "params": {
                "file": self.file,
                "offset": self.offset,
                }
            }

class ReanalyzeRequest(object):
    def __init__(self, request_id, **kwargs):
        self.method = "analysis.reanalyze"
        self.request_id = request_id

class SetAnalysisRootsRequest(object):
    def __init__(self, request_id, **kwargs):
        self.method = "analysis.setAnalysisRoots"
        self.request_id = request_id
        self.included = kwargs['included']
        self.excluded = kwargs['excluded']
        self.packageRoots = kwargs['packageRoots']

    def to_dict(self):
        return {
            "id": self.request_id,
            "method": self.method,
            "params": {
                "included": self.included,
                "excluded": self.excluded,
                "packageRoots": self.packageRoots,
                }
            }

class SetPriorityFilesRequest(object):
    def __init__(self, request_id, **kwargs):
        self.method = "analysis.setPriorityFiles"
        self.request_id = request_id
        self.files = kwargs['files']

    def to_dict(self):
        return {
            "id": self.request_id,
            "method": self.method,
            "params": {
                "files": self.files,
                }
            }

class SetSubscriptionsRequest(object):
    def __init__(self, request_id, **kwargs):
        self.method = "analysis.setSubscriptions"
        self.request_id = request_id
        self.subscriptions = kwargs['subscriptions']

    def to_dict(self):
        return {
            "id": self.request_id,
            "method": self.method,
            "params": {
                "subscriptions": self.subscriptions,
                }
            }

class UpdateContentRequest(object):
    def __init__(self, request_id, **kwargs):
        self.method = "analysis.updateContent"
        self.request_id = request_id
        self.files = kwargs['files']

    def to_dict(self):
        return {
            "id": self.request_id,
            "method": self.method,
            "params": {
                "files": self.files,
                }
            }

class UpdateOptionsRequest(object):
    def __init__(self, request_id, **kwargs):
        self.method = "analysis.updateOptions"
        self.request_id = request_id
        self.options = kwargs['options']

    def to_dict(self):
        return {
            "id": self.request_id,
            "method": self.method,
            "params": {
                "options": self.options,
                }
            }

class GetSuggestionsRequest(object):
    def __init__(self, request_id, **kwargs):
        self.method = "completion.getSuggestions"
        self.request_id = request_id
        self.file = kwargs['file']
        self.offset = kwargs['offset']

    def to_dict(self):
        return {
            "id": self.request_id,
            "method": self.method,
            "params": {
                "file": self.file,
                "offset": self.offset,
                }
            }

class FindElementReferencesRequest(object):
    def __init__(self, request_id, **kwargs):
        self.method = "search.findElementReferences"
        self.request_id = request_id
        self.file = kwargs['file']
        self.offset = kwargs['offset']
        self.includePotential = kwargs['includePotential']

    def to_dict(self):
        return {
            "id": self.request_id,
            "method": self.method,
            "params": {
                "file": self.file,
                "offset": self.offset,
                "includePotential": self.includePotential,
                }
            }

class FindMemberDeclarationsRequest(object):
    def __init__(self, request_id, **kwargs):
        self.method = "search.findMemberDeclarations"
        self.request_id = request_id
        self.name = kwargs['name']

    def to_dict(self):
        return {
            "id": self.request_id,
            "method": self.method,
            "params": {
                "name": self.name,
                }
            }

class FindMemberReferencesRequest(object):
    def __init__(self, request_id, **kwargs):
        self.method = "search.findMemberReferences"
        self.request_id = request_id
        self.name = kwargs['name']

    def to_dict(self):
        return {
            "id": self.request_id,
            "method": self.method,
            "params": {
                "name": self.name,
                }
            }

class FindTopLevelDeclarationsRequest(object):
    def __init__(self, request_id, **kwargs):
        self.method = "search.findTopLevelDeclarations"
        self.request_id = request_id
        self.pattern = kwargs['pattern']

    def to_dict(self):
        return {
            "id": self.request_id,
            "method": self.method,
            "params": {
                "pattern": self.pattern,
                }
            }

class GetTypeHierarchyRequest(object):
    def __init__(self, request_id, **kwargs):
        self.method = "search.getTypeHierarchy"
        self.request_id = request_id
        self.file = kwargs['file']
        self.offset = kwargs['offset']

    def to_dict(self):
        return {
            "id": self.request_id,
            "method": self.method,
            "params": {
                "file": self.file,
                "offset": self.offset,
                }
            }

class GetAssistsRequest(object):
    def __init__(self, request_id, **kwargs):
        self.method = "edit.getAssists"
        self.request_id = request_id
        self.file = kwargs['file']
        self.offset = kwargs['offset']
        self.length = kwargs['length']

    def to_dict(self):
        return {
            "id": self.request_id,
            "method": self.method,
            "params": {
                "file": self.file,
                "offset": self.offset,
                "length": self.length,
                }
            }

class GetAvailableRefactoringsRequest(object):
    def __init__(self, request_id, **kwargs):
        self.method = "edit.getAvailableRefactorings"
        self.request_id = request_id
        self.file = kwargs['file']
        self.offset = kwargs['offset']
        self.length = kwargs['length']

    def to_dict(self):
        return {
            "id": self.request_id,
            "method": self.method,
            "params": {
                "file": self.file,
                "offset": self.offset,
                "length": self.length,
                }
            }

class GetFixesRequest(object):
    def __init__(self, request_id, **kwargs):
        self.method = "edit.getFixes"
        self.request_id = request_id
        self.file = kwargs['file']
        self.offset = kwargs['offset']

    def to_dict(self):
        return {
            "id": self.request_id,
            "method": self.method,
            "params": {
                "file": self.file,
                "offset": self.offset,
                }
            }

class GetRefactoringRequest(object):
    def __init__(self, request_id, **kwargs):
        self.method = "edit.getRefactoring"
        self.request_id = request_id
        self.kind = kwargs['kind']
        self.file = kwargs['file']
        self.offset = kwargs['offset']
        self.length = kwargs['length']
        self.validateOnly = kwargs['validateOnly']
        self.options = kwargs['options']

    def to_dict(self):
        return {
            "id": self.request_id,
            "method": self.method,
            "params": {
                "kind": self.kind,
                "file": self.file,
                "offset": self.offset,
                "length": self.length,
                "validateOnly": self.validateOnly,
                "options": self.options,
                }
            }

class SortMembersRequest(object):
    def __init__(self, request_id, **kwargs):
        self.method = "edit.sortMembers"
        self.request_id = request_id
        self.file = kwargs['file']

    def to_dict(self):
        return {
            "id": self.request_id,
            "method": self.method,
            "params": {
                "file": self.file,
                }
            }

class CreateContextRequest(object):
    def __init__(self, request_id, **kwargs):
        self.method = "execution.createContext"
        self.request_id = request_id
        self.contextRoot = kwargs['contextRoot']

    def to_dict(self):
        return {
            "id": self.request_id,
            "method": self.method,
            "params": {
                "contextRoot": self.contextRoot,
                }
            }

class DeleteContextRequest(object):
    def __init__(self, request_id, **kwargs):
        self.method = "execution.deleteContext"
        self.request_id = request_id
        self.id = kwargs['id']

    def to_dict(self):
        return {
            "id": self.request_id,
            "method": self.method,
            "params": {
                "id": self.id,
                }
            }

class MapUriRequest(object):
    def __init__(self, request_id, **kwargs):
        self.method = "execution.mapUri"
        self.request_id = request_id
        self.id = kwargs['id']
        self.file = kwargs['file']
        self.uri = kwargs['uri']

    def to_dict(self):
        return {
            "id": self.request_id,
            "method": self.method,
            "params": {
                "id": self.id,
                "file": self.file,
                "uri": self.uri,
                }
            }

class SetSubscriptionsRequest(object):
    def __init__(self, request_id, **kwargs):
        self.method = "execution.setSubscriptions"
        self.request_id = request_id
        self.subscriptions = kwargs['subscriptions']

    def to_dict(self):
        return {
            "id": self.request_id,
            "method": self.method,
            "params": {
                "subscriptions": self.subscriptions,
                }
            }

