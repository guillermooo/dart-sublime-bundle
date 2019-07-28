# Copyright (c) 2014, the Dart project authors.  Please see the AUTHORS file
# for details. All rights reserved. Use of this source code is governed by a
# BSD-style license that can be found in the LICENSE file.
#
# This file has been automatically generated.  Please do not edit it manually.
# To regenerate the file, use the script
# "pkg/analysis_server/tool/spec/generate_files".


from .api_types import *

class Response(object):
   """
   Base class for all responses.
   """

class ServerGetVersionResponse(Response):

  def __init__(self, data):
    self.item_id = data["id"]
    self.data = data

  @property
  def error(self):
    return self.data.get('error')

  @property
  def itemId(self):
    return self.data['id']

  @property
  def version(self):
    return self.data['result'].get('version')

class ServerShutdownResponse(Response):

  def __init__(self, data):
    self.item_id = data["id"]
    self.data = data

  @property
  def error(self):
    return self.data.get('error')

  @property
  def itemId(self):
    return self.data['id']

class ServerSetSubscriptionsResponse(Response):

  def __init__(self, data):
    self.item_id = data["id"]
    self.data = data

  @property
  def error(self):
    return self.data.get('error')

  @property
  def itemId(self):
    return self.data['id']

class AnalysisGetErrorsResponse(Response):

  def __init__(self, data):
    self.item_id = data["id"]
    self.data = data

  @property
  def error(self):
    return self.data.get('error')

  @property
  def errors(self):
    yield from [AnalysisError.fromJson(x) for x in self.data['result'].get('errors')]

  @property
  def itemId(self):
    return self.data['id']

class AnalysisGetHoverResponse(Response):

  def __init__(self, data):
    self.item_id = data["id"]
    self.data = data

  @property
  def error(self):
    return self.data.get('error')

  @property
  def hovers(self):
    yield from [HoverInformation.fromJson(x) for x in self.data['result'].get('hovers')]

  @property
  def itemId(self):
    return self.data['id']

class AnalysisGetNavigationResponse(Response):

  def __init__(self, data):
    self.item_id = data["id"]
    self.data = data

  @property
  def error(self):
    return self.data.get('error')

  @property
  def files(self):
    yield from [x for x in self.data['result'].get('files')]

  @property
  def itemId(self):
    return self.data['id']

  @property
  def regions(self):
    yield from [NavigationRegion.fromJson(x) for x in self.data['result'].get('regions')]

  @property
  def targets(self):
    yield from [NavigationTarget.fromJson(x) for x in self.data['result'].get('targets')]

class AnalysisReanalyzeResponse(Response):

  def __init__(self, data):
    self.item_id = data["id"]
    self.data = data

  @property
  def error(self):
    return self.data.get('error')

  @property
  def itemId(self):
    return self.data['id']

class AnalysisSetAnalysisRootsResponse(Response):

  def __init__(self, data):
    self.item_id = data["id"]
    self.data = data

  @property
  def error(self):
    return self.data.get('error')

  @property
  def itemId(self):
    return self.data['id']

class AnalysisSetPriorityFilesResponse(Response):

  def __init__(self, data):
    self.item_id = data["id"]
    self.data = data

  @property
  def error(self):
    return self.data.get('error')

  @property
  def itemId(self):
    return self.data['id']

class AnalysisSetSubscriptionsResponse(Response):

  def __init__(self, data):
    self.item_id = data["id"]
    self.data = data

  @property
  def error(self):
    return self.data.get('error')

  @property
  def itemId(self):
    return self.data['id']

class AnalysisUpdateContentResponse(Response):

  def __init__(self, data):
    self.item_id = data["id"]
    self.data = data

  @property
  def error(self):
    return self.data.get('error')

  @property
  def itemId(self):
    return self.data['id']

class AnalysisUpdateOptionsResponse(Response):

  def __init__(self, data):
    self.item_id = data["id"]
    self.data = data

  @property
  def error(self):
    return self.data.get('error')

  @property
  def itemId(self):
    return self.data['id']

class CompletionGetSuggestionsResponse(Response):

  def __init__(self, data):
    self.item_id = data["id"]
    self.data = data

  @property
  def error(self):
    return self.data.get('error')

  @property
  def id(self):
    return self.data['result'].get('id')

class SearchFindElementReferencesResponse(Response):

  def __init__(self, data):
    self.item_id = data["id"]
    self.data = data
  @property
  def element(self):
    return self.data['result'].get('element')


  @property
  def error(self):
    return self.data.get('error')

  @property
  def id(self):
    return self.data['result'].get('id')

class SearchFindMemberDeclarationsResponse(Response):

  def __init__(self, data):
    self.item_id = data["id"]
    self.data = data

  @property
  def error(self):
    return self.data.get('error')

  @property
  def id(self):
    return self.data['result'].get('id')

