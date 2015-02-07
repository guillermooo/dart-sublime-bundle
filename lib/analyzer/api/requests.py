# Copyright (c) 2014, the Dart project authors.  Please see the AUTHORS file
# for details. All rights reserved. Use of this source code is governed by a
# BSD-style license that can be found in the LICENSE file.
#
# This file has been automatically generated.  Please do not edit it manually.
# To regenerate the file, use the script
# "pkg/analysis_server/tool/spec/generate_files".


class Request(object):
   """
   Base class for all requests.
   """

class ServerGetVersionRequest(Request):
  """
  Return the version number of the analysis server.
  """

  def __init__(self, op_id):
    self.op_id = op_id
    self.method = "server.getVersion"

  def toJson(self):
    return {
      "id": self.op_id,
      "params": {
        "method": self.method,
      }
    }

class ServerShutdownRequest(Request):
  """
  Cleanly shutdown the analysis server. Requests that are received after this
  request will not be processed. Requests that were received before this
  request, but for which a response has not yet been sent, will not be
  responded to. No further responses or notifications will be sent after the
  response to this request has been sent.
  """

  def __init__(self, op_id):
    self.op_id = op_id
    self.method = "server.shutdown"

  def toJson(self):
    return {
      "id": self.op_id,
      "params": {
        "method": self.method,
      }
    }

class ServerSetSubscriptionsRequest(Request):
  """
  Subscribe for services. All previous subscriptions are replaced by the given
  set of services.

  It is an error if any of the elements in the list are not valid services. If
  there is an error, then the current subscriptions will remain unchanged.
  """

  def __init__(self, op_id, subscriptions):
    self.op_id = op_id
    self.subscriptions = subscriptions
    self.method = "server.setSubscriptions"

  def toJson(self):
    return {
      "id": self.op_id,
      "params": {
        "method": self.method,
        "subscriptions": self.subscriptions,
      }
    }

class AnalysisGetErrorsRequest(Request):
  """
  Return the errors associated with the given file. If the errors for the given
  file have not yet been computed, or the most recently computed errors for the
  given file are out of date, then the response for this request will be
  delayed until they have been computed. If some or all of the errors for the
  file cannot be computed, then the subset of the errors that can be computed
  will be returned and the response will contain an error to indicate why the
  errors could not be computed. If the content of the file changes after this
  request was received but before a response could be sent, then an error of
  type CONTENT_MODIFIED will be generated.

  This request is intended to be used by clients that cannot asynchronously
  apply updated error information. Clients that can apply error information as
  it becomes available should use the information provided by the
  'analysis.errors' notification.

  If a request is made for a file which does not exist, or which is not
  currently subject to analysis (e.g. because it is not associated with any
  analysis root specified to analysis.setAnalysisRoots), an error of type
  GET_ERRORS_INVALID_FILE will be generated.
  """

  def __init__(self, op_id, file):
    self.op_id = op_id
    self.file = file
    self.method = "analysis.getErrors"

  def toJson(self):
    return {
      "id": self.op_id,
      "params": {
        "method": self.method,
        "file": self.file,
      }
    }

class AnalysisGetHoverRequest(Request):
  """
  Return the hover information associate with the given location. If some or
  all of the hover information is not available at the time this request is
  processed the information will be omitted from the response.
  """

  def __init__(self, op_id, file, offset):
    self.op_id = op_id
    self.file = file
    self.offset = offset
    self.method = "analysis.getHover"

  def toJson(self):
    return {
      "id": self.op_id,
      "params": {
        "method": self.method,
        "file": self.file,
        "offset": self.offset,
      }
    }

class AnalysisGetNavigationRequest(Request):
  """
  Return the navigation information associated with the given region of the
  given file. If the navigation information for the given file has not yet been
  computed, or the most recently computed navigation information for the given
  file is out of date, then the response for this request will be delayed until
  it has been computed. If the content of the file changes after this request
  was received but before a response could be sent, then an error of type
  CONTENT_MODIFIED will be generated.

  If a navigation region overlaps (but extends either before or after) the
  given region of the file it will be included in the result. This means that
  it is theoretically possible to get the same navigation region in response to
  multiple requests. Clients can avoid this by always choosing a region that
  starts at the beginning of a line and ends at the end of a (possibly
  different) line in the file.
  """

  def __init__(self, op_id, file, offset, length):
    self.op_id = op_id
    self.file = file
    self.offset = offset
    self.length = length
    self.method = "analysis.getNavigation"

  def toJson(self):
    return {
      "id": self.op_id,
      "params": {
        "method": self.method,
        "file": self.file,
        "offset": self.offset,
        "length": self.length,
      }
    }

class AnalysisReanalyzeRequest(Request):
  """
  Force the re-analysis of everything contained in the existing analysis roots.
  This will cause all previously computed analysis results to be discarded and
  recomputed, and will cause all subscribed notifications to be re-sent.
  """

  def __init__(self, op_id):
    self.op_id = op_id
    self.method = "analysis.reanalyze"

  def toJson(self):
    return {
      "id": self.op_id,
      "params": {
        "method": self.method,
      }
    }

class AnalysisSetAnalysisRootsRequest(Request):
  """
  Sets the root paths used to determine which files to analyze. The set of
  files to be analyzed are all of the files in one of the root paths that are
  not also in one of the excluded paths.

  Note that this request determines the set of requested analysis roots. The
  actual set of analysis roots at any given time is the intersection of this
  set with the set of files and directories actually present on the filesystem.
  When the filesystem changes, the actual set of analysis roots is
  automatically updated, but the set of requested analysis roots is unchanged.
  This means that if the client sets an analysis root before the root becomes
  visible to server in the filesystem, there is no error; once the server sees
  the root in the filesystem it will start analyzing it. Similarly, server will
  stop analyzing files that are removed from the file system but they will
  remain in the set of requested roots.

  If an included path represents a file, then server will look in the directory
  containing the file for a pubspec.yaml file. If none is found, then the
  parents of the directory will be searched until such a file is found or the
  root of the file system is reached. If such a file is found, it will be used
  to resolve package: URI’s within the file.
  """

  def __init__(self, op_id, included, excluded, packageRoots={}):
    self.op_id = op_id
    self.included = included
    self.excluded = excluded
    self.packageRoots = packageRoots
    self.method = "analysis.setAnalysisRoots"

  def toJson(self):
    return {
      "id": self.op_id,
      "params": {
        "method": self.method,
        "included": self.included,
        "excluded": self.excluded,
        "packageRoots": self.packageRoots,
      }
    }

class AnalysisSetPriorityFilesRequest(Request):
  """
  Set the priority files to the files in the given list. A priority file is a
  file that is given priority when scheduling which analysis work to do first.
  The list typically contains those files that are visible to the user and
  those for which analysis results will have the biggest impact on the user
  experience. The order of the files within the list is significant: the first
  file will be given higher priority than the second, the second higher
  priority than the third, and so on.

  Note that this request determines the set of requested priority files. The
  actual set of priority files is the intersection of the requested set of
  priority files with the set of files currently subject to analysis. (See
  analysis.setSubscriptions for a description of files that are subject to
  analysis.)

  If a requested priority file is a directory it is ignored, but remains in the
  set of requested priority files so that if it later becomes a file it can be
  included in the set of actual priority files.
  """

  def __init__(self, op_id, files):
    self.op_id = op_id
    self.files = files
    self.method = "analysis.setPriorityFiles"

  def toJson(self):
    return {
      "id": self.op_id,
      "params": {
        "method": self.method,
        "files": self.files,
      }
    }