class SearchFindMemberReferencesResponse(Response):

  def __init__(self, data):
    self.item_id = data["id"]
    self.data = data

  @property
  def error(self):
    return self.data.get('error')

  @property
  def id(self):
    return self.data['result'].get('id')

class SearchFindTopLevelDeclarationsResponse(Response):

  def __init__(self, data):
    self.item_id = data["id"]
    self.data = data

  @property
  def error(self):
    return self.data.get('error')

  @property
  def id(self):
    return self.data['result'].get('id')

class SearchGetTypeHierarchyResponse(Response):

  def __init__(self, data):
    self.item_id = data["id"]
    self.data = data

  @property
  def error(self):
    return self.data.get('error')

  @property
  def hierarchyItems(self):
    yield from [TypeHierarchyItem.fromJson(x) for x in self.data['result'].get('hierarchyItems')]

  @property
  def itemId(self):
    return self.data['id']

class EditFormatResponse(Response):

  def __init__(self, data):
    self.item_id = data["id"]
    self.data = data
  @property
  def edits(self):
    yield from [SourceEdit.fromJson(x) for x in self.data['result'].get('edits')]


  @property
  def error(self):
    return self.data.get('error')

  @property
  def itemId(self):
    return self.data['id']

  @property
  def selectionLength(self):
    return self.data['result'].get('selectionLength')

  @property
  def selectionOffset(self):
    return self.data['result'].get('selectionOffset')

class EditGetAssistsResponse(Response):

  def __init__(self, data):
    self.item_id = data["id"]
    self.data = data
  @property
  def assists(self):
    yield from [SourceChange.fromJson(x) for x in self.data['result'].get('assists')]


  @property
  def error(self):
    return self.data.get('error')

  @property
  def itemId(self):
    return self.data['id']

class EditGetAvailableRefactoringsResponse(Response):

  def __init__(self, data):
    self.item_id = data["id"]
    self.data = data

  @property
  def error(self):
    return self.data.get('error')

  @property
  def itemId(self):
    return self.data['id']

  @property
  def kinds(self):
    yield from [x for x in self.data['result'].get('kinds')]

class EditGetFixesResponse(Response):

  def __init__(self, data):
    self.item_id = data["id"]
    self.data = data

  @property
  def error(self):
    return self.data.get('error')

  @property
  def fixes(self):
    yield from [AnalysisErrorFixes.fromJson(x) for x in self.data['result'].get('fixes')]

  @property
  def itemId(self):
    return self.data['id']

class EditGetRefactoringResponse(Response):

  def __init__(self, data):
    self.item_id = data["id"]
    self.data = data
  @property
  def change(self):
    return self.data['result'].get('change')


  @property
  def error(self):
    return self.data.get('error')

  @property
  def feedback(self):
    return self.data['result'].get('feedback')

  @property
  def finalProblems(self):
    yield from [RefactoringProblem.fromJson(x) for x in self.data['result'].get('finalProblems')]

  @property
  def itemId(self):
    return self.data['id']

  @property
  def initialProblems(self):
    yield from [RefactoringProblem.fromJson(x) for x in self.data['result'].get('initialProblems')]

  @property
  def optionsProblems(self):
    yield from [RefactoringProblem.fromJson(x) for x in self.data['result'].get('optionsProblems')]

  @property
  def potentialEdits(self):
    yield from [x for x in self.data['result'].get('potentialEdits')]

class EditSortMembersResponse(Response):

  def __init__(self, data):
    self.item_id = data["id"]
    self.data = data
  @property
  def edit(self):
    return self.data['result'].get('edit')


  @property
  def error(self):
    return self.data.get('error')

  @property
  def itemId(self):
    return self.data['id']

class ExecutionCreateContextResponse(Response):

  def __init__(self, data):
    self.item_id = data["id"]
    self.data = data

  @property
  def error(self):
    return self.data.get('error')

  @property
  def id(self):
    return self.data['result'].get('id')

class ExecutionDeleteContextResponse(Response):

  def __init__(self, data):
    self.item_id = data["id"]
    self.data = data

  @property
  def error(self):
    return self.data.get('error')

  @property
  def itemId(self):
    return self.data['id']

class ExecutionMapUriResponse(Response):

  def __init__(self, data):
    self.item_id = data["id"]
    self.data = data

  @property
  def error(self):
    return self.data.get('error')

  @property
  def file(self):
    return self.data['result'].get('file')

  @property
  def itemId(self):
    return self.data['id']

  @property
  def uri(self):
    return self.data['result'].get('uri')

class ExecutionSetSubscriptionsResponse(Response):

  def __init__(self, data):
    self.item_id = data["id"]
    self.data = data

  @property
  def error(self):
    return self.data.get('error')

  @property
  def itemId(self):
    return self.data['id']