class AnalysisSetSubscriptionsRequest(Request):
  """
  Subscribe for services. All previous subscriptions are replaced by the
  current set of subscriptions. If a given service is not included as a key in
  the map then no files will be subscribed to the service, exactly as if the
  service had been included in the map with an explicit empty list of files.

  Note that this request determines the set of requested subscriptions. The
  actual set of subscriptions at any given time is the intersection of this set
  with the set of files currently subject to analysis. The files currently
  subject to analysis are the set of files contained within an actual analysis
  root but not excluded, plus all of the files transitively reachable from
  those files via import, export and part directives. (See
  analysis.setAnalysisRoots for an explanation of how the actual analysis roots
  are determined.) When the actual analysis roots change, the actual set of
  subscriptions is automatically updated, but the set of requested
  subscriptions is unchanged.

  If a requested subscription is a directory it is ignored, but remains in the
  set of requested subscriptions so that if it later becomes a file it can be
  included in the set of actual subscriptions.

  It is an error if any of the keys in the map are not valid services. If there
  is an error, then the existing subscriptions will remain unchanged.
  """

  def __init__(self, op_id, subscriptions):
    self.op_id = op_id
    self.subscriptions = subscriptions
    self.method = "analysis.setSubscriptions"

  def toJson(self):
    return {
      "id": self.op_id,
      "params": {
        "method": self.method,
        "subscriptions": self.subscriptions,
      }
    }

class AnalysisUpdateContentRequest(Request):
  """
  Update the content of one or more files. Files that were previously updated
  but not included in this update remain unchanged. This effectively represents
  an overlay of the filesystem. The files whose content is overridden are
  therefore seen by server as being files with the given content, even if the
  files do not exist on the filesystem or if the file path represents the path
  to a directory on the filesystem.
  """

  def __init__(self, op_id, files):
    self.op_id = op_id
    self.files = files
    self.method = "analysis.updateContent"

  def toJson(self):
    return {
      "id": self.op_id,
      "params": {
        "method": self.method,
        "files": {(k, v.toJson()) for (k, v) in self.files},
      }
    }

class AnalysisUpdateOptionsRequest(Request):
  """
  Update the options controlling analysis based on the given set of options.
  Any options that are not included in the analysis options will not be
  changed. If there are options in the analysis options that are not valid,
  they will be silently ignored.
  """

  def __init__(self, op_id, options):
    self.op_id = op_id
    self.options = options
    self.method = "analysis.updateOptions"

  def toJson(self):
    return {
      "id": self.op_id,
      "params": {
        "method": self.method,
        "options": self.options.toJson(),
      }
    }

class CompletionGetSuggestionsRequest(Request):
  """
  Request that completion suggestions for the given offset in the given file be
  returned.
  """

  def __init__(self, op_id, file, offset):
    self.op_id = op_id
    self.file = file
    self.offset = offset
    self.method = "completion.getSuggestions"

  def toJson(self):
    return {
      "id": self.op_id,
      "params": {
        "method": self.method,
        "file": self.file,
        "offset": self.offset,
      }
    }

class SearchFindElementReferencesRequest(Request):
  """
  Perform a search for references to the element defined or referenced at the
  given offset in the given file.

  An identifier is returned immediately, and individual results will be
  returned via the search.results notification as they become available.
  """

  def __init__(self, op_id, file, offset, includePotential):
    self.op_id = op_id
    self.file = file
    self.offset = offset
    self.includePotential = includePotential
    self.method = "search.findElementReferences"

  def toJson(self):
    return {
      "id": self.op_id,
      "params": {
        "method": self.method,
        "file": self.file,
        "offset": self.offset,
        "includePotential": self.includePotential,
      }
    }

class SearchFindMemberDeclarationsRequest(Request):
  """
  Perform a search for declarations of members whose name is equal to the given
  name.

  An identifier is returned immediately, and individual results will be
  returned via the search.results notification as they become available.
  """

  def __init__(self, op_id, name):
    self.op_id = op_id
    self.name = name
    self.method = "search.findMemberDeclarations"

  def toJson(self):
    return {
      "id": self.op_id,
      "params": {
        "method": self.method,
        "name": self.name,
      }
    }

class SearchFindMemberReferencesRequest(Request):
  """
  Perform a search for references to members whose name is equal to the given
  name. This search does not check to see that there is a member defined with
  the given name, so it is able to find references to undefined members as
  well.

  An identifier is returned immediately, and individual results will be
  returned via the search.results notification as they become available.
  """

  def __init__(self, op_id, name):
    self.op_id = op_id
    self.name = name
    self.method = "search.findMemberReferences"

  def toJson(self):
    return {
      "id": self.op_id,
      "params": {
        "method": self.method,
        "name": self.name,
      }
    }

class SearchFindTopLevelDeclarationsRequest(Request):
  """
  Perform a search for declarations of top-level elements (classes, typedefs,
  getters, setters, functions and fields) whose name matches the given pattern.

  An identifier is returned immediately, and individual results will be
  returned via the search.results notification as they become available.
  """

  def __init__(self, op_id, pattern):
    self.op_id = op_id
    self.pattern = pattern
    self.method = "search.findTopLevelDeclarations"

  def toJson(self):
    return {
      "id": self.op_id,
      "params": {
        "method": self.method,
        "pattern": self.pattern,
      }
    }

class SearchGetTypeHierarchyRequest(Request):
  """
  Return the type hierarchy of the class declared or referenced at the given
  location.
  """

  def __init__(self, op_id, file, offset):
    self.op_id = op_id
    self.file = file
    self.offset = offset
    self.method = "search.getTypeHierarchy"

  def toJson(self):
    return {
      "id": self.op_id,
      "params": {
        "method": self.method,
        "file": self.file,
        "offset": self.offset,
      }
    }

class EditFormatRequest(Request):
  """
  Format the contents of a single file. The currently selected region of text
  is passed in so that the selection can be preserved across the formatting
  operation. The updated selection will be as close to matching the original as
  possible, but whitespace at the beginning or end of the selected region will
  be ignored.

  If a request is made for a file which does not exist, or which is not
  currently subject to analysis (e.g. because it is not associated with any
  analysis root specified to analysis.setAnalysisRoots), an error of type
  FORMAT_INVALID_FILE will be generated.
  """

  def __init__(self, op_id, file, selectionOffset, selectionLength):
    self.op_id = op_id
    self.file = file
    self.selectionOffset = selectionOffset
    self.selectionLength = selectionLength
    self.method = "edit.format"

  def toJson(self):
    return {
      "id": self.op_id,
      "params": {
        "method": self.method,
        "file": self.file,
        "selectionOffset": self.selectionOffset,
        "selectionLength": self.selectionLength,
      }
    }

class EditGetAssistsRequest(Request):
  """
  Return the set of assists that are available at the given location. An assist
  is distinguished from a refactoring primarily by the fact that it affects a
  single file and does not require user input in order to be performed.
  """

  def __init__(self, op_id, file, offset, length):
    self.op_id = op_id
    self.file = file
    self.offset = offset
    self.length = length
    self.method = "edit.getAssists"

  def toJson(self):
    return {
      "id": self.op_id,
      "params": {
        "method": self.method,
        "file": self.file,
        "offset": self.offset,
        "length": self.length,
      }
    }

class EditGetAvailableRefactoringsRequest(Request):
  """
  Get a list of the kinds of refactorings that are valid for the given
  selection in the given file.
  """

  def __init__(self, op_id, file, offset, length):
    self.op_id = op_id
    self.file = file
    self.offset = offset
    self.length = length
    self.method = "edit.getAvailableRefactorings"

  def toJson(self):
    return {
      "id": self.op_id,
      "params": {
        "method": self.method,
        "file": self.file,
        "offset": self.offset,
        "length": self.length,
      }
    }

class EditGetFixesRequest(Request):
  """
  Return the set of fixes that are available for the errors at a given offset
  in a given file.
  """

  def __init__(self, op_id, file, offset):
    self.op_id = op_id
    self.file = file
    self.offset = offset
    self.method = "edit.getFixes"

  def toJson(self):
    return {
      "id": self.op_id,
      "params": {
        "method": self.method,
        "file": self.file,
        "offset": self.offset,
      }
    }

class EditGetRefactoringRequest(Request):
  """
  Get the changes required to perform a refactoring.
  """

  def __init__(self, op_id, kind, file, offset, length, validateOnly, options=None):
    self.op_id = op_id
    self.kind = kind
    self.file = file
    self.offset = offset
    self.length = length
    self.validateOnly = validateOnly
    self.options = options
    self.method = "edit.getRefactoring"

  def toJson(self):
    return {
      "id": self.op_id,
      "params": {
        "method": self.method,
        "kind": self.kind,
        "file": self.file,
        "offset": self.offset,
        "length": self.length,
        "validateOnly": self.validateOnly,
        "options": self.options.toJson(),
      }
    }

class EditSortMembersRequest(Request):
  """
  Sort all of the directives, unit and class members of the given Dart file.

  If a request is made for a file that does not exist, does not belong to an
  analysis root or is not a Dart file, SORT_MEMBERS_INVALID_FILE will be
  generated.

  If the Dart file has scan or parse errors, SORT_MEMBERS_PARSE_ERRORS will be
  generated.
  """

  def __init__(self, op_id, file):
    self.op_id = op_id
    self.file = file
    self.method = "edit.sortMembers"

  def toJson(self):
    return {
      "id": self.op_id,
      "params": {
        "method": self.method,
        "file": self.file,
      }
    }

class ExecutionCreateContextRequest(Request):
  """
  Create an execution context for the executable file with the given path. The
  context that is created will persist until execution.deleteContext is used to
  delete it. Clients, therefore, are responsible for managing the lifetime of
  execution contexts.
  """

  def __init__(self, op_id, contextRoot):
    self.op_id = op_id
    self.contextRoot = contextRoot
    self.method = "execution.createContext"

  def toJson(self):
    return {
      "id": self.op_id,
      "params": {
        "method": self.method,
        "contextRoot": self.contextRoot,
      }
    }

class ExecutionDeleteContextRequest(Request):
  """
  Delete the execution context with the given identifier. The context id is no
  longer valid after this command. The server is allowed to re-use ids when
  they are no longer valid.
  """

  def __init__(self, op_id, item_id):
    self.op_id = op_id
    self.item_id = item_id
    self.method = "execution.deleteContext"

  def toJson(self):
    return {
      "id": self.op_id,
      "params": {
        "method": self.method,
        "id": self.item_id,
      }
    }

class ExecutionMapUriRequest(Request):
  """
  Map a URI from the execution context to the file that it corresponds to, or
  map a file to the URI that it corresponds to in the execution context.

  Exactly one of the file and uri fields must be provided.
  """

  def __init__(self, op_id, item_id, file='', uri=''):
    self.op_id = op_id
    self.item_id = item_id
    self.file = file
    self.uri = uri
    self.method = "execution.mapUri"

  def toJson(self):
    return {
      "id": self.op_id,
      "params": {
        "method": self.method,
        "id": self.item_id,
        "file": self.file,
        "uri": self.uri,
      }
    }

class ExecutionSetSubscriptionsRequest(Request):
  """
  Subscribe for services. All previous subscriptions are replaced by the given
  set of services.

  It is an error if any of the elements in the list are not valid services. If
  there is an error, then the current subscriptions will remain unchanged.
  """

  def __init__(self, op_id, subscriptions):
    self.op_id = op_id
    self.subscriptions = subscriptions
    self.method = "execution.setSubscriptions"

  def toJson(self):
    return {
      "id": self.op_id,
      "params": {
        "method": self.method,
        "subscriptions": self.subscriptions,
      }
    }

