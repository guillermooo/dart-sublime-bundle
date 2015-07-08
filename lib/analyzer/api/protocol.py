# Copyright (c) 2014, the Dart project authors.  Please see the AUTHORS file
# for details. All rights reserved. Use of this source code is governed by a
# BSD-style license that can be found in the LICENSE file.
#
# This file has been automatically generated.  Please do not edit it manually.
# To regenerate the file, use the script
# "pkg/analysis_server/tool/spec/generate_files".

from .base import *
import json

# server.getVersion params
class ServerGetVersionParams(object):
  def to_request(self, id):
    assert id is not None, "must provide an id for the request"
    return Request(id, "server.getVersion", None)



# server.getVersion result
#
# {
#   "version": String
# }
class ServerGetVersionResult(object):
  def __init__(self, version):
    # The version number of the analysis server.
    self.version = version

  @classmethod
  def from_json(cls, data):
    if not data:
      raise ValueError("server.getVersion result" + " has no data")

    version = data["version"]

    return cls(version)

  def to_json(self):
    result = {}
    result["version"] = self.version
    return result

  def to_response(self, id):
    assert id is not None, "must provide an id for the response"
    return Response(id, result=self)

  def __str__(self):
    return json.dumps(self.to_json())


# server.shutdown params
class ServerShutdownParams(object):
  def to_request(self, id):
    assert id is not None, "must provide an id for the request"
    return Request(id, "server.shutdown", None)


# server.shutdown result
class ServerShutdownResult(object):
  def to_response(self, id):
    assert id is not None, "must provide an id for the response"
    return Response(id, result=None)



# server.setSubscriptions params
#
# {
#   "subscriptions": List<ServerService>
# }
class ServerSetSubscriptionsParams(object):
  def __init__(self, subscriptions):
    # A list of the services being subscribed to.
    self.subscriptions = subscriptions

  @classmethod
  def from_json(cls, data):
    if not data:
      raise ValueError("server.setSubscriptions params" + " has no data")

    subscriptions = data["subscriptions"]

    return cls(subscriptions)

  def to_json(self):
    result = {}
    result["subscriptions"] = self.subscriptions
    return result

  def to_request(self, id):
    assert id is not None, "must provide an id for the request"
    return Request(id, "server.setSubscriptions", self)

  def __str__(self):
    return json.dumps(self.to_json())


# server.setSubscriptions result
class ServerSetSubscriptionsResult(object):
  def to_response(self, id):
    assert id is not None, "must provide an id for the response"
    return Response(id, result=None)



# server.connected params
#
# {
#   "version": String
# }
class ServerConnectedParams(object):
  def __init__(self, version):
    # The version number of the analysis server.
    self.version = version

  @classmethod
  def from_json(cls, data):
    if not data:
      raise ValueError("server.connected params" + " has no data")

    version = data["version"]

    return cls(version)

  def to_json(self):
    result = {}
    result["version"] = self.version
    return result

  def to_notification(self):
    return Notification("server.connected", self);

  def __str__(self):
    return json.dumps(self.to_json())



# server.error params
#
# {
#   "isFatal": bool
#   "message": String
#   "stackTrace": String
# }
class ServerErrorParams(object):
  def __init__(self, isFatal, message, stackTrace):
    # True if the error is a fatal error, meaning that the server will shutdown
    # automatically after sending this notification.
    self.isFatal = isFatal
    # The error message indicating what kind of error was encountered.
    self.message = message
    # The stack trace associated with the generation of the error, used for
    # debugging the server.
    self.stackTrace = stackTrace

  @classmethod
  def from_json(cls, data):
    if not data:
      raise ValueError("server.error params" + " has no data")

    isFatal = data["isFatal"]
    message = data["message"]
    stackTrace = data["stackTrace"]

    return cls(isFatal, message, stackTrace)

  def to_json(self):
    result = {}
    result["isFatal"] = self.isFatal
    result["message"] = self.message
    result["stackTrace"] = self.stackTrace
    return result

  def to_notification(self):
    return Notification("server.error", self);

  def __str__(self):
    return json.dumps(self.to_json())



# server.status params
#
# {
#   "analysis": optional AnalysisStatus
#   "pub": optional PubStatus
# }
class ServerStatusParams(object):
  def __init__(self, analysis=None, pub=None):
    # The current status of analysis, including whether analysis is being
    # performed and if so what is being analyzed.
    self.analysis = analysis
    # The current status of pub execution, indicating whether we are currently
    # running pub.
    self.pub = pub

  @classmethod
  def from_json(cls, data):
    if not data:
      raise ValueError("server.status params" + " has no data")

    analysis = data.get("analysis", None)
    if analysis:
      analysis = AnalysisStatus.from_json(analysis)
    pub = data.get("pub", None)
    if pub:
      pub = PubStatus.from_json(pub)

    return cls(analysis=analysis, pub=pub)

  def to_json(self):
    result = {}
    if self.analysis:
      result["analysis"] = self.analysis.to_json()
    if self.pub:
      result["pub"] = self.pub.to_json()
    return result

  def to_notification(self):
    return Notification("server.status", self);

  def __str__(self):
    return json.dumps(self.to_json())



# analysis.getErrors params
#
# {
#   "file": FilePath
# }
class AnalysisGetErrorsParams(object):
  def __init__(self, file):
    # The file for which errors are being requested.
    self.file = file

  @classmethod
  def from_json(cls, data):
    if not data:
      raise ValueError("analysis.getErrors params" + " has no data")

    file = data["file"]

    return cls(file)

  def to_json(self):
    result = {}
    result["file"] = self.file
    return result

  def to_request(self, id):
    assert id is not None, "must provide an id for the request"
    return Request(id, "analysis.getErrors", self)

  def __str__(self):
    return json.dumps(self.to_json())



# analysis.getErrors result
#
# {
#   "errors": List<AnalysisError>
# }
class AnalysisGetErrorsResult(object):
  def __init__(self, errors):
    # The errors associated with the file.
    self.errors = errors

  @classmethod
  def from_json(cls, data):
    if not data:
      raise ValueError("analysis.getErrors result" + " has no data")

    errors = [AnalysisError.from_json(x) for x in data["errors"]]

    return cls(errors)

  def to_json(self):
    result = {}
    result["errors"] = [x.to_json() for x in self.errors]
    return result

  def to_response(self, id):
    assert id is not None, "must provide an id for the response"
    return Response(id, result=self)

  def __str__(self):
    return json.dumps(self.to_json())



# analysis.getHover params
#
# {
#   "file": FilePath
#   "offset": int
# }
class AnalysisGetHoverParams(object):
  def __init__(self, file, offset):
    # The file in which hover information is being requested.
    self.file = file
    # The offset for which hover information is being requested.
    self.offset = offset

  @classmethod
  def from_json(cls, data):
    if not data:
      raise ValueError("analysis.getHover params" + " has no data")

    file = data["file"]
    offset = data["offset"]

    return cls(file, offset)

  def to_json(self):
    result = {}
    result["file"] = self.file
    result["offset"] = self.offset
    return result

  def to_request(self, id):
    assert id is not None, "must provide an id for the request"
    return Request(id, "analysis.getHover", self)

  def __str__(self):
    return json.dumps(self.to_json())



# analysis.getHover result
#
# {
#   "hovers": List<HoverInformation>
# }
class AnalysisGetHoverResult(object):
  def __init__(self, hovers):
    # The hover information associated with the location. The list will be
    # empty if no information could be determined for the location. The list
    # can contain multiple items if the file is being analyzed in multiple
    # contexts in conflicting ways (such as a part that is included in multiple
    # libraries).
    self.hovers = hovers

  @classmethod
  def from_json(cls, data):
    if not data:
      raise ValueError("analysis.getHover result" + " has no data")

    hovers = [HoverInformation.from_json(x) for x in data["hovers"]]

    return cls(hovers)

  def to_json(self):
    result = {}
    result["hovers"] = [x.to_json() for x in self.hovers]
    return result

  def to_response(self, id):
    assert id is not None, "must provide an id for the response"
    return Response(id, result=self)

  def __str__(self):
    return json.dumps(self.to_json())


# analysis.getLibraryDependencies params
class AnalysisGetLibraryDependenciesParams(object):
  def to_request(self, id):
    assert id is not None, "must provide an id for the request"
    return Request(id, "analysis.getLibraryDependencies", None)



# analysis.getLibraryDependencies result
#
# {
#   "libraries": List<FilePath>
#   "packageMap": Map<String, Map<String, List<FilePath>>>
# }
class AnalysisGetLibraryDependenciesResult(object):
  def __init__(self, libraries, packageMap):
    # A list of the paths of library elements referenced by files in existing
    # analysis roots.
    self.libraries = libraries
    # A mapping from context source roots to package maps which map package
    # names to source directories for use in client-side package URI
    # resolution.
    self.packageMap = packageMap

  @classmethod
  def from_json(cls, data):
    if not data:
      raise ValueError("analysis.getLibraryDependencies result" + " has no data")

    libraries = data["libraries"]
    packageMap = data["packageMap"]

    return cls(libraries, packageMap)

  def to_json(self):
    result = {}
    result["libraries"] = self.libraries
    result["packageMap"] = {k: {k: v for (k, v) in v.items()} for (k, v) in self.packageMap.items()}
    return result

  def to_response(self, id):
    assert id is not None, "must provide an id for the response"
    return Response(id, result=self)

  def __str__(self):
    return json.dumps(self.to_json())



# analysis.getNavigation params
#
# {
#   "file": FilePath
#   "offset": int
#   "length": int
# }
class AnalysisGetNavigationParams(object):
  def __init__(self, file, offset, length):
    # The file in which navigation information is being requested.
    self.file = file
    # The offset of the region for which navigation information is being
    # requested.
    self.offset = offset
    # The length of the region for which navigation information is being
    # requested.
    self.length = length

  @classmethod
  def from_json(cls, data):
    if not data:
      raise ValueError("analysis.getNavigation params" + " has no data")

    file = data["file"]
    offset = data["offset"]
    length = data["length"]

    return cls(file, offset, length)

  def to_json(self):
    result = {}
    result["file"] = self.file
    result["offset"] = self.offset
    result["length"] = self.length
    return result

  def to_request(self, id):
    assert id is not None, "must provide an id for the request"
    return Request(id, "analysis.getNavigation", self)

  def __str__(self):
    return json.dumps(self.to_json())



# analysis.getNavigation result
#
# {
#   "files": List<FilePath>
#   "targets": List<NavigationTarget>
#   "regions": List<NavigationRegion>
# }
class AnalysisGetNavigationResult(object):
  def __init__(self, files, targets, regions):
    # A list of the paths of files that are referenced by the navigation
    # targets.
    self.files = files
    # A list of the navigation targets that are referenced by the navigation
    # regions.
    self.targets = targets
    # A list of the navigation regions within the requested region of the file.
    self.regions = regions

  @classmethod
  def from_json(cls, data):
    if not data:
      raise ValueError("analysis.getNavigation result" + " has no data")

    files = data["files"]
    targets = [NavigationTarget.from_json(x) for x in data["targets"]]
    regions = [NavigationRegion.from_json(x) for x in data["regions"]]

    return cls(files, targets, regions)

  def to_json(self):
    result = {}
    result["files"] = self.files
    result["targets"] = [x.to_json() for x in self.targets]
    result["regions"] = [x.to_json() for x in self.regions]
    return result

  def to_response(self, id):
    assert id is not None, "must provide an id for the response"
    return Response(id, result=self)

  def __str__(self):
    return json.dumps(self.to_json())



# analysis.reanalyze params
#
# {
#   "roots": optional List<FilePath>
# }
class AnalysisReanalyzeParams(object):
  def __init__(self, roots=[]):
    # A list of the analysis roots that are to be re-analyzed.
    self.roots = roots

  @classmethod
  def from_json(cls, data):
    if not data:
      raise ValueError("analysis.reanalyze params" + " has no data")

    roots = data.get("roots", [])
    if roots:
      roots = roots

    return cls(roots=roots)

  def to_json(self):
    result = {}
    if self.roots:
      result["roots"] = self.roots
    return result

  def to_request(self, id):
    assert id is not None, "must provide an id for the request"
    return Request(id, "analysis.reanalyze", self)

  def __str__(self):
    return json.dumps(self.to_json())


# analysis.reanalyze result
class AnalysisReanalyzeResult(object):
  def to_response(self, id):
    assert id is not None, "must provide an id for the response"
    return Response(id, result=None)



# analysis.setAnalysisRoots params
#
# {
#   "included": List<FilePath>
#   "excluded": List<FilePath>
#   "packageRoots": optional Map<FilePath, FilePath>
# }
class AnalysisSetAnalysisRootsParams(object):
  def __init__(self, included, excluded, packageRoots={}):
    # A list of the files and directories that should be analyzed.
    self.included = included
    # A list of the files and directories within the included directories that
    # should not be analyzed.
    self.excluded = excluded
    # A mapping from source directories to target directories that should
    # override the normal package: URI resolution mechanism. The analyzer will
    # behave as though each source directory in the map contains a special
    # pubspec.yaml file which resolves any package: URI to the corresponding
    # path within the target directory. The effect is the same as specifying
    # the target directory as a "--package_root" parameter to the Dart VM when
    # executing any Dart file inside the source directory.
    #
    # Files in any directories that are not overridden by this mapping have
    # their package: URI's resolved using the normal pubspec.yaml mechanism. If
    # this field is absent, or the empty map is specified, that indicates that
    # the normal pubspec.yaml mechanism should always be used.
    self.packageRoots = packageRoots

  @classmethod
  def from_json(cls, data):
    if not data:
      raise ValueError("analysis.setAnalysisRoots params" + " has no data")

    included = data["included"]
    excluded = data["excluded"]
    packageRoots = data.get("packageRoots", {})
    if packageRoots:
      packageRoots = packageRoots

    return cls(included, excluded, packageRoots=packageRoots)

  def to_json(self):
    result = {}
    result["included"] = self.included
    result["excluded"] = self.excluded
    if self.packageRoots:
      result["packageRoots"] = {k: v for (k, v) in self.packageRoots.items()}
    return result

  def to_request(self, id):
    assert id is not None, "must provide an id for the request"
    return Request(id, "analysis.setAnalysisRoots", self)

  def __str__(self):
    return json.dumps(self.to_json())


# analysis.setAnalysisRoots result
class AnalysisSetAnalysisRootsResult(object):
  def to_response(self, id):
    assert id is not None, "must provide an id for the response"
    return Response(id, result=None)



# analysis.setPriorityFiles params
#
# {
#   "files": List<FilePath>
# }
class AnalysisSetPriorityFilesParams(object):
  def __init__(self, files):
    # The files that are to be a priority for analysis.
    self.files = files

  @classmethod
  def from_json(cls, data):
    if not data:
      raise ValueError("analysis.setPriorityFiles params" + " has no data")

    files = data["files"]

    return cls(files)

  def to_json(self):
    result = {}
    result["files"] = self.files
    return result

  def to_request(self, id):
    assert id is not None, "must provide an id for the request"
    return Request(id, "analysis.setPriorityFiles", self)

  def __str__(self):
    return json.dumps(self.to_json())


# analysis.setPriorityFiles result
class AnalysisSetPriorityFilesResult(object):
  def to_response(self, id):
    assert id is not None, "must provide an id for the response"
    return Response(id, result=None)



# analysis.setSubscriptions params
#
# {
#   "subscriptions": Map<AnalysisService, List<FilePath>>
# }
class AnalysisSetSubscriptionsParams(object):
  def __init__(self, subscriptions):
    # A table mapping services to a list of the files being subscribed to the
    # service.
    self.subscriptions = subscriptions

  @classmethod
  def from_json(cls, data):
    if not data:
      raise ValueError("analysis.setSubscriptions params" + " has no data")

    subscriptions = data["subscriptions"]

    return cls(subscriptions)

  def to_json(self):
    result = {}
    result["subscriptions"] = {k: v for (k, v) in self.subscriptions.items()}
    return result

  def to_request(self, id):
    assert id is not None, "must provide an id for the request"
    return Request(id, "analysis.setSubscriptions", self)

  def __str__(self):
    return json.dumps(self.to_json())


# analysis.setSubscriptions result
class AnalysisSetSubscriptionsResult(object):
  def to_response(self, id):
    assert id is not None, "must provide an id for the response"
    return Response(id, result=None)



# analysis.updateContent params
#
# {
#   "files": Map<FilePath, AddContentOverlay | ChangeContentOverlay | RemoveContentOverlay>
# }
class AnalysisUpdateContentParams(object):
  def __init__(self, files):
    # A table mapping the files whose content has changed to a description of
    # the content change.
    self.files = files

  @classmethod
  def from_json(cls, data):
    if not data:
      raise ValueError("analysis.updateContent params" + " has no data")

    files = data["files"]

    return cls(files)

  def to_json(self):
    result = {}
    result["files"] = {k: v.to_json() for (k, v) in self.files.items()}
    return result

  def to_request(self, id):
    assert id is not None, "must provide an id for the request"
    return Request(id, "analysis.updateContent", self)

  def __str__(self):
    return json.dumps(self.to_json())



# analysis.updateContent result
#
# {
# }
class AnalysisUpdateContentResult(object):

  @classmethod
  def from_json(cls, data):
    return cls()

  def to_json(self):
    result = {}
    return result

  def to_response(self, id):
    assert id is not None, "must provide an id for the response"
    return Response(id, result=self)

  def __str__(self):
    return json.dumps(self.to_json())



# analysis.updateOptions params
#
# {
#   "options": AnalysisOptions
# }
class AnalysisUpdateOptionsParams(object):
  def __init__(self, options):
    # The options that are to be used to control analysis.
    self.options = options

  @classmethod
  def from_json(cls, data):
    if not data:
      raise ValueError("analysis.updateOptions params" + " has no data")

    options = AnalysisOptions.from_json(data["options"])

    return cls(options)

  def to_json(self):
    result = {}
    result["options"] = self.options.to_json()
    return result

  def to_request(self, id):
    assert id is not None, "must provide an id for the request"
    return Request(id, "analysis.updateOptions", self)

  def __str__(self):
    return json.dumps(self.to_json())


# analysis.updateOptions result
class AnalysisUpdateOptionsResult(object):
  def to_response(self, id):
    assert id is not None, "must provide an id for the response"
    return Response(id, result=None)



# analysis.errors params
#
# {
#   "file": FilePath
#   "errors": List<AnalysisError>
# }
class AnalysisErrorsParams(object):
  def __init__(self, file, errors):
    # The file containing the errors.
    self.file = file
    # The errors contained in the file.
    self.errors = errors

  @classmethod
  def from_json(cls, data):
    if not data:
      raise ValueError("analysis.errors params" + " has no data")

    file = data["file"]
    errors = [AnalysisError.from_json(x) for x in data["errors"]]

    return cls(file, errors)

  def to_json(self):
    result = {}
    result["file"] = self.file
    result["errors"] = [x.to_json() for x in self.errors]
    return result

  def to_notification(self):
    return Notification("analysis.errors", self);

  def __str__(self):
    return json.dumps(self.to_json())



# analysis.flushResults params
#
# {
#   "files": List<FilePath>
# }
class AnalysisFlushResultsParams(object):
  def __init__(self, files):
    # The files that are no longer being analyzed.
    self.files = files

  @classmethod
  def from_json(cls, data):
    if not data:
      raise ValueError("analysis.flushResults params" + " has no data")

    files = data["files"]

    return cls(files)

  def to_json(self):
    result = {}
    result["files"] = self.files
    return result

  def to_notification(self):
    return Notification("analysis.flushResults", self);

  def __str__(self):
    return json.dumps(self.to_json())



# analysis.folding params
#
# {
#   "file": FilePath
#   "regions": List<FoldingRegion>
# }
class AnalysisFoldingParams(object):
  def __init__(self, file, regions):
    # The file containing the folding regions.
    self.file = file
    # The folding regions contained in the file.
    self.regions = regions

  @classmethod
  def from_json(cls, data):
    if not data:
      raise ValueError("analysis.folding params" + " has no data")

    file = data["file"]
    regions = [FoldingRegion.from_json(x) for x in data["regions"]]

    return cls(file, regions)

  def to_json(self):
    result = {}
    result["file"] = self.file
    result["regions"] = [x.to_json() for x in self.regions]
    return result

  def to_notification(self):
    return Notification("analysis.folding", self);

  def __str__(self):
    return json.dumps(self.to_json())



# analysis.highlights params
#
# {
#   "file": FilePath
#   "regions": List<HighlightRegion>
# }
class AnalysisHighlightsParams(object):
  def __init__(self, file, regions):
    # The file containing the highlight regions.
    self.file = file
    # The highlight regions contained in the file. Each highlight region
    # represents a particular syntactic or semantic meaning associated with
    # some range. Note that the highlight regions that are returned can overlap
    # other highlight regions if there is more than one meaning associated with
    # a particular region.
    self.regions = regions

  @classmethod
  def from_json(cls, data):
    if not data:
      raise ValueError("analysis.highlights params" + " has no data")

    file = data["file"]
    regions = [HighlightRegion.from_json(x) for x in data["regions"]]

    return cls(file, regions)

  def to_json(self):
    result = {}
    result["file"] = self.file
    result["regions"] = [x.to_json() for x in self.regions]
    return result

  def to_notification(self):
    return Notification("analysis.highlights", self);

  def __str__(self):
    return json.dumps(self.to_json())



# analysis.invalidate params
#
# {
#   "file": FilePath
#   "offset": int
#   "length": int
#   "delta": int
# }
class AnalysisInvalidateParams(object):
  def __init__(self, file, offset, length, delta):
    # The file whose information has been invalidated.
    self.file = file
    # The offset of the invalidated region.
    self.offset = offset
    # The length of the invalidated region.
    self.length = length
    # The delta to be applied to the offsets in information that follows the
    # invalidated region in order to update it so that it doesn't need to be
    # re-requested.
    self.delta = delta

  @classmethod
  def from_json(cls, data):
    if not data:
      raise ValueError("analysis.invalidate params" + " has no data")

    file = data["file"]
    offset = data["offset"]
    length = data["length"]
    delta = data["delta"]

    return cls(file, offset, length, delta)

  def to_json(self):
    result = {}
    result["file"] = self.file
    result["offset"] = self.offset
    result["length"] = self.length
    result["delta"] = self.delta
    return result

  def to_notification(self):
    return Notification("analysis.invalidate", self);

  def __str__(self):
    return json.dumps(self.to_json())



# analysis.navigation params
#
# {
#   "file": FilePath
#   "regions": List<NavigationRegion>
#   "targets": List<NavigationTarget>
#   "files": List<FilePath>
# }
class AnalysisNavigationParams(object):
  def __init__(self, file, regions, targets, files):
    # The file containing the navigation regions.
    self.file = file
    # The navigation regions contained in the file. The regions are sorted by
    # their offsets. Each navigation region represents a list of targets
    # associated with some range. The lists will usually contain a single
    # target, but can contain more in the case of a part that is included in
    # multiple libraries or in Dart code that is compiled against multiple
    # versions of a package. Note that the navigation regions that are returned
    # do not overlap other navigation regions.
    self.regions = regions
    # The navigation targets referenced in the file. They are referenced by
    # NavigationRegions by their index in this array.
    self.targets = targets
    # The files containing navigation targets referenced in the file. They are
    # referenced by NavigationTargets by their index in this array.
    self.files = files

  @classmethod
  def from_json(cls, data):
    if not data:
      raise ValueError("analysis.navigation params" + " has no data")

    file = data["file"]
    regions = [NavigationRegion.from_json(x) for x in data["regions"]]
    targets = [NavigationTarget.from_json(x) for x in data["targets"]]
    files = data["files"]

    return cls(file, regions, targets, files)

  def to_json(self):
    result = {}
    result["file"] = self.file
    result["regions"] = [x.to_json() for x in self.regions]
    result["targets"] = [x.to_json() for x in self.targets]
    result["files"] = self.files
    return result

  def to_notification(self):
    return Notification("analysis.navigation", self);

  def __str__(self):
    return json.dumps(self.to_json())



# analysis.occurrences params
#
# {
#   "file": FilePath
#   "occurrences": List<Occurrences>
# }
class AnalysisOccurrencesParams(object):
  def __init__(self, file, occurrences):
    # The file in which the references occur.
    self.file = file
    # The occurrences of references to elements within the file.
    self.occurrences = occurrences

  @classmethod
  def from_json(cls, data):
    if not data:
      raise ValueError("analysis.occurrences params" + " has no data")

    file = data["file"]
    occurrences = [Occurrences.from_json(x) for x in data["occurrences"]]

    return cls(file, occurrences)

  def to_json(self):
    result = {}
    result["file"] = self.file
    result["occurrences"] = [x.to_json() for x in self.occurrences]
    return result

  def to_notification(self):
    return Notification("analysis.occurrences", self);

  def __str__(self):
    return json.dumps(self.to_json())



# analysis.outline params
#
# {
#   "file": FilePath
#   "outline": Outline
# }
class AnalysisOutlineParams(object):
  def __init__(self, file, outline):
    # The file with which the outline is associated.
    self.file = file
    # The outline associated with the file.
    self.outline = outline

  @classmethod
  def from_json(cls, data):
    if not data:
      raise ValueError("analysis.outline params" + " has no data")

    file = data["file"]
    outline = Outline.from_json(data["outline"])

    return cls(file, outline)

  def to_json(self):
    result = {}
    result["file"] = self.file
    result["outline"] = self.outline.to_json()
    return result

  def to_notification(self):
    return Notification("analysis.outline", self);

  def __str__(self):
    return json.dumps(self.to_json())



# analysis.overrides params
#
# {
#   "file": FilePath
#   "overrides": List<Override>
# }
class AnalysisOverridesParams(object):
  def __init__(self, file, overrides):
    # The file with which the overrides are associated.
    self.file = file
    # The overrides associated with the file.
    self.overrides = overrides

  @classmethod
  def from_json(cls, data):
    if not data:
      raise ValueError("analysis.overrides params" + " has no data")

    file = data["file"]
    overrides = [Override.from_json(x) for x in data["overrides"]]

    return cls(file, overrides)

  def to_json(self):
    result = {}
    result["file"] = self.file
    result["overrides"] = [x.to_json() for x in self.overrides]
    return result

  def to_notification(self):
    return Notification("analysis.overrides", self);

  def __str__(self):
    return json.dumps(self.to_json())



# completion.getSuggestions params
#
# {
#   "file": FilePath
#   "offset": int
# }
class CompletionGetSuggestionsParams(object):
  def __init__(self, file, offset):
    # The file containing the point at which suggestions are to be made.
    self.file = file
    # The offset within the file at which suggestions are to be made.
    self.offset = offset

  @classmethod
  def from_json(cls, data):
    if not data:
      raise ValueError("completion.getSuggestions params" + " has no data")

    file = data["file"]
    offset = data["offset"]

    return cls(file, offset)

  def to_json(self):
    result = {}
    result["file"] = self.file
    result["offset"] = self.offset
    return result

  def to_request(self, id):
    assert id is not None, "must provide an id for the request"
    return Request(id, "completion.getSuggestions", self)

  def __str__(self):
    return json.dumps(self.to_json())



# completion.getSuggestions result
#
# {
#   "id": CompletionId
# }
class CompletionGetSuggestionsResult(object):
  def __init__(self, id):
    # The identifier used to associate results with this completion request.
    self.id = id

  @classmethod
  def from_json(cls, data):
    if not data:
      raise ValueError("completion.getSuggestions result" + " has no data")

    id = data["id"]

    return cls(id)

  def to_json(self):
    result = {}
    result["id"] = self.id
    return result

  def to_response(self, id):
    assert id is not None, "must provide an id for the response"
    return Response(id, result=self)

  def __str__(self):
    return json.dumps(self.to_json())



# completion.results params
#
# {
#   "id": CompletionId
#   "replacementOffset": int
#   "replacementLength": int
#   "results": List<CompletionSuggestion>
#   "isLast": bool
# }
class CompletionResultsParams(object):
  def __init__(self, id, replacementOffset, replacementLength, results, isLast):
    # The id associated with the completion.
    self.id = id
    # The offset of the start of the text to be replaced. This will be
    # different than the offset used to request the completion suggestions if
    # there was a portion of an identifier before the original offset. In
    # particular, the replacementOffset will be the offset of the beginning of
    # said identifier.
    self.replacementOffset = replacementOffset
    # The length of the text to be replaced if the remainder of the identifier
    # containing the cursor is to be replaced when the suggestion is applied
    # (that is, the number of characters in the existing identifier).
    self.replacementLength = replacementLength
    # The completion suggestions being reported. The notification contains all
    # possible completions at the requested cursor position, even those that do
    # not match the characters the user has already typed. This allows the
    # client to respond to further keystrokes from the user without having to
    # make additional requests.
    self.results = results
    # True if this is that last set of results that will be returned for the
    # indicated completion.
    self.isLast = isLast

  @classmethod
  def from_json(cls, data):
    if not data:
      raise ValueError("completion.results params" + " has no data")

    id = data["id"]
    replacementOffset = data["replacementOffset"]
    replacementLength = data["replacementLength"]
    results = [CompletionSuggestion.from_json(x) for x in data["results"]]
    isLast = data["isLast"]

    return cls(id, replacementOffset, replacementLength, results, isLast)

  def to_json(self):
    result = {}
    result["id"] = self.id
    result["replacementOffset"] = self.replacementOffset
    result["replacementLength"] = self.replacementLength
    result["results"] = [x.to_json() for x in self.results]
    result["isLast"] = self.isLast
    return result

  def to_notification(self):
    return Notification("completion.results", self);

  def __str__(self):
    return json.dumps(self.to_json())



# search.findElementReferences params
#
# {
#   "file": FilePath
#   "offset": int
#   "includePotential": bool
# }
class SearchFindElementReferencesParams(object):
  def __init__(self, file, offset, includePotential):
    # The file containing the declaration of or reference to the element used
    # to define the search.
    self.file = file
    # The offset within the file of the declaration of or reference to the
    # element.
    self.offset = offset
    # True if potential matches are to be included in the results.
    self.includePotential = includePotential

  @classmethod
  def from_json(cls, data):
    if not data:
      raise ValueError("search.findElementReferences params" + " has no data")

    file = data["file"]
    offset = data["offset"]
    includePotential = data["includePotential"]

    return cls(file, offset, includePotential)

  def to_json(self):
    result = {}
    result["file"] = self.file
    result["offset"] = self.offset
    result["includePotential"] = self.includePotential
    return result

  def to_request(self, id):
    assert id is not None, "must provide an id for the request"
    return Request(id, "search.findElementReferences", self)

  def __str__(self):
    return json.dumps(self.to_json())



# search.findElementReferences result
#
# {
#   "id": optional SearchId
#   "element": optional Element
# }
class SearchFindElementReferencesResult(object):
  def __init__(self, id='', element=None):
    # The identifier used to associate results with this search request.
    #
    # If no element was found at the given location, this field will be absent,
    # and no results will be reported via the search.results notification.
    self.id = id
    # The element referenced or defined at the given offset and whose
    # references will be returned in the search results.
    #
    # If no element was found at the given location, this field will be absent.
    self.element = element

  @classmethod
  def from_json(cls, data):
    if not data:
      raise ValueError("search.findElementReferences result" + " has no data")

    id = data.get("id", '')
    if id:
      id = id
    element = data.get("element", None)
    if element:
      element = Element.from_json(element)

    return cls(id=id, element=element)

  def to_json(self):
    result = {}
    if self.id:
      result["id"] = self.id
    if self.element:
      result["element"] = self.element.to_json()
    return result

  def to_response(self, id):
    assert id is not None, "must provide an id for the response"
    return Response(id, result=self)

  def __str__(self):
    return json.dumps(self.to_json())



# search.findMemberDeclarations params
#
# {
#   "name": String
# }
class SearchFindMemberDeclarationsParams(object):
  def __init__(self, name):
    # The name of the declarations to be found.
    self.name = name

  @classmethod
  def from_json(cls, data):
    if not data:
      raise ValueError("search.findMemberDeclarations params" + " has no data")

    name = data["name"]

    return cls(name)

  def to_json(self):
    result = {}
    result["name"] = self.name
    return result

  def to_request(self, id):
    assert id is not None, "must provide an id for the request"
    return Request(id, "search.findMemberDeclarations", self)

  def __str__(self):
    return json.dumps(self.to_json())



# search.findMemberDeclarations result
#
# {
#   "id": SearchId
# }
class SearchFindMemberDeclarationsResult(object):
  def __init__(self, id):
    # The identifier used to associate results with this search request.
    self.id = id

  @classmethod
  def from_json(cls, data):
    if not data:
      raise ValueError("search.findMemberDeclarations result" + " has no data")

    id = data["id"]

    return cls(id)

  def to_json(self):
    result = {}
    result["id"] = self.id
    return result

  def to_response(self, id):
    assert id is not None, "must provide an id for the response"
    return Response(id, result=self)

  def __str__(self):
    return json.dumps(self.to_json())



# search.findMemberReferences params
#
# {
#   "name": String
# }
class SearchFindMemberReferencesParams(object):
  def __init__(self, name):
    # The name of the references to be found.
    self.name = name

  @classmethod
  def from_json(cls, data):
    if not data:
      raise ValueError("search.findMemberReferences params" + " has no data")

    name = data["name"]

    return cls(name)

  def to_json(self):
    result = {}
    result["name"] = self.name
    return result

  def to_request(self, id):
    assert id is not None, "must provide an id for the request"
    return Request(id, "search.findMemberReferences", self)

  def __str__(self):
    return json.dumps(self.to_json())



# search.findMemberReferences result
#
# {
#   "id": SearchId
# }
class SearchFindMemberReferencesResult(object):
  def __init__(self, id):
    # The identifier used to associate results with this search request.
    self.id = id

  @classmethod
  def from_json(cls, data):
    if not data:
      raise ValueError("search.findMemberReferences result" + " has no data")

    id = data["id"]

    return cls(id)

  def to_json(self):
    result = {}
    result["id"] = self.id
    return result

  def to_response(self, id):
    assert id is not None, "must provide an id for the response"
    return Response(id, result=self)

  def __str__(self):
    return json.dumps(self.to_json())



# search.findTopLevelDeclarations params
#
# {
#   "pattern": String
# }
class SearchFindTopLevelDeclarationsParams(object):
  def __init__(self, pattern):
    # The regular expression used to match the names of the declarations to be
    # found.
    self.pattern = pattern

  @classmethod
  def from_json(cls, data):
    if not data:
      raise ValueError("search.findTopLevelDeclarations params" + " has no data")

    pattern = data["pattern"]

    return cls(pattern)

  def to_json(self):
    result = {}
    result["pattern"] = self.pattern
    return result

  def to_request(self, id):
    assert id is not None, "must provide an id for the request"
    return Request(id, "search.findTopLevelDeclarations", self)

  def __str__(self):
    return json.dumps(self.to_json())



# search.findTopLevelDeclarations result
#
# {
#   "id": SearchId
# }
class SearchFindTopLevelDeclarationsResult(object):
  def __init__(self, id):
    # The identifier used to associate results with this search request.
    self.id = id

  @classmethod
  def from_json(cls, data):
    if not data:
      raise ValueError("search.findTopLevelDeclarations result" + " has no data")

    id = data["id"]

    return cls(id)

  def to_json(self):
    result = {}
    result["id"] = self.id
    return result

  def to_response(self, id):
    assert id is not None, "must provide an id for the response"
    return Response(id, result=self)

  def __str__(self):
    return json.dumps(self.to_json())



# search.getTypeHierarchy params
#
# {
#   "file": FilePath
#   "offset": int
# }
class SearchGetTypeHierarchyParams(object):
  def __init__(self, file, offset):
    # The file containing the declaration or reference to the type for which a
    # hierarchy is being requested.
    self.file = file
    # The offset of the name of the type within the file.
    self.offset = offset

  @classmethod
  def from_json(cls, data):
    if not data:
      raise ValueError("search.getTypeHierarchy params" + " has no data")

    file = data["file"]
    offset = data["offset"]

    return cls(file, offset)

  def to_json(self):
    result = {}
    result["file"] = self.file
    result["offset"] = self.offset
    return result

  def to_request(self, id):
    assert id is not None, "must provide an id for the request"
    return Request(id, "search.getTypeHierarchy", self)

  def __str__(self):
    return json.dumps(self.to_json())



# search.getTypeHierarchy result
#
# {
#   "hierarchyItems": optional List<TypeHierarchyItem>
# }
class SearchGetTypeHierarchyResult(object):
  def __init__(self, hierarchyItems=[]):
    # A list of the types in the requested hierarchy. The first element of the
    # list is the item representing the type for which the hierarchy was
    # requested. The index of other elements of the list is unspecified, but
    # correspond to the integers used to reference supertype and subtype items
    # within the items.
    #
    # This field will be absent if the code at the given file and offset does
    # not represent a type, or if the file has not been sufficiently analyzed
    # to allow a type hierarchy to be produced.
    self.hierarchyItems = hierarchyItems

  @classmethod
  def from_json(cls, data):
    if not data:
      raise ValueError("search.getTypeHierarchy result" + " has no data")

    hierarchyItems = data.get("hierarchyItems", [])
    if hierarchyItems:
      hierarchyItems = [TypeHierarchyItem.from_json(x) for x in hierarchyItems]

    return cls(hierarchyItems=hierarchyItems)

  def to_json(self):
    result = {}
    if self.hierarchyItems:
      result["hierarchyItems"] = [x.to_json() for x in self.hierarchyItems]
    return result

  def to_response(self, id):
    assert id is not None, "must provide an id for the response"
    return Response(id, result=self)

  def __str__(self):
    return json.dumps(self.to_json())



# search.results params
#
# {
#   "id": SearchId
#   "results": List<SearchResult>
#   "isLast": bool
# }
class SearchResultsParams(object):
  def __init__(self, id, results, isLast):
    # The id associated with the search.
    self.id = id
    # The search results being reported.
    self.results = results
    # True if this is that last set of results that will be returned for the
    # indicated search.
    self.isLast = isLast

  @classmethod
  def from_json(cls, data):
    if not data:
      raise ValueError("search.results params" + " has no data")

    id = data["id"]
    results = [SearchResult.from_json(x) for x in data["results"]]
    isLast = data["isLast"]

    return cls(id, results, isLast)

  def to_json(self):
    result = {}
    result["id"] = self.id
    result["results"] = [x.to_json() for x in self.results]
    result["isLast"] = self.isLast
    return result

  def to_notification(self):
    return Notification("search.results", self);

  def __str__(self):
    return json.dumps(self.to_json())



# edit.format params
#
# {
#   "file": FilePath
#   "selectionOffset": int
#   "selectionLength": int
# }
class EditFormatParams(object):
  def __init__(self, file, selectionOffset, selectionLength):
    # The file containing the code to be formatted.
    self.file = file
    # The offset of the current selection in the file.
    self.selectionOffset = selectionOffset
    # The length of the current selection in the file.
    self.selectionLength = selectionLength

  @classmethod
  def from_json(cls, data):
    if not data:
      raise ValueError("edit.format params" + " has no data")

    file = data["file"]
    selectionOffset = data["selectionOffset"]
    selectionLength = data["selectionLength"]

    return cls(file, selectionOffset, selectionLength)

  def to_json(self):
    result = {}
    result["file"] = self.file
    result["selectionOffset"] = self.selectionOffset
    result["selectionLength"] = self.selectionLength
    return result

  def to_request(self, id):
    assert id is not None, "must provide an id for the request"
    return Request(id, "edit.format", self)

  def __str__(self):
    return json.dumps(self.to_json())



# edit.format result
#
# {
#   "edits": List<SourceEdit>
#   "selectionOffset": int
#   "selectionLength": int
# }
class EditFormatResult(object):
  def __init__(self, edits, selectionOffset, selectionLength):
    # The edit(s) to be applied in order to format the code. The list will be
    # empty if the code was already formatted (there are no changes).
    self.edits = edits
    # The offset of the selection after formatting the code.
    self.selectionOffset = selectionOffset
    # The length of the selection after formatting the code.
    self.selectionLength = selectionLength

  @classmethod
  def from_json(cls, data):
    if not data:
      raise ValueError("edit.format result" + " has no data")

    edits = [SourceEdit.from_json(x) for x in data["edits"]]
    selectionOffset = data["selectionOffset"]
    selectionLength = data["selectionLength"]

    return cls(edits, selectionOffset, selectionLength)

  def to_json(self):
    result = {}
    result["edits"] = [x.to_json() for x in self.edits]
    result["selectionOffset"] = self.selectionOffset
    result["selectionLength"] = self.selectionLength
    return result

  def to_response(self, id):
    assert id is not None, "must provide an id for the response"
    return Response(id, result=self)

  def __str__(self):
    return json.dumps(self.to_json())



# edit.getAssists params
#
# {
#   "file": FilePath
#   "offset": int
#   "length": int
# }
class EditGetAssistsParams(object):
  def __init__(self, file, offset, length):
    # The file containing the code for which assists are being requested.
    self.file = file
    # The offset of the code for which assists are being requested.
    self.offset = offset
    # The length of the code for which assists are being requested.
    self.length = length

  @classmethod
  def from_json(cls, data):
    if not data:
      raise ValueError("edit.getAssists params" + " has no data")

    file = data["file"]
    offset = data["offset"]
    length = data["length"]

    return cls(file, offset, length)

  def to_json(self):
    result = {}
    result["file"] = self.file
    result["offset"] = self.offset
    result["length"] = self.length
    return result

  def to_request(self, id):
    assert id is not None, "must provide an id for the request"
    return Request(id, "edit.getAssists", self)

  def __str__(self):
    return json.dumps(self.to_json())



# edit.getAssists result
#
# {
#   "assists": List<SourceChange>
# }
class EditGetAssistsResult(object):
  def __init__(self, assists):
    # The assists that are available at the given location.
    self.assists = assists

  @classmethod
  def from_json(cls, data):
    if not data:
      raise ValueError("edit.getAssists result" + " has no data")

    assists = [SourceChange.from_json(x) for x in data["assists"]]

    return cls(assists)

  def to_json(self):
    result = {}
    result["assists"] = [x.to_json() for x in self.assists]
    return result

  def to_response(self, id):
    assert id is not None, "must provide an id for the response"
    return Response(id, result=self)

  def __str__(self):
    return json.dumps(self.to_json())



# edit.getAvailableRefactorings params
#
# {
#   "file": FilePath
#   "offset": int
#   "length": int
# }
class EditGetAvailableRefactoringsParams(object):
  def __init__(self, file, offset, length):
    # The file containing the code on which the refactoring would be based.
    self.file = file
    # The offset of the code on which the refactoring would be based.
    self.offset = offset
    # The length of the code on which the refactoring would be based.
    self.length = length

  @classmethod
  def from_json(cls, data):
    if not data:
      raise ValueError("edit.getAvailableRefactorings params" + " has no data")

    file = data["file"]
    offset = data["offset"]
    length = data["length"]

    return cls(file, offset, length)

  def to_json(self):
    result = {}
    result["file"] = self.file
    result["offset"] = self.offset
    result["length"] = self.length
    return result

  def to_request(self, id):
    assert id is not None, "must provide an id for the request"
    return Request(id, "edit.getAvailableRefactorings", self)

  def __str__(self):
    return json.dumps(self.to_json())



# edit.getAvailableRefactorings result
#
# {
#   "kinds": List<RefactoringKind>
# }
class EditGetAvailableRefactoringsResult(object):
  def __init__(self, kinds):
    # The kinds of refactorings that are valid for the given selection.
    self.kinds = kinds

  @classmethod
  def from_json(cls, data):
    if not data:
      raise ValueError("edit.getAvailableRefactorings result" + " has no data")

    kinds = data["kinds"]

    return cls(kinds)

  def to_json(self):
    result = {}
    result["kinds"] = self.kinds
    return result

  def to_response(self, id):
    assert id is not None, "must provide an id for the response"
    return Response(id, result=self)

  def __str__(self):
    return json.dumps(self.to_json())



# edit.getFixes params
#
# {
#   "file": FilePath
#   "offset": int
# }
class EditGetFixesParams(object):
  def __init__(self, file, offset):
    # The file containing the errors for which fixes are being requested.
    self.file = file
    # The offset used to select the errors for which fixes will be returned.
    self.offset = offset

  @classmethod
  def from_json(cls, data):
    if not data:
      raise ValueError("edit.getFixes params" + " has no data")

    file = data["file"]
    offset = data["offset"]

    return cls(file, offset)

  def to_json(self):
    result = {}
    result["file"] = self.file
    result["offset"] = self.offset
    return result

  def to_request(self, id):
    assert id is not None, "must provide an id for the request"
    return Request(id, "edit.getFixes", self)

  def __str__(self):
    return json.dumps(self.to_json())



# edit.getFixes result
#
# {
#   "fixes": List<AnalysisErrorFixes>
# }
class EditGetFixesResult(object):
  def __init__(self, fixes):
    # The fixes that are available for the errors at the given offset.
    self.fixes = fixes

  @classmethod
  def from_json(cls, data):
    if not data:
      raise ValueError("edit.getFixes result" + " has no data")

    fixes = [AnalysisErrorFixes.from_json(x) for x in data["fixes"]]

    return cls(fixes)

  def to_json(self):
    result = {}
    result["fixes"] = [x.to_json() for x in self.fixes]
    return result

  def to_response(self, id):
    assert id is not None, "must provide an id for the response"
    return Response(id, result=self)

  def __str__(self):
    return json.dumps(self.to_json())



# edit.getRefactoring params
#
# {
#   "kind": RefactoringKind
#   "file": FilePath
#   "offset": int
#   "length": int
#   "validateOnly": bool
#   "options": optional RefactoringOptions
# }
class EditGetRefactoringParams(object):
  def __init__(self, kind, file, offset, length, validateOnly, options=None):
    # The kind of refactoring to be performed.
    self.kind = kind
    # The file containing the code involved in the refactoring.
    self.file = file
    # The offset of the region involved in the refactoring.
    self.offset = offset
    # The length of the region involved in the refactoring.
    self.length = length
    # True if the client is only requesting that the values of the options be
    # validated and no change be generated.
    self.validateOnly = validateOnly
    # Data used to provide values provided by the user. The structure of the
    # data is dependent on the kind of refactoring being performed. The data
    # that is expected is documented in the section titled Refactorings,
    # labeled as “Options”. This field can be omitted if the refactoring does
    # not require any options or if the values of those options are not known.
    self.options = options

  @classmethod
  def from_json(cls, data):
    if not data:
      raise ValueError("edit.getRefactoring params" + " has no data")

    kind = data["kind"]
    file = data["file"]
    offset = data["offset"]
    length = data["length"]
    validateOnly = data["validateOnly"]
    options = data.get("options", None)
    if options:
      options = RefactoringOptions.from_json(options)

    return cls(kind, file, offset, length, validateOnly, options=options)

  def to_json(self):
    result = {}
    result["kind"] = self.kind
    result["file"] = self.file
    result["offset"] = self.offset
    result["length"] = self.length
    result["validateOnly"] = self.validateOnly
    if self.options:
      result["options"] = self.options.to_json()
    return result

  def to_request(self, id):
    assert id is not None, "must provide an id for the request"
    return Request(id, "edit.getRefactoring", self)

  def __str__(self):
    return json.dumps(self.to_json())



# edit.getRefactoring result
#
# {
#   "initialProblems": List<RefactoringProblem>
#   "optionsProblems": List<RefactoringProblem>
#   "finalProblems": List<RefactoringProblem>
#   "feedback": optional RefactoringFeedback
#   "change": optional SourceChange
#   "potentialEdits": optional List<String>
# }
class EditGetRefactoringResult(object):
  def __init__(self, initialProblems, optionsProblems, finalProblems, feedback=None, change=None, potentialEdits=[]):
    # The initial status of the refactoring, i.e. problems related to the
    # context in which the refactoring is requested. The array will be empty if
    # there are no known problems.
    self.initialProblems = initialProblems
    # The options validation status, i.e. problems in the given options, such
    # as light-weight validation of a new name, flags compatibility, etc. The
    # array will be empty if there are no known problems.
    self.optionsProblems = optionsProblems
    # The final status of the refactoring, i.e. problems identified in the
    # result of a full, potentially expensive validation and / or change
    # creation. The array will be empty if there are no known problems.
    self.finalProblems = finalProblems
    # Data used to provide feedback to the user. The structure of the data is
    # dependent on the kind of refactoring being created. The data that is
    # returned is documented in the section titled Refactorings, labeled as
    # “Feedback”.
    self.feedback = feedback
    # The changes that are to be applied to affect the refactoring. This field
    # will be omitted if there are problems that prevent a set of changes from
    # being computed, such as having no options specified for a refactoring
    # that requires them, or if only validation was requested.
    self.change = change
    # The ids of source edits that are not known to be valid. An edit is not
    # known to be valid if there was insufficient type information for the
    # server to be able to determine whether or not the code needs to be
    # modified, such as when a member is being renamed and there is a reference
    # to a member from an unknown type. This field will be omitted if the
    # change field is omitted or if there are no potential edits for the
    # refactoring.
    self.potentialEdits = potentialEdits

  @classmethod
  def from_json(cls, data):
    if not data:
      raise ValueError("edit.getRefactoring result" + " has no data")

    initialProblems = [RefactoringProblem.from_json(x) for x in data["initialProblems"]]
    optionsProblems = [RefactoringProblem.from_json(x) for x in data["optionsProblems"]]
    finalProblems = [RefactoringProblem.from_json(x) for x in data["finalProblems"]]
    feedback = data.get("feedback", None)
    if feedback:
      feedback = RefactoringFeedback.from_json(feedback)
    change = data.get("change", None)
    if change:
      change = SourceChange.from_json(change)
    potentialEdits = data.get("potentialEdits", [])
    if potentialEdits:
      potentialEdits = potentialEdits

    return cls(initialProblems, optionsProblems, finalProblems, feedback=feedback, change=change, potentialEdits=potentialEdits)

  def to_json(self):
    result = {}
    result["initialProblems"] = [x.to_json() for x in self.initialProblems]
    result["optionsProblems"] = [x.to_json() for x in self.optionsProblems]
    result["finalProblems"] = [x.to_json() for x in self.finalProblems]
    if self.feedback:
      result["feedback"] = self.feedback.to_json()
    if self.change:
      result["change"] = self.change.to_json()
    if self.potentialEdits:
      result["potentialEdits"] = self.potentialEdits
    return result

  def to_response(self, id):
    assert id is not None, "must provide an id for the response"
    return Response(id, result=self)

  def __str__(self):
    return json.dumps(self.to_json())



# edit.sortMembers params
#
# {
#   "file": FilePath
# }
class EditSortMembersParams(object):
  def __init__(self, file):
    # The Dart file to sort.
    self.file = file

  @classmethod
  def from_json(cls, data):
    if not data:
      raise ValueError("edit.sortMembers params" + " has no data")

    file = data["file"]

    return cls(file)

  def to_json(self):
    result = {}
    result["file"] = self.file
    return result

  def to_request(self, id):
    assert id is not None, "must provide an id for the request"
    return Request(id, "edit.sortMembers", self)

  def __str__(self):
    return json.dumps(self.to_json())



# edit.sortMembers result
#
# {
#   "edit": SourceFileEdit
# }
class EditSortMembersResult(object):
  def __init__(self, edit):
    # The file edit that is to be applied to the given file to effect the
    # sorting.
    self.edit = edit

  @classmethod
  def from_json(cls, data):
    if not data:
      raise ValueError("edit.sortMembers result" + " has no data")

    edit = SourceFileEdit.from_json(data["edit"])

    return cls(edit)

  def to_json(self):
    result = {}
    result["edit"] = self.edit.to_json()
    return result

  def to_response(self, id):
    assert id is not None, "must provide an id for the response"
    return Response(id, result=self)

  def __str__(self):
    return json.dumps(self.to_json())



# execution.createContext params
#
# {
#   "contextRoot": FilePath
# }
class ExecutionCreateContextParams(object):
  def __init__(self, contextRoot):
    # The path of the Dart or HTML file that will be launched, or the path of
    # the directory containing the file.
    self.contextRoot = contextRoot

  @classmethod
  def from_json(cls, data):
    if not data:
      raise ValueError("execution.createContext params" + " has no data")

    contextRoot = data["contextRoot"]

    return cls(contextRoot)

  def to_json(self):
    result = {}
    result["contextRoot"] = self.contextRoot
    return result

  def to_request(self, id):
    assert id is not None, "must provide an id for the request"
    return Request(id, "execution.createContext", self)

  def __str__(self):
    return json.dumps(self.to_json())



# execution.createContext result
#
# {
#   "id": ExecutionContextId
# }
class ExecutionCreateContextResult(object):
  def __init__(self, id):
    # The identifier used to refer to the execution context that was created.
    self.id = id

  @classmethod
  def from_json(cls, data):
    if not data:
      raise ValueError("execution.createContext result" + " has no data")

    id = data["id"]

    return cls(id)

  def to_json(self):
    result = {}
    result["id"] = self.id
    return result

  def to_response(self, id):
    assert id is not None, "must provide an id for the response"
    return Response(id, result=self)

  def __str__(self):
    return json.dumps(self.to_json())



# execution.deleteContext params
#
# {
#   "id": ExecutionContextId
# }
class ExecutionDeleteContextParams(object):
  def __init__(self, id):
    # The identifier of the execution context that is to be deleted.
    self.id = id

  @classmethod
  def from_json(cls, data):
    if not data:
      raise ValueError("execution.deleteContext params" + " has no data")

    id = data["id"]

    return cls(id)

  def to_json(self):
    result = {}
    result["id"] = self.id
    return result

  def to_request(self, id):
    assert id is not None, "must provide an id for the request"
    return Request(id, "execution.deleteContext", self)

  def __str__(self):
    return json.dumps(self.to_json())


# execution.deleteContext result
class ExecutionDeleteContextResult(object):
  def to_response(self, id):
    assert id is not None, "must provide an id for the response"
    return Response(id, result=None)



# execution.mapUri params
#
# {
#   "id": ExecutionContextId
#   "file": optional FilePath
#   "uri": optional String
# }
class ExecutionMapUriParams(object):
  def __init__(self, id, file='', uri=''):
    # The identifier of the execution context in which the URI is to be mapped.
    self.id = id
    # The path of the file to be mapped into a URI.
    self.file = file
    # The URI to be mapped into a file path.
    self.uri = uri

  @classmethod
  def from_json(cls, data):
    if not data:
      raise ValueError("execution.mapUri params" + " has no data")

    id = data["id"]
    file = data.get("file", '')
    if file:
      file = file
    uri = data.get("uri", '')
    if uri:
      uri = uri

    return cls(id, file=file, uri=uri)

  def to_json(self):
    result = {}
    result["id"] = self.id
    if self.file:
      result["file"] = self.file
    if self.uri:
      result["uri"] = self.uri
    return result

  def to_request(self, id):
    assert id is not None, "must provide an id for the request"
    return Request(id, "execution.mapUri", self)

  def __str__(self):
    return json.dumps(self.to_json())



# execution.mapUri result
#
# {
#   "file": optional FilePath
#   "uri": optional String
# }
class ExecutionMapUriResult(object):
  def __init__(self, file='', uri=''):
    # The file to which the URI was mapped. This field is omitted if the uri
    # field was not given in the request.
    self.file = file
    # The URI to which the file path was mapped. This field is omitted if the
    # file field was not given in the request.
    self.uri = uri

  @classmethod
  def from_json(cls, data):
    if not data:
      raise ValueError("execution.mapUri result" + " has no data")

    file = data.get("file", '')
    if file:
      file = file
    uri = data.get("uri", '')
    if uri:
      uri = uri

    return cls(file=file, uri=uri)

  def to_json(self):
    result = {}
    if self.file:
      result["file"] = self.file
    if self.uri:
      result["uri"] = self.uri
    return result

  def to_response(self, id):
    assert id is not None, "must provide an id for the response"
    return Response(id, result=self)

  def __str__(self):
    return json.dumps(self.to_json())



# execution.setSubscriptions params
#
# {
#   "subscriptions": List<ExecutionService>
# }
class ExecutionSetSubscriptionsParams(object):
  def __init__(self, subscriptions):
    # A list of the services being subscribed to.
    self.subscriptions = subscriptions

  @classmethod
  def from_json(cls, data):
    if not data:
      raise ValueError("execution.setSubscriptions params" + " has no data")

    subscriptions = data["subscriptions"]

    return cls(subscriptions)

  def to_json(self):
    result = {}
    result["subscriptions"] = self.subscriptions
    return result

  def to_request(self, id):
    assert id is not None, "must provide an id for the request"
    return Request(id, "execution.setSubscriptions", self)

  def __str__(self):
    return json.dumps(self.to_json())


# execution.setSubscriptions result
class ExecutionSetSubscriptionsResult(object):
  def to_response(self, id):
    assert id is not None, "must provide an id for the response"
    return Response(id, result=None)



# execution.launchData params
#
# {
#   "file": FilePath
#   "kind": optional ExecutableKind
#   "referencedFiles": optional List<FilePath>
# }
class ExecutionLaunchDataParams(object):
  def __init__(self, file, kind='', referencedFiles=[]):
    # The file for which launch data is being provided. This will either be a
    # Dart library or an HTML file.
    self.file = file
    # The kind of the executable file. This field is omitted if the file is not
    # a Dart file.
    self.kind = kind
    # A list of the Dart files that are referenced by the file. This field is
    # omitted if the file is not an HTML file.
    self.referencedFiles = referencedFiles

  @classmethod
  def from_json(cls, data):
    if not data:
      raise ValueError("execution.launchData params" + " has no data")

    file = data["file"]
    kind = data.get("kind", '')
    if kind:
      kind = kind
    referencedFiles = data.get("referencedFiles", [])
    if referencedFiles:
      referencedFiles = referencedFiles

    return cls(file, kind=kind, referencedFiles=referencedFiles)

  def to_json(self):
    result = {}
    result["file"] = self.file
    if self.kind:
      result["kind"] = self.kind
    if self.referencedFiles:
      result["referencedFiles"] = self.referencedFiles
    return result

  def to_notification(self):
    return Notification("execution.launchData", self);

  def __str__(self):
    return json.dumps(self.to_json())



# AddContentOverlay
#
# {
#   "type": "add"
#   "content": String
# }
class AddContentOverlay(object):
  def __init__(self, content):
    # The new content of the file.
    self.content = content

  @classmethod
  def from_json(cls, data):
    if not data:
      raise ValueError("AddContentOverlay" + " has no data")

    if data["type"] != "add":
      raise ValueError('expected "add" value')
    content = data["content"]

    return cls(content)

  def to_json(self):
    result = {}
    result["type"] = "add"
    result["content"] = self.content
    return result

  def __str__(self):
    return json.dumps(self.to_json())



# AnalysisError
#
# {
#   "severity": AnalysisErrorSeverity
#   "type": AnalysisErrorType
#   "location": Location
#   "message": String
#   "correction": optional String
# }
class AnalysisError(object):
  def __init__(self, severity, type, location, message, correction=''):
    # The severity of the error.
    self.severity = severity
    # The type of the error.
    self.type = type
    # The location associated with the error.
    self.location = location
    # The message to be displayed for this error. The message should indicate
    # what is wrong with the code and why it is wrong.
    self.message = message
    # The correction message to be displayed for this error. The correction
    # message should indicate how the user can fix the error. The field is
    # omitted if there is no correction message associated with the error code.
    self.correction = correction

  @classmethod
  def from_json(cls, data):
    if not data:
      raise ValueError("AnalysisError" + " has no data")

    severity = data["severity"]
    type = data["type"]
    location = Location.from_json(data["location"])
    message = data["message"]
    correction = data.get("correction", '')
    if correction:
      correction = correction

    return cls(severity, type, location, message, correction=correction)

  def to_json(self):
    result = {}
    result["severity"] = self.severity
    result["type"] = self.type
    result["location"] = self.location.to_json()
    result["message"] = self.message
    if self.correction:
      result["correction"] = self.correction
    return result

  def __str__(self):
    return json.dumps(self.to_json())



# AnalysisErrorFixes
#
# {
#   "error": AnalysisError
#   "fixes": List<SourceChange>
# }
class AnalysisErrorFixes(object):
  def __init__(self, error, fixes=[]):
    # The error with which the fixes are associated.
    self.error = error
    # The fixes associated with the error.
    self.fixes = fixes
    self.fixes = self.fixes if self.fixes else []



  @classmethod
  def from_json(cls, data):
    if not data:
      raise ValueError("AnalysisErrorFixes" + " has no data")

    error = AnalysisError.from_json(data["error"])
    fixes = [SourceChange.from_json(x) for x in data["fixes"]]

    return cls(error, fixes=fixes)

  def to_json(self):
    result = {}
    result["error"] = self.error.to_json()
    result["fixes"] = [x.to_json() for x in self.fixes]
    return result

  def __str__(self):
    return json.dumps(self.to_json())



# AnalysisErrorSeverity
#
# enum {
#   INFO
#   WARNING
#   ERROR
# }
class AnalysisErrorSeverity:
  INFO = "INFO"
  WARNING = "WARNING"
  ERROR = "ERROR"

  # A list containing all of the enum values that are defined.
  VALUES = ['INFO', 'WARNING', 'ERROR']


# AnalysisErrorType
#
# enum {
#   CHECKED_MODE_COMPILE_TIME_ERROR
#   COMPILE_TIME_ERROR
#   HINT
#   LINT
#   STATIC_TYPE_WARNING
#   STATIC_WARNING
#   SYNTACTIC_ERROR
#   TODO
# }
class AnalysisErrorType:
  CHECKED_MODE_COMPILE_TIME_ERROR = "CHECKED_MODE_COMPILE_TIME_ERROR"
  COMPILE_TIME_ERROR = "COMPILE_TIME_ERROR"
  HINT = "HINT"
  LINT = "LINT"
  STATIC_TYPE_WARNING = "STATIC_TYPE_WARNING"
  STATIC_WARNING = "STATIC_WARNING"
  SYNTACTIC_ERROR = "SYNTACTIC_ERROR"
  TODO = "TODO"

  # A list containing all of the enum values that are defined.
  VALUES = ['CHECKED_MODE_COMPILE_TIME_ERROR', 'COMPILE_TIME_ERROR', 'HINT', 'LINT', 'STATIC_TYPE_WARNING', 'STATIC_WARNING', 'SYNTACTIC_ERROR', 'TODO']


# AnalysisOptions
#
# {
#   "enableAsync": optional bool
#   "enableDeferredLoading": optional bool
#   "enableEnums": optional bool
#   "enableNullAwareOperators": optional bool
#   "generateDart2jsHints": optional bool
#   "generateHints": optional bool
#   "generateLints": optional bool
# }
class AnalysisOptions(object):
  def __init__(self, enableAsync=False, enableDeferredLoading=False, enableEnums=False, enableNullAwareOperators=False, generateDart2jsHints=False, generateHints=False, generateLints=False):
    # Deprecated
    #
    # True if the client wants to enable support for the proposed async
    # feature.
    self.enableAsync = enableAsync
    # Deprecated
    #
    # True if the client wants to enable support for the proposed deferred
    # loading feature.
    self.enableDeferredLoading = enableDeferredLoading
    # Deprecated
    #
    # True if the client wants to enable support for the proposed enum feature.
    self.enableEnums = enableEnums
    # True if the client wants to enable support for the proposed "null aware
    # operators" feature.
    self.enableNullAwareOperators = enableNullAwareOperators
    # True if hints that are specific to dart2js should be generated. This
    # option is ignored if generateHints is false.
    self.generateDart2jsHints = generateDart2jsHints
    # True if hints should be generated as part of generating errors and
    # warnings.
    self.generateHints = generateHints
    # True if lints should be generated as part of generating errors and
    # warnings.
    self.generateLints = generateLints

  @classmethod
  def from_json(cls, data):
    if not data:
      raise ValueError("AnalysisOptions" + " has no data")

    enableAsync = data.get("enableAsync", False)
    if enableAsync:
      enableAsync = enableAsync
    enableDeferredLoading = data.get("enableDeferredLoading", False)
    if enableDeferredLoading:
      enableDeferredLoading = enableDeferredLoading
    enableEnums = data.get("enableEnums", False)
    if enableEnums:
      enableEnums = enableEnums
    enableNullAwareOperators = data.get("enableNullAwareOperators", False)
    if enableNullAwareOperators:
      enableNullAwareOperators = enableNullAwareOperators
    generateDart2jsHints = data.get("generateDart2jsHints", False)
    if generateDart2jsHints:
      generateDart2jsHints = generateDart2jsHints
    generateHints = data.get("generateHints", False)
    if generateHints:
      generateHints = generateHints
    generateLints = data.get("generateLints", False)
    if generateLints:
      generateLints = generateLints

    return cls(enableAsync=enableAsync, enableDeferredLoading=enableDeferredLoading, enableEnums=enableEnums, enableNullAwareOperators=enableNullAwareOperators, generateDart2jsHints=generateDart2jsHints, generateHints=generateHints, generateLints=generateLints)

  def to_json(self):
    result = {}
    if self.enableAsync:
      result["enableAsync"] = self.enableAsync
    if self.enableDeferredLoading:
      result["enableDeferredLoading"] = self.enableDeferredLoading
    if self.enableEnums:
      result["enableEnums"] = self.enableEnums
    if self.enableNullAwareOperators:
      result["enableNullAwareOperators"] = self.enableNullAwareOperators
    if self.generateDart2jsHints:
      result["generateDart2jsHints"] = self.generateDart2jsHints
    if self.generateHints:
      result["generateHints"] = self.generateHints
    if self.generateLints:
      result["generateLints"] = self.generateLints
    return result

  def __str__(self):
    return json.dumps(self.to_json())



# AnalysisService
#
# enum {
#   FOLDING
#   HIGHLIGHTS
#   INVALIDATE
#   NAVIGATION
#   OCCURRENCES
#   OUTLINE
#   OVERRIDES
# }
class AnalysisService:
  FOLDING = "FOLDING"
  HIGHLIGHTS = "HIGHLIGHTS"
  INVALIDATE = "INVALIDATE"
  NAVIGATION = "NAVIGATION"
  OCCURRENCES = "OCCURRENCES"
  OUTLINE = "OUTLINE"
  OVERRIDES = "OVERRIDES"

  # A list containing all of the enum values that are defined.
  VALUES = ['FOLDING', 'HIGHLIGHTS', 'INVALIDATE', 'NAVIGATION', 'OCCURRENCES', 'OUTLINE', 'OVERRIDES']


# AnalysisStatus
#
# {
#   "isAnalyzing": bool
#   "analysisTarget": optional String
# }
class AnalysisStatus(object):
  def __init__(self, isAnalyzing, analysisTarget=''):
    # True if analysis is currently being performed.
    self.isAnalyzing = isAnalyzing
    # The name of the current target of analysis. This field is omitted if
    # analyzing is false.
    self.analysisTarget = analysisTarget

  @classmethod
  def from_json(cls, data):
    if not data:
      raise ValueError("AnalysisStatus" + " has no data")

    isAnalyzing = data["isAnalyzing"]
    analysisTarget = data.get("analysisTarget", '')
    if analysisTarget:
      analysisTarget = analysisTarget

    return cls(isAnalyzing, analysisTarget=analysisTarget)

  def to_json(self):
    result = {}
    result["isAnalyzing"] = self.isAnalyzing
    if self.analysisTarget:
      result["analysisTarget"] = self.analysisTarget
    return result

  def __str__(self):
    return json.dumps(self.to_json())



# ChangeContentOverlay
#
# {
#   "type": "change"
#   "edits": List<SourceEdit>
# }
class ChangeContentOverlay(object):
  def __init__(self, edits):
    # The edits to be applied to the file.
    self.edits = edits

  @classmethod
  def from_json(cls, data):
    if not data:
      raise ValueError("ChangeContentOverlay" + " has no data")

    if data["type"] != "change":
      raise ValueError('expected "change" value')
    edits = [SourceEdit.from_json(x) for x in data["edits"]]

    return cls(edits)

  def to_json(self):
    result = {}
    result["type"] = "change"
    result["edits"] = [x.to_json() for x in self.edits]
    return result

  def __str__(self):
    return json.dumps(self.to_json())



# CompletionSuggestion
#
# {
#   "kind": CompletionSuggestionKind
#   "relevance": int
#   "completion": String
#   "selectionOffset": int
#   "selectionLength": int
#   "isDeprecated": bool
#   "isPotential": bool
#   "docSummary": optional String
#   "docComplete": optional String
#   "declaringType": optional String
#   "element": optional Element
#   "returnType": optional String
#   "parameterNames": optional List<String>
#   "parameterTypes": optional List<String>
#   "requiredParameterCount": optional int
#   "hasNamedParameters": optional bool
#   "parameterName": optional String
#   "parameterType": optional String
#   "importUri": optional String
# }
class CompletionSuggestion(object):
  def __init__(self, kind, relevance, completion, selectionOffset, selectionLength, isDeprecated, isPotential, docSummary='', docComplete='', declaringType='', element=None, returnType='', parameterNames=[], parameterTypes=[], requiredParameterCount=0, hasNamedParameters=False, parameterName='', parameterType='', importUri=''):
    # The kind of element being suggested.
    self.kind = kind
    # The relevance of this completion suggestion where a higher number
    # indicates a higher relevance.
    self.relevance = relevance
    # The identifier to be inserted if the suggestion is selected. If the
    # suggestion is for a method or function, the client might want to
    # additionally insert a template for the parameters. The information
    # required in order to do so is contained in other fields.
    self.completion = completion
    # The offset, relative to the beginning of the completion, of where the
    # selection should be placed after insertion.
    self.selectionOffset = selectionOffset
    # The number of characters that should be selected after insertion.
    self.selectionLength = selectionLength
    # True if the suggested element is deprecated.
    self.isDeprecated = isDeprecated
    # True if the element is not known to be valid for the target. This happens
    # if the type of the target is dynamic.
    self.isPotential = isPotential
    # An abbreviated version of the Dartdoc associated with the element being
    # suggested, This field is omitted if there is no Dartdoc associated with
    # the element.
    self.docSummary = docSummary
    # The Dartdoc associated with the element being suggested, This field is
    # omitted if there is no Dartdoc associated with the element.
    self.docComplete = docComplete
    # The class that declares the element being suggested. This field is
    # omitted if the suggested element is not a member of a class.
    self.declaringType = declaringType
    # Information about the element reference being suggested.
    self.element = element
    # The return type of the getter, function or method or the type of the
    # field being suggested. This field is omitted if the suggested element is
    # not a getter, function or method.
    self.returnType = returnType
    # The names of the parameters of the function or method being suggested.
    # This field is omitted if the suggested element is not a setter, function
    # or method.
    self.parameterNames = parameterNames
    # The types of the parameters of the function or method being suggested.
    # This field is omitted if the parameterNames field is omitted.
    self.parameterTypes = parameterTypes
    # The number of required parameters for the function or method being
    # suggested. This field is omitted if the parameterNames field is omitted.
    self.requiredParameterCount = requiredParameterCount
    # True if the function or method being suggested has at least one named
    # parameter. This field is omitted if the parameterNames field is omitted.
    self.hasNamedParameters = hasNamedParameters
    # The name of the optional parameter being suggested. This field is omitted
    # if the suggestion is not the addition of an optional argument within an
    # argument list.
    self.parameterName = parameterName
    # The type of the options parameter being suggested. This field is omitted
    # if the parameterName field is omitted.
    self.parameterType = parameterType
    # The import to be added if the suggestion is out of scope and needs an
    # import to be added to be in scope.
    self.importUri = importUri

  @classmethod
  def from_json(cls, data):
    if not data:
      raise ValueError("CompletionSuggestion" + " has no data")

    kind = data["kind"]
    relevance = data["relevance"]
    completion = data["completion"]
    selectionOffset = data["selectionOffset"]
    selectionLength = data["selectionLength"]
    isDeprecated = data["isDeprecated"]
    isPotential = data["isPotential"]
    docSummary = data.get("docSummary", '')
    if docSummary:
      docSummary = docSummary
    docComplete = data.get("docComplete", '')
    if docComplete:
      docComplete = docComplete
    declaringType = data.get("declaringType", '')
    if declaringType:
      declaringType = declaringType
    element = data.get("element", None)
    if element:
      element = Element.from_json(element)
    returnType = data.get("returnType", '')
    if returnType:
      returnType = returnType
    parameterNames = data.get("parameterNames", [])
    if parameterNames:
      parameterNames = parameterNames
    parameterTypes = data.get("parameterTypes", [])
    if parameterTypes:
      parameterTypes = parameterTypes
    requiredParameterCount = data.get("requiredParameterCount", 0)
    if requiredParameterCount:
      requiredParameterCount = requiredParameterCount
    hasNamedParameters = data.get("hasNamedParameters", False)
    if hasNamedParameters:
      hasNamedParameters = hasNamedParameters
    parameterName = data.get("parameterName", '')
    if parameterName:
      parameterName = parameterName
    parameterType = data.get("parameterType", '')
    if parameterType:
      parameterType = parameterType
    importUri = data.get("importUri", '')
    if importUri:
      importUri = importUri

    return cls(kind, relevance, completion, selectionOffset, selectionLength, isDeprecated, isPotential, docSummary=docSummary, docComplete=docComplete, declaringType=declaringType, element=element, returnType=returnType, parameterNames=parameterNames, parameterTypes=parameterTypes, requiredParameterCount=requiredParameterCount, hasNamedParameters=hasNamedParameters, parameterName=parameterName, parameterType=parameterType, importUri=importUri)

  def to_json(self):
    result = {}
    result["kind"] = self.kind
    result["relevance"] = self.relevance
    result["completion"] = self.completion
    result["selectionOffset"] = self.selectionOffset
    result["selectionLength"] = self.selectionLength
    result["isDeprecated"] = self.isDeprecated
    result["isPotential"] = self.isPotential
    if self.docSummary:
      result["docSummary"] = self.docSummary
    if self.docComplete:
      result["docComplete"] = self.docComplete
    if self.declaringType:
      result["declaringType"] = self.declaringType
    if self.element:
      result["element"] = self.element.to_json()
    if self.returnType:
      result["returnType"] = self.returnType
    if self.parameterNames:
      result["parameterNames"] = self.parameterNames
    if self.parameterTypes:
      result["parameterTypes"] = self.parameterTypes
    if self.requiredParameterCount:
      result["requiredParameterCount"] = self.requiredParameterCount
    if self.hasNamedParameters:
      result["hasNamedParameters"] = self.hasNamedParameters
    if self.parameterName:
      result["parameterName"] = self.parameterName
    if self.parameterType:
      result["parameterType"] = self.parameterType
    if self.importUri:
      result["importUri"] = self.importUri
    return result

  def __str__(self):
    return json.dumps(self.to_json())



# CompletionSuggestionKind
#
# enum {
#   ARGUMENT_LIST
#   IMPORT
#   IDENTIFIER
#   INVOCATION
#   KEYWORD
#   NAMED_ARGUMENT
#   OPTIONAL_ARGUMENT
#   PARAMETER
# }
class CompletionSuggestionKind:
  # A list of arguments for the method or function that is being invoked. For
  # this suggestion kind, the completion field is a textual representation of
  # the invocation and the parameterNames, parameterTypes, and
  # requiredParameterCount attributes are defined.
  ARGUMENT_LIST = "ARGUMENT_LIST"
  IMPORT = "IMPORT"
  # The element identifier should be inserted at the completion location. For
  # example "someMethod" in import 'myLib.dart' show someMethod; . For
  # suggestions of this kind, the element attribute is defined and the
  # completion field is the element's identifier.
  IDENTIFIER = "IDENTIFIER"
  # The element is being invoked at the completion location. For example,
  # "someMethod" in x.someMethod(); . For suggestions of this kind, the element
  # attribute is defined and the completion field is the element's identifier.
  INVOCATION = "INVOCATION"
  # A keyword is being suggested. For suggestions of this kind, the completion
  # is the keyword.
  KEYWORD = "KEYWORD"
  # A named argument for the current callsite is being suggested. For
  # suggestions of this kind, the completion is the named argument identifier
  # including a trailing ':' and space.
  NAMED_ARGUMENT = "NAMED_ARGUMENT"
  OPTIONAL_ARGUMENT = "OPTIONAL_ARGUMENT"
  PARAMETER = "PARAMETER"

  # A list containing all of the enum values that are defined.
  VALUES = ['ARGUMENT_LIST', 'IMPORT', 'IDENTIFIER', 'INVOCATION', 'KEYWORD', 'NAMED_ARGUMENT', 'OPTIONAL_ARGUMENT', 'PARAMETER']


# Element
#
# {
#   "kind": ElementKind
#   "name": String
#   "location": optional Location
#   "flags": int
#   "parameters": optional String
#   "returnType": optional String
#   "typeParameters": optional String
# }
class Element(object):
  FLAG_ABSTRACT = 0x01
  FLAG_CONST = 0x02
  FLAG_FINAL = 0x04
  FLAG_STATIC = 0x08
  FLAG_PRIVATE = 0x10
  FLAG_DEPRECATED = 0x20

  def __init__(self, kind, name, flags, location=None, parameters='', returnType='', typeParameters=''):
    # The kind of the element.
    self.kind = kind
    # The name of the element. This is typically used as the label in the
    # outline.
    self.name = name
    # The location of the name in the declaration of the element.
    self.location = location
    # A bit-map containing the following flags:
    #
    # - 0x01 - set if the element is explicitly or implicitly abstract
    # - 0x02 - set if the element was declared to be ‘const’
    # - 0x04 - set if the element was declared to be ‘final’
    # - 0x08 - set if the element is a static member of a class or is a
    #   top-level function or field
    # - 0x10 - set if the element is private
    # - 0x20 - set if the element is deprecated
    self.flags = flags
    # The parameter list for the element. If the element is not a method or
    # function this field will not be defined. If the element doesn't have
    # parameters (e.g. getter), this field will not be defined. If the element
    # has zero parameters, this field will have a value of "()".
    self.parameters = parameters
    # The return type of the element. If the element is not a method or
    # function this field will not be defined. If the element does not have a
    # declared return type, this field will contain an empty string.
    self.returnType = returnType
    # The type parameter list for the element. If the element doesn't have type
    # parameters, this field will not be defined.
    self.typeParameters = typeParameters

  @classmethod
  def from_json(cls, data):
    if not data:
      raise ValueError("Element" + " has no data")

    kind = data["kind"]
    name = data["name"]
    location = data.get("location", None)
    if location:
      location = Location.from_json(location)
    flags = data["flags"]
    parameters = data.get("parameters", '')
    if parameters:
      parameters = parameters
    returnType = data.get("returnType", '')
    if returnType:
      returnType = returnType
    typeParameters = data.get("typeParameters", '')
    if typeParameters:
      typeParameters = typeParameters

    return cls(kind, name, flags, location=location, parameters=parameters, returnType=returnType, typeParameters=typeParameters)

  def to_json(self):
    result = {}
    result["kind"] = self.kind
    result["name"] = self.name
    if self.location:
      result["location"] = self.location.to_json()
    result["flags"] = self.flags
    if self.parameters:
      result["parameters"] = self.parameters
    if self.returnType:
      result["returnType"] = self.returnType
    if self.typeParameters:
      result["typeParameters"] = self.typeParameters
    return result

  def __str__(self):
    return json.dumps(self.to_json())



# ElementKind
#
# enum {
#   CLASS
#   CLASS_TYPE_ALIAS
#   COMPILATION_UNIT
#   CONSTRUCTOR
#   ENUM
#   ENUM_CONSTANT
#   FIELD
#   FUNCTION
#   FUNCTION_TYPE_ALIAS
#   GETTER
#   LABEL
#   LIBRARY
#   LOCAL_VARIABLE
#   METHOD
#   PARAMETER
#   PREFIX
#   SETTER
#   TOP_LEVEL_VARIABLE
#   TYPE_PARAMETER
#   UNIT_TEST_GROUP
#   UNIT_TEST_TEST
#   UNKNOWN
# }
class ElementKind:
  CLASS = "CLASS"
  CLASS_TYPE_ALIAS = "CLASS_TYPE_ALIAS"
  COMPILATION_UNIT = "COMPILATION_UNIT"
  CONSTRUCTOR = "CONSTRUCTOR"
  ENUM = "ENUM"
  ENUM_CONSTANT = "ENUM_CONSTANT"
  FIELD = "FIELD"
  FUNCTION = "FUNCTION"
  FUNCTION_TYPE_ALIAS = "FUNCTION_TYPE_ALIAS"
  GETTER = "GETTER"
  LABEL = "LABEL"
  LIBRARY = "LIBRARY"
  LOCAL_VARIABLE = "LOCAL_VARIABLE"
  METHOD = "METHOD"
  PARAMETER = "PARAMETER"
  PREFIX = "PREFIX"
  SETTER = "SETTER"
  TOP_LEVEL_VARIABLE = "TOP_LEVEL_VARIABLE"
  TYPE_PARAMETER = "TYPE_PARAMETER"
  UNIT_TEST_GROUP = "UNIT_TEST_GROUP"
  UNIT_TEST_TEST = "UNIT_TEST_TEST"
  UNKNOWN = "UNKNOWN"

  # A list containing all of the enum values that are defined.
  VALUES = ['CLASS', 'CLASS_TYPE_ALIAS', 'COMPILATION_UNIT', 'CONSTRUCTOR', 'ENUM', 'ENUM_CONSTANT', 'FIELD', 'FUNCTION', 'FUNCTION_TYPE_ALIAS', 'GETTER', 'LABEL', 'LIBRARY', 'LOCAL_VARIABLE', 'METHOD', 'PARAMETER', 'PREFIX', 'SETTER', 'TOP_LEVEL_VARIABLE', 'TYPE_PARAMETER', 'UNIT_TEST_GROUP', 'UNIT_TEST_TEST', 'UNKNOWN']


# ExecutableFile
#
# {
#   "file": FilePath
#   "kind": ExecutableKind
# }
class ExecutableFile(object):
  def __init__(self, file, kind):
    # The path of the executable file.
    self.file = file
    # The kind of the executable file.
    self.kind = kind

  @classmethod
  def from_json(cls, data):
    if not data:
      raise ValueError("ExecutableFile" + " has no data")

    file = data["file"]
    kind = data["kind"]

    return cls(file, kind)

  def to_json(self):
    result = {}
    result["file"] = self.file
    result["kind"] = self.kind
    return result

  def __str__(self):
    return json.dumps(self.to_json())



# ExecutableKind
#
# enum {
#   CLIENT
#   EITHER
#   NOT_EXECUTABLE
#   SERVER
# }
class ExecutableKind:
  CLIENT = "CLIENT"
  EITHER = "EITHER"
  NOT_EXECUTABLE = "NOT_EXECUTABLE"
  SERVER = "SERVER"

  # A list containing all of the enum values that are defined.
  VALUES = ['CLIENT', 'EITHER', 'NOT_EXECUTABLE', 'SERVER']


# ExecutionService
#
# enum {
#   LAUNCH_DATA
# }
class ExecutionService:
  LAUNCH_DATA = "LAUNCH_DATA"

  # A list containing all of the enum values that are defined.
  VALUES = ['LAUNCH_DATA']


# FoldingKind
#
# enum {
#   COMMENT
#   CLASS_MEMBER
#   DIRECTIVES
#   DOCUMENTATION_COMMENT
#   TOP_LEVEL_DECLARATION
# }
class FoldingKind:
  COMMENT = "COMMENT"
  CLASS_MEMBER = "CLASS_MEMBER"
  DIRECTIVES = "DIRECTIVES"
  DOCUMENTATION_COMMENT = "DOCUMENTATION_COMMENT"
  TOP_LEVEL_DECLARATION = "TOP_LEVEL_DECLARATION"

  # A list containing all of the enum values that are defined.
  VALUES = ['COMMENT', 'CLASS_MEMBER', 'DIRECTIVES', 'DOCUMENTATION_COMMENT', 'TOP_LEVEL_DECLARATION']


# FoldingRegion
#
# {
#   "kind": FoldingKind
#   "offset": int
#   "length": int
# }
class FoldingRegion(object):
  def __init__(self, kind, offset, length):
    # The kind of the region.
    self.kind = kind
    # The offset of the region to be folded.
    self.offset = offset
    # The length of the region to be folded.
    self.length = length

  @classmethod
  def from_json(cls, data):
    if not data:
      raise ValueError("FoldingRegion" + " has no data")

    kind = data["kind"]
    offset = data["offset"]
    length = data["length"]

    return cls(kind, offset, length)

  def to_json(self):
    result = {}
    result["kind"] = self.kind
    result["offset"] = self.offset
    result["length"] = self.length
    return result

  def __str__(self):
    return json.dumps(self.to_json())



# HighlightRegion
#
# {
#   "type": HighlightRegionType
#   "offset": int
#   "length": int
# }
class HighlightRegion(object):
  def __init__(self, type, offset, length):
    # The type of highlight associated with the region.
    self.type = type
    # The offset of the region to be highlighted.
    self.offset = offset
    # The length of the region to be highlighted.
    self.length = length

  @classmethod
  def from_json(cls, data):
    if not data:
      raise ValueError("HighlightRegion" + " has no data")

    type = data["type"]
    offset = data["offset"]
    length = data["length"]

    return cls(type, offset, length)

  def to_json(self):
    result = {}
    result["type"] = self.type
    result["offset"] = self.offset
    result["length"] = self.length
    return result

  def __str__(self):
    return json.dumps(self.to_json())



# HighlightRegionType
#
# enum {
#   ANNOTATION
#   BUILT_IN
#   CLASS
#   COMMENT_BLOCK
#   COMMENT_DOCUMENTATION
#   COMMENT_END_OF_LINE
#   CONSTRUCTOR
#   DIRECTIVE
#   DYNAMIC_TYPE
#   ENUM
#   ENUM_CONSTANT
#   FIELD
#   FIELD_STATIC
#   FUNCTION
#   FUNCTION_DECLARATION
#   FUNCTION_TYPE_ALIAS
#   GETTER_DECLARATION
#   IDENTIFIER_DEFAULT
#   IMPORT_PREFIX
#   KEYWORD
#   LABEL
#   LITERAL_BOOLEAN
#   LITERAL_DOUBLE
#   LITERAL_INTEGER
#   LITERAL_LIST
#   LITERAL_MAP
#   LITERAL_STRING
#   LOCAL_VARIABLE
#   LOCAL_VARIABLE_DECLARATION
#   METHOD
#   METHOD_DECLARATION
#   METHOD_DECLARATION_STATIC
#   METHOD_STATIC
#   PARAMETER
#   SETTER_DECLARATION
#   TOP_LEVEL_VARIABLE
#   TYPE_NAME_DYNAMIC
#   TYPE_PARAMETER
# }
class HighlightRegionType:
  ANNOTATION = "ANNOTATION"
  BUILT_IN = "BUILT_IN"
  CLASS = "CLASS"
  COMMENT_BLOCK = "COMMENT_BLOCK"
  COMMENT_DOCUMENTATION = "COMMENT_DOCUMENTATION"
  COMMENT_END_OF_LINE = "COMMENT_END_OF_LINE"
  CONSTRUCTOR = "CONSTRUCTOR"
  DIRECTIVE = "DIRECTIVE"
  DYNAMIC_TYPE = "DYNAMIC_TYPE"
  ENUM = "ENUM"
  ENUM_CONSTANT = "ENUM_CONSTANT"
  FIELD = "FIELD"
  FIELD_STATIC = "FIELD_STATIC"
  FUNCTION = "FUNCTION"
  FUNCTION_DECLARATION = "FUNCTION_DECLARATION"
  FUNCTION_TYPE_ALIAS = "FUNCTION_TYPE_ALIAS"
  GETTER_DECLARATION = "GETTER_DECLARATION"
  IDENTIFIER_DEFAULT = "IDENTIFIER_DEFAULT"
  IMPORT_PREFIX = "IMPORT_PREFIX"
  KEYWORD = "KEYWORD"
  LABEL = "LABEL"
  LITERAL_BOOLEAN = "LITERAL_BOOLEAN"
  LITERAL_DOUBLE = "LITERAL_DOUBLE"
  LITERAL_INTEGER = "LITERAL_INTEGER"
  LITERAL_LIST = "LITERAL_LIST"
  LITERAL_MAP = "LITERAL_MAP"
  LITERAL_STRING = "LITERAL_STRING"
  LOCAL_VARIABLE = "LOCAL_VARIABLE"
  LOCAL_VARIABLE_DECLARATION = "LOCAL_VARIABLE_DECLARATION"
  METHOD = "METHOD"
  METHOD_DECLARATION = "METHOD_DECLARATION"
  METHOD_DECLARATION_STATIC = "METHOD_DECLARATION_STATIC"
  METHOD_STATIC = "METHOD_STATIC"
  PARAMETER = "PARAMETER"
  SETTER_DECLARATION = "SETTER_DECLARATION"
  TOP_LEVEL_VARIABLE = "TOP_LEVEL_VARIABLE"
  TYPE_NAME_DYNAMIC = "TYPE_NAME_DYNAMIC"
  TYPE_PARAMETER = "TYPE_PARAMETER"

  # A list containing all of the enum values that are defined.
  VALUES = ['ANNOTATION', 'BUILT_IN', 'CLASS', 'COMMENT_BLOCK', 'COMMENT_DOCUMENTATION', 'COMMENT_END_OF_LINE', 'CONSTRUCTOR', 'DIRECTIVE', 'DYNAMIC_TYPE', 'ENUM', 'ENUM_CONSTANT', 'FIELD', 'FIELD_STATIC', 'FUNCTION', 'FUNCTION_DECLARATION', 'FUNCTION_TYPE_ALIAS', 'GETTER_DECLARATION', 'IDENTIFIER_DEFAULT', 'IMPORT_PREFIX', 'KEYWORD', 'LABEL', 'LITERAL_BOOLEAN', 'LITERAL_DOUBLE', 'LITERAL_INTEGER', 'LITERAL_LIST', 'LITERAL_MAP', 'LITERAL_STRING', 'LOCAL_VARIABLE', 'LOCAL_VARIABLE_DECLARATION', 'METHOD', 'METHOD_DECLARATION', 'METHOD_DECLARATION_STATIC', 'METHOD_STATIC', 'PARAMETER', 'SETTER_DECLARATION', 'TOP_LEVEL_VARIABLE', 'TYPE_NAME_DYNAMIC', 'TYPE_PARAMETER']


# HoverInformation
#
# {
#   "offset": int
#   "length": int
#   "containingLibraryPath": optional String
#   "containingLibraryName": optional String
#   "containingClassDescription": optional String
#   "dartdoc": optional String
#   "elementDescription": optional String
#   "elementKind": optional String
#   "parameter": optional String
#   "propagatedType": optional String
#   "staticType": optional String
# }
class HoverInformation(object):
  def __init__(self, offset, length, containingLibraryPath='', containingLibraryName='', containingClassDescription='', dartdoc='', elementDescription='', elementKind='', parameter='', propagatedType='', staticType=''):
    # The offset of the range of characters that encompases the cursor position
    # and has the same hover information as the cursor position.
    self.offset = offset
    # The length of the range of characters that encompases the cursor position
    # and has the same hover information as the cursor position.
    self.length = length
    # The path to the defining compilation unit of the library in which the
    # referenced element is declared. This data is omitted if there is no
    # referenced element, or if the element is declared inside an HTML file.
    self.containingLibraryPath = containingLibraryPath
    # The name of the library in which the referenced element is declared. This
    # data is omitted if there is no referenced element, or if the element is
    # declared inside an HTML file.
    self.containingLibraryName = containingLibraryName
    # A human-readable description of the class declaring the element being
    # referenced. This data is omitted if there is no referenced element, or if
    # the element is not a class member.
    self.containingClassDescription = containingClassDescription
    # The dartdoc associated with the referenced element. Other than the
    # removal of the comment delimiters, including leading asterisks in the
    # case of a block comment, the dartdoc is unprocessed markdown. This data
    # is omitted if there is no referenced element, or if the element has no
    # dartdoc.
    self.dartdoc = dartdoc
    # A human-readable description of the element being referenced. This data
    # is omitted if there is no referenced element.
    self.elementDescription = elementDescription
    # A human-readable description of the kind of element being referenced
    # (such as “class” or “function type alias”). This data is omitted if there
    # is no referenced element.
    self.elementKind = elementKind
    # A human-readable description of the parameter corresponding to the
    # expression being hovered over. This data is omitted if the location is
    # not in an argument to a function.
    self.parameter = parameter
    # The name of the propagated type of the expression. This data is omitted
    # if the location does not correspond to an expression or if there is no
    # propagated type information.
    self.propagatedType = propagatedType
    # The name of the static type of the expression. This data is omitted if
    # the location does not correspond to an expression.
    self.staticType = staticType

  @classmethod
  def from_json(cls, data):
    if not data:
      raise ValueError("HoverInformation" + " has no data")

    offset = data["offset"]
    length = data["length"]
    containingLibraryPath = data.get("containingLibraryPath", '')
    if containingLibraryPath:
      containingLibraryPath = containingLibraryPath
    containingLibraryName = data.get("containingLibraryName", '')
    if containingLibraryName:
      containingLibraryName = containingLibraryName
    containingClassDescription = data.get("containingClassDescription", '')
    if containingClassDescription:
      containingClassDescription = containingClassDescription
    dartdoc = data.get("dartdoc", '')
    if dartdoc:
      dartdoc = dartdoc
    elementDescription = data.get("elementDescription", '')
    if elementDescription:
      elementDescription = elementDescription
    elementKind = data.get("elementKind", '')
    if elementKind:
      elementKind = elementKind
    parameter = data.get("parameter", '')
    if parameter:
      parameter = parameter
    propagatedType = data.get("propagatedType", '')
    if propagatedType:
      propagatedType = propagatedType
    staticType = data.get("staticType", '')
    if staticType:
      staticType = staticType

    return cls(offset, length, containingLibraryPath=containingLibraryPath, containingLibraryName=containingLibraryName, containingClassDescription=containingClassDescription, dartdoc=dartdoc, elementDescription=elementDescription, elementKind=elementKind, parameter=parameter, propagatedType=propagatedType, staticType=staticType)

  def to_json(self):
    result = {}
    result["offset"] = self.offset
    result["length"] = self.length
    if self.containingLibraryPath:
      result["containingLibraryPath"] = self.containingLibraryPath
    if self.containingLibraryName:
      result["containingLibraryName"] = self.containingLibraryName
    if self.containingClassDescription:
      result["containingClassDescription"] = self.containingClassDescription
    if self.dartdoc:
      result["dartdoc"] = self.dartdoc
    if self.elementDescription:
      result["elementDescription"] = self.elementDescription
    if self.elementKind:
      result["elementKind"] = self.elementKind
    if self.parameter:
      result["parameter"] = self.parameter
    if self.propagatedType:
      result["propagatedType"] = self.propagatedType
    if self.staticType:
      result["staticType"] = self.staticType
    return result

  def __str__(self):
    return json.dumps(self.to_json())



# LinkedEditGroup
#
# {
#   "positions": List<Position>
#   "length": int
#   "suggestions": List<LinkedEditSuggestion>
# }
class LinkedEditGroup(object):
  def __init__(self, positions, length, suggestions):
    # The positions of the regions that should be edited simultaneously.
    self.positions = positions
    # The length of the regions that should be edited simultaneously.
    self.length = length
    # Pre-computed suggestions for what every region might want to be changed
    # to.
    self.suggestions = suggestions

  @classmethod
  def from_json(cls, data):
    if not data:
      raise ValueError("LinkedEditGroup" + " has no data")

    positions = [Position.from_json(x) for x in data["positions"]]
    length = data["length"]
    suggestions = [LinkedEditSuggestion.from_json(x) for x in data["suggestions"]]

    return cls(positions, length, suggestions)

  def to_json(self):
    result = {}
    result["positions"] = [x.to_json() for x in self.positions]
    result["length"] = self.length
    result["suggestions"] = [x.to_json() for x in self.suggestions]
    return result

  def __str__(self):
    return json.dumps(self.to_json())



# LinkedEditSuggestion
#
# {
#   "value": String
#   "kind": LinkedEditSuggestionKind
# }
class LinkedEditSuggestion(object):
  def __init__(self, value, kind):
    # The value that could be used to replace all of the linked edit regions.
    self.value = value
    # The kind of value being proposed.
    self.kind = kind

  @classmethod
  def from_json(cls, data):
    if not data:
      raise ValueError("LinkedEditSuggestion" + " has no data")

    value = data["value"]
    kind = data["kind"]

    return cls(value, kind)

  def to_json(self):
    result = {}
    result["value"] = self.value
    result["kind"] = self.kind
    return result

  def __str__(self):
    return json.dumps(self.to_json())



# LinkedEditSuggestionKind
#
# enum {
#   METHOD
#   PARAMETER
#   TYPE
#   VARIABLE
# }
class LinkedEditSuggestionKind:
  METHOD = "METHOD"
  PARAMETER = "PARAMETER"
  TYPE = "TYPE"
  VARIABLE = "VARIABLE"

  # A list containing all of the enum values that are defined.
  VALUES = ['METHOD', 'PARAMETER', 'TYPE', 'VARIABLE']


# Location
#
# {
#   "file": FilePath
#   "offset": int
#   "length": int
#   "startLine": int
#   "startColumn": int
# }
class Location(object):
  def __init__(self, file, offset, length, startLine, startColumn):
    # The file containing the range.
    self.file = file
    # The offset of the range.
    self.offset = offset
    # The length of the range.
    self.length = length
    # The one-based index of the line containing the first character of the
    # range.
    self.startLine = startLine
    # The one-based index of the column containing the first character of the
    # range.
    self.startColumn = startColumn

  @classmethod
  def from_json(cls, data):
    if not data:
      raise ValueError("Location" + " has no data")

    file = data["file"]
    offset = data["offset"]
    length = data["length"]
    startLine = data["startLine"]
    startColumn = data["startColumn"]

    return cls(file, offset, length, startLine, startColumn)

  def to_json(self):
    result = {}
    result["file"] = self.file
    result["offset"] = self.offset
    result["length"] = self.length
    result["startLine"] = self.startLine
    result["startColumn"] = self.startColumn
    return result

  def __str__(self):
    return json.dumps(self.to_json())



# NavigationRegion
#
# {
#   "offset": int
#   "length": int
#   "targets": List<int>
# }
class NavigationRegion(object):
  def __init__(self, offset, length, targets):
    # The offset of the region from which the user can navigate.
    self.offset = offset
    # The length of the region from which the user can navigate.
    self.length = length
    # The indexes of the targets (in the enclosing navigation response) to
    # which the given region is bound. By opening the target, clients can
    # implement one form of navigation.
    self.targets = targets

  @classmethod
  def from_json(cls, data):
    if not data:
      raise ValueError("NavigationRegion" + " has no data")

    offset = data["offset"]
    length = data["length"]
    targets = data["targets"]

    return cls(offset, length, targets)

  def to_json(self):
    result = {}
    result["offset"] = self.offset
    result["length"] = self.length
    result["targets"] = self.targets
    return result

  def __str__(self):
    return json.dumps(self.to_json())



# NavigationTarget
#
# {
#   "kind": ElementKind
#   "fileIndex": int
#   "offset": int
#   "length": int
#   "startLine": int
#   "startColumn": int
# }
class NavigationTarget(object):
  def __init__(self, kind, fileIndex, offset, length, startLine, startColumn):
    # The kind of the element.
    self.kind = kind
    # The index of the file (in the enclosing navigation response) to navigate
    # to.
    self.fileIndex = fileIndex
    # The offset of the region from which the user can navigate.
    self.offset = offset
    # The length of the region from which the user can navigate.
    self.length = length
    # The one-based index of the line containing the first character of the
    # region.
    self.startLine = startLine
    # The one-based index of the column containing the first character of the
    # region.
    self.startColumn = startColumn

  @classmethod
  def from_json(cls, data):
    if not data:
      raise ValueError("NavigationTarget" + " has no data")

    kind = data["kind"]
    fileIndex = data["fileIndex"]
    offset = data["offset"]
    length = data["length"]
    startLine = data["startLine"]
    startColumn = data["startColumn"]

    return cls(kind, fileIndex, offset, length, startLine, startColumn)

  def to_json(self):
    result = {}
    result["kind"] = self.kind
    result["fileIndex"] = self.fileIndex
    result["offset"] = self.offset
    result["length"] = self.length
    result["startLine"] = self.startLine
    result["startColumn"] = self.startColumn
    return result

  def __str__(self):
    return json.dumps(self.to_json())



# Occurrences
#
# {
#   "element": Element
#   "offsets": List<int>
#   "length": int
# }
class Occurrences(object):
  def __init__(self, element, offsets, length):
    # The element that was referenced.
    self.element = element
    # The offsets of the name of the referenced element within the file.
    self.offsets = offsets
    # The length of the name of the referenced element.
    self.length = length

  @classmethod
  def from_json(cls, data):
    if not data:
      raise ValueError("Occurrences" + " has no data")

    element = Element.from_json(data["element"])
    offsets = data["offsets"]
    length = data["length"]

    return cls(element, offsets, length)

  def to_json(self):
    result = {}
    result["element"] = self.element.to_json()
    result["offsets"] = self.offsets
    result["length"] = self.length
    return result

  def __str__(self):
    return json.dumps(self.to_json())



# Outline
#
# {
#   "element": Element
#   "offset": int
#   "length": int
#   "children": optional List<Outline>
# }
class Outline(object):
  def __init__(self, element, offset, length, children=[]):
    # A description of the element represented by this node.
    self.element = element
    # The offset of the first character of the element. This is different than
    # the offset in the Element, which if the offset of the name of the
    # element. It can be used, for example, to map locations in the file back
    # to an outline.
    self.offset = offset
    # The length of the element.
    self.length = length
    # The children of the node. The field will be omitted if the node has no
    # children.
    self.children = children

  @classmethod
  def from_json(cls, data):
    if not data:
      raise ValueError("Outline" + " has no data")

    element = Element.from_json(data["element"])
    offset = data["offset"]
    length = data["length"]
    children = data.get("children", [])
    if children:
      children = [Outline.from_json(x) for x in children]

    return cls(element, offset, length, children=children)

  def to_json(self):
    result = {}
    result["element"] = self.element.to_json()
    result["offset"] = self.offset
    result["length"] = self.length
    if self.children:
      result["children"] = [x.to_json() for x in self.children]
    return result

  def __str__(self):
    return json.dumps(self.to_json())



# Override
#
# {
#   "offset": int
#   "length": int
#   "superclassMember": optional OverriddenMember
#   "interfaceMembers": optional List<OverriddenMember>
# }
class Override(object):
  def __init__(self, offset, length, superclassMember=None, interfaceMembers=[]):
    # The offset of the name of the overriding member.
    self.offset = offset
    # The length of the name of the overriding member.
    self.length = length
    # The member inherited from a superclass that is overridden by the
    # overriding member. The field is omitted if there is no superclass member,
    # in which case there must be at least one interface member.
    self.superclassMember = superclassMember
    # The members inherited from interfaces that are overridden by the
    # overriding member. The field is omitted if there are no interface
    # members, in which case there must be a superclass member.
    self.interfaceMembers = interfaceMembers

  @classmethod
  def from_json(cls, data):
    if not data:
      raise ValueError("Override" + " has no data")

    offset = data["offset"]
    length = data["length"]
    superclassMember = data.get("superclassMember", None)
    if superclassMember:
      superclassMember = OverriddenMember.from_json(superclassMember)
    interfaceMembers = data.get("interfaceMembers", [])
    if interfaceMembers:
      interfaceMembers = [OverriddenMember.from_json(x) for x in interfaceMembers]

    return cls(offset, length, superclassMember=superclassMember, interfaceMembers=interfaceMembers)

  def to_json(self):
    result = {}
    result["offset"] = self.offset
    result["length"] = self.length
    if self.superclassMember:
      result["superclassMember"] = self.superclassMember.to_json()
    if self.interfaceMembers:
      result["interfaceMembers"] = [x.to_json() for x in self.interfaceMembers]
    return result

  def __str__(self):
    return json.dumps(self.to_json())



# OverriddenMember
#
# {
#   "element": Element
#   "className": String
# }
class OverriddenMember(object):
  def __init__(self, element, className):
    # The element that is being overridden.
    self.element = element
    # The name of the class in which the member is defined.
    self.className = className

  @classmethod
  def from_json(cls, data):
    if not data:
      raise ValueError("OverriddenMember" + " has no data")

    element = Element.from_json(data["element"])
    className = data["className"]

    return cls(element, className)

  def to_json(self):
    result = {}
    result["element"] = self.element.to_json()
    result["className"] = self.className
    return result

  def __str__(self):
    return json.dumps(self.to_json())



# Position
#
# {
#   "file": FilePath
#   "offset": int
# }
class Position(object):
  def __init__(self, file, offset):
    # The file containing the position.
    self.file = file
    # The offset of the position.
    self.offset = offset

  @classmethod
  def from_json(cls, data):
    if not data:
      raise ValueError("Position" + " has no data")

    file = data["file"]
    offset = data["offset"]

    return cls(file, offset)

  def to_json(self):
    result = {}
    result["file"] = self.file
    result["offset"] = self.offset
    return result

  def __str__(self):
    return json.dumps(self.to_json())



# PubStatus
#
# {
#   "isListingPackageDirs": bool
# }
class PubStatus(object):
  def __init__(self, isListingPackageDirs):
    # True if the server is currently running pub to produce a list of package
    # directories.
    self.isListingPackageDirs = isListingPackageDirs

  @classmethod
  def from_json(cls, data):
    if not data:
      raise ValueError("PubStatus" + " has no data")

    isListingPackageDirs = data["isListingPackageDirs"]

    return cls(isListingPackageDirs)

  def to_json(self):
    result = {}
    result["isListingPackageDirs"] = self.isListingPackageDirs
    return result

  def __str__(self):
    return json.dumps(self.to_json())



# RefactoringKind
#
# enum {
#   CONVERT_GETTER_TO_METHOD
#   CONVERT_METHOD_TO_GETTER
#   EXTRACT_LOCAL_VARIABLE
#   EXTRACT_METHOD
#   INLINE_LOCAL_VARIABLE
#   INLINE_METHOD
#   MOVE_FILE
#   RENAME
#   SORT_MEMBERS
# }
class RefactoringKind:
  CONVERT_GETTER_TO_METHOD = "CONVERT_GETTER_TO_METHOD"
  CONVERT_METHOD_TO_GETTER = "CONVERT_METHOD_TO_GETTER"
  EXTRACT_LOCAL_VARIABLE = "EXTRACT_LOCAL_VARIABLE"
  EXTRACT_METHOD = "EXTRACT_METHOD"
  INLINE_LOCAL_VARIABLE = "INLINE_LOCAL_VARIABLE"
  INLINE_METHOD = "INLINE_METHOD"
  MOVE_FILE = "MOVE_FILE"
  RENAME = "RENAME"
  SORT_MEMBERS = "SORT_MEMBERS"

  # A list containing all of the enum values that are defined.
  VALUES = ['CONVERT_GETTER_TO_METHOD', 'CONVERT_METHOD_TO_GETTER', 'EXTRACT_LOCAL_VARIABLE', 'EXTRACT_METHOD', 'INLINE_LOCAL_VARIABLE', 'INLINE_METHOD', 'MOVE_FILE', 'RENAME', 'SORT_MEMBERS']


# RefactoringMethodParameter
#
# {
#   "id": optional String
#   "kind": RefactoringMethodParameterKind
#   "type": String
#   "name": String
#   "parameters": optional String
# }
class RefactoringMethodParameter(object):
  def __init__(self, kind, type, name, id='', parameters=''):
    # The unique identifier of the parameter. Clients may omit this field for
    # the parameters they want to add.
    self.id = id
    # The kind of the parameter.
    self.kind = kind
    # The type that should be given to the parameter, or the return type of the
    # parameter's function type.
    self.type = type
    # The name that should be given to the parameter.
    self.name = name
    # The parameter list of the parameter's function type. If the parameter is
    # not of a function type, this field will not be defined. If the function
    # type has zero parameters, this field will have a value of "()".
    self.parameters = parameters

  @classmethod
  def from_json(cls, data):
    if not data:
      raise ValueError("RefactoringMethodParameter" + " has no data")

    id = data.get("id", '')
    if id:
      id = id
    kind = data["kind"]
    type = data["type"]
    name = data["name"]
    parameters = data.get("parameters", '')
    if parameters:
      parameters = parameters

    return cls(kind, type, name, id=id, parameters=parameters)

  def to_json(self):
    result = {}
    if self.id:
      result["id"] = self.id
    result["kind"] = self.kind
    result["type"] = self.type
    result["name"] = self.name
    if self.parameters:
      result["parameters"] = self.parameters
    return result

  def __str__(self):
    return json.dumps(self.to_json())



# RefactoringMethodParameterKind
#
# enum {
#   REQUIRED
#   POSITIONAL
#   NAMED
# }
class RefactoringMethodParameterKind:
  REQUIRED = "REQUIRED"
  POSITIONAL = "POSITIONAL"
  NAMED = "NAMED"

  # A list containing all of the enum values that are defined.
  VALUES = ['REQUIRED', 'POSITIONAL', 'NAMED']


# RefactoringProblem
#
# {
#   "severity": RefactoringProblemSeverity
#   "message": String
#   "location": optional Location
# }
class RefactoringProblem(object):
  def __init__(self, severity, message, location=None):
    # The severity of the problem being represented.
    self.severity = severity
    # A human-readable description of the problem being represented.
    self.message = message
    # The location of the problem being represented. This field is omitted
    # unless there is a specific location associated with the problem (such as
    # a location where an element being renamed will be shadowed).
    self.location = location

  @classmethod
  def from_json(cls, data):
    if not data:
      raise ValueError("RefactoringProblem" + " has no data")

    severity = data["severity"]
    message = data["message"]
    location = data.get("location", None)
    if location:
      location = Location.from_json(location)

    return cls(severity, message, location=location)

  def to_json(self):
    result = {}
    result["severity"] = self.severity
    result["message"] = self.message
    if self.location:
      result["location"] = self.location.to_json()
    return result

  def __str__(self):
    return json.dumps(self.to_json())



# RefactoringProblemSeverity
#
# enum {
#   INFO
#   WARNING
#   ERROR
#   FATAL
# }
class RefactoringProblemSeverity:
  INFO = "INFO"
  WARNING = "WARNING"
  ERROR = "ERROR"
  FATAL = "FATAL"

  # A list containing all of the enum values that are defined.
  VALUES = ['INFO', 'WARNING', 'ERROR', 'FATAL']

  # Returns the [RefactoringProblemSeverity] with the maximal severity.
  @staticmethod
  def max(a, b):
    values = {"INFO": 0, "WARNING": 1, "ERROR": 2, "FATAL": 3}
    a1 = values[a]
    b1 = values[b]
    found = max(a, b)
    return a if found == a1 else b


# RemoveContentOverlay
#
# {
#   "type": "remove"
# }
class RemoveContentOverlay(object):

  @classmethod
  def from_json(cls, data):
    if not data:
      raise ValueError("RemoveContentOverlay" + " has no data")

    if data["type"] != "remove":
      raise ValueError('expected "remove" value')

    return cls()

  def to_json(self):
    result = {}
    result["type"] = "remove"
    return result

  def __str__(self):
    return json.dumps(self.to_json())



# RequestError
#
# {
#   "code": RequestErrorCode
#   "message": String
#   "stackTrace": optional String
# }
class RequestError(object):
  def __init__(self, code, message, stackTrace=''):
    # A code that uniquely identifies the error that occurred.
    self.code = code
    # A short description of the error.
    self.message = message
    # The stack trace associated with processing the request, used for
    # debugging the server.
    self.stackTrace = stackTrace

  @classmethod
  def from_json(cls, data):
    if not data:
      raise ValueError("RequestError" + " has no data")

    code = data["code"]
    message = data["message"]
    stackTrace = data.get("stackTrace", '')
    if stackTrace:
      stackTrace = stackTrace

    return cls(code, message, stackTrace=stackTrace)

  def to_json(self):
    result = {}
    result["code"] = self.code
    result["message"] = self.message
    if self.stackTrace:
      result["stackTrace"] = self.stackTrace
    return result

  def __str__(self):
    return json.dumps(self.to_json())



# RequestErrorCode
#
# enum {
#   CONTENT_MODIFIED
#   FORMAT_INVALID_FILE
#   FORMAT_WITH_ERRORS
#   GET_ERRORS_INVALID_FILE
#   INVALID_ANALYSIS_ROOT
#   INVALID_EXECUTION_CONTEXT
#   INVALID_OVERLAY_CHANGE
#   INVALID_PARAMETER
#   INVALID_REQUEST
#   NO_INDEX_GENERATED
#   REFACTORING_REQUEST_CANCELLED
#   SERVER_ALREADY_STARTED
#   SERVER_ERROR
#   SORT_MEMBERS_INVALID_FILE
#   SORT_MEMBERS_PARSE_ERRORS
#   UNANALYZED_PRIORITY_FILES
#   UNKNOWN_REQUEST
#   UNKNOWN_SOURCE
#   UNSUPPORTED_FEATURE
# }
class RequestErrorCode:
  # An "analysis.getErrors" or "analysis.getNavigation" request could not be
  # satisfied because the content of the file changed before the requested
  # results could be computed.
  CONTENT_MODIFIED = "CONTENT_MODIFIED"
  # An "edit.format" request specified a FilePath which does not match a Dart
  # file in an analysis root.
  FORMAT_INVALID_FILE = "FORMAT_INVALID_FILE"
  # An "edit.format" request specified a file that contains syntax errors.
  FORMAT_WITH_ERRORS = "FORMAT_WITH_ERRORS"
  # An "analysis.getErrors" request specified a FilePath which does not match a
  # file currently subject to analysis.
  GET_ERRORS_INVALID_FILE = "GET_ERRORS_INVALID_FILE"
  # A path passed as an argument to a request (such as analysis.reanalyze) is
  # required to be an analysis root, but isn't.
  INVALID_ANALYSIS_ROOT = "INVALID_ANALYSIS_ROOT"
  # The context root used to create an execution context does not exist.
  INVALID_EXECUTION_CONTEXT = "INVALID_EXECUTION_CONTEXT"
  # An "analysis.updateContent" request contained a ChangeContentOverlay object
  # which can't be applied, due to an edit having an offset or length that is
  # out of range.
  INVALID_OVERLAY_CHANGE = "INVALID_OVERLAY_CHANGE"
  # One of the method parameters was invalid.
  INVALID_PARAMETER = "INVALID_PARAMETER"
  # A malformed request was received.
  INVALID_REQUEST = "INVALID_REQUEST"
  # The "--no-index" flag was passed when the analysis server created, but this
  # API call requires an index to have been generated.
  NO_INDEX_GENERATED = "NO_INDEX_GENERATED"
  # Another refactoring request was received during processing of this one.
  REFACTORING_REQUEST_CANCELLED = "REFACTORING_REQUEST_CANCELLED"
  # The analysis server has already been started (and hence won't accept new
  # connections).
  #
  # This error is included for future expansion; at present the analysis server
  # can only speak to one client at a time so this error will never occur.
  SERVER_ALREADY_STARTED = "SERVER_ALREADY_STARTED"
  # An internal error occurred in the analysis server. Also see the
  # server.error notification.
  SERVER_ERROR = "SERVER_ERROR"
  # An "edit.sortMembers" request specified a FilePath which does not match a
  # Dart file in an analysis root.
  SORT_MEMBERS_INVALID_FILE = "SORT_MEMBERS_INVALID_FILE"
  # An "edit.sortMembers" request specified a Dart file that has scan or parse
  # errors.
  SORT_MEMBERS_PARSE_ERRORS = "SORT_MEMBERS_PARSE_ERRORS"
  # An "analysis.setPriorityFiles" request includes one or more files that are
  # not being analyzed.
  #
  # This is a legacy error; it will be removed before the API reaches version
  # 1.0.
  UNANALYZED_PRIORITY_FILES = "UNANALYZED_PRIORITY_FILES"
  # A request was received which the analysis server does not recognize, or
  # cannot handle in its current configuation.
  UNKNOWN_REQUEST = "UNKNOWN_REQUEST"
  # The analysis server was requested to perform an action on a source that
  # does not exist.
  UNKNOWN_SOURCE = "UNKNOWN_SOURCE"
  # The analysis server was requested to perform an action which is not
  # supported.
  #
  # This is a legacy error; it will be removed before the API reaches version
  # 1.0.
  UNSUPPORTED_FEATURE = "UNSUPPORTED_FEATURE"

  # A list containing all of the enum values that are defined.
  VALUES = ['CONTENT_MODIFIED', 'FORMAT_INVALID_FILE', 'FORMAT_WITH_ERRORS', 'GET_ERRORS_INVALID_FILE', 'INVALID_ANALYSIS_ROOT', 'INVALID_EXECUTION_CONTEXT', 'INVALID_OVERLAY_CHANGE', 'INVALID_PARAMETER', 'INVALID_REQUEST', 'NO_INDEX_GENERATED', 'REFACTORING_REQUEST_CANCELLED', 'SERVER_ALREADY_STARTED', 'SERVER_ERROR', 'SORT_MEMBERS_INVALID_FILE', 'SORT_MEMBERS_PARSE_ERRORS', 'UNANALYZED_PRIORITY_FILES', 'UNKNOWN_REQUEST', 'UNKNOWN_SOURCE', 'UNSUPPORTED_FEATURE']


# SearchResult
#
# {
#   "location": Location
#   "kind": SearchResultKind
#   "isPotential": bool
#   "path": List<Element>
# }
class SearchResult(object):
  def __init__(self, location, kind, isPotential, path):
    # The location of the code that matched the search criteria.
    self.location = location
    # The kind of element that was found or the kind of reference that was
    # found.
    self.kind = kind
    # True if the result is a potential match but cannot be confirmed to be a
    # match. For example, if all references to a method m defined in some class
    # were requested, and a reference to a method m from an unknown class were
    # found, it would be marked as being a potential match.
    self.isPotential = isPotential
    # The elements that contain the result, starting with the most immediately
    # enclosing ancestor and ending with the library.
    self.path = path

  @classmethod
  def from_json(cls, data):
    if not data:
      raise ValueError("SearchResult" + " has no data")

    location = Location.from_json(data["location"])
    kind = data["kind"]
    isPotential = data["isPotential"]
    path = [Element.from_json(x) for x in data["path"]]

    return cls(location, kind, isPotential, path)

  def to_json(self):
    result = {}
    result["location"] = self.location.to_json()
    result["kind"] = self.kind
    result["isPotential"] = self.isPotential
    result["path"] = [x.to_json() for x in self.path]
    return result

  def __str__(self):
    return json.dumps(self.to_json())



# SearchResultKind
#
# enum {
#   DECLARATION
#   INVOCATION
#   READ
#   READ_WRITE
#   REFERENCE
#   UNKNOWN
#   WRITE
# }
class SearchResultKind:
  # The declaration of an element.
  DECLARATION = "DECLARATION"
  # The invocation of a function or method.
  INVOCATION = "INVOCATION"
  # A reference to a field, parameter or variable where it is being read.
  READ = "READ"
  # A reference to a field, parameter or variable where it is being read and
  # written.
  READ_WRITE = "READ_WRITE"
  # A reference to an element.
  REFERENCE = "REFERENCE"
  # Some other kind of search result.
  UNKNOWN = "UNKNOWN"
  # A reference to a field, parameter or variable where it is being written.
  WRITE = "WRITE"

  # A list containing all of the enum values that are defined.
  VALUES = ['DECLARATION', 'INVOCATION', 'READ', 'READ_WRITE', 'REFERENCE', 'UNKNOWN', 'WRITE']


# ServerService
#
# enum {
#   STATUS
# }
class ServerService:
  STATUS = "STATUS"

  # A list containing all of the enum values that are defined.
  VALUES = ['STATUS']


# SourceChange
#
# {
#   "message": String
#   "edits": List<SourceFileEdit>
#   "linkedEditGroups": List<LinkedEditGroup>
#   "selection": optional Position
# }
class SourceChange(object):
  def __init__(self, message, edits=[], linkedEditGroups=[], selection=None):
    # A human-readable description of the change to be applied.
    self.message = message
    # A list of the edits used to effect the change, grouped by file.
    self.edits = edits
    # A list of the linked editing groups used to customize the changes that
    # were made.
    self.linkedEditGroups = linkedEditGroups
    # The position that should be selected after the edits have been applied.
    self.selection = selection
    self.edits = self.edits if self.edits else []

    self.linkedEditGroups = self.linkedEditGroups if self.linkedEditGroups else []



  @classmethod
  def from_json(cls, data):
    if not data:
      raise ValueError("SourceChange" + " has no data")

    message = data["message"]
    edits = [SourceFileEdit.from_json(x) for x in data["edits"]]
    linkedEditGroups = [LinkedEditGroup.from_json(x) for x in data["linkedEditGroups"]]
    selection = data.get("selection", None)
    if selection:
      selection = Position.from_json(selection)

    return cls(message, edits=edits, linkedEditGroups=linkedEditGroups, selection=selection)

  def to_json(self):
    result = {}
    result["message"] = self.message
    result["edits"] = [x.to_json() for x in self.edits]
    result["linkedEditGroups"] = [x.to_json() for x in self.linkedEditGroups]
    if self.selection:
      result["selection"] = self.selection.to_json()
    return result

  def __str__(self):
    return json.dumps(self.to_json())



# SourceEdit
#
# {
#   "offset": int
#   "length": int
#   "replacement": String
#   "id": optional String
# }
class SourceEdit(object):

  def __init__(self, offset, length, replacement, id=''):
    # The offset of the region to be modified.
    self.offset = offset
    # The length of the region to be modified.
    self.length = length
    # The code that is to replace the specified region in the original code.
    self.replacement = replacement
    # An identifier that uniquely identifies this source edit from other edits
    # in the same response. This field is omitted unless a containing structure
    # needs to be able to identify the edit for some reason.
    #
    # For example, some refactoring operations can produce edits that might not
    # be appropriate (referred to as potential edits). Such edits will have an
    # id so that they can be referenced. Edits in the same response that do not
    # need to be referenced will not have an id.
    self.id = id

  @classmethod
  def from_json(cls, data):
    if not data:
      raise ValueError("SourceEdit" + " has no data")

    offset = data["offset"]
    length = data["length"]
    replacement = data["replacement"]
    id = data.get("id", '')
    if id:
      id = id

    return cls(offset, length, replacement, id=id)

  def to_json(self):
    result = {}
    result["offset"] = self.offset
    result["length"] = self.length
    result["replacement"] = self.replacement
    if self.id:
      result["id"] = self.id
    return result

  def __str__(self):
    return json.dumps(self.to_json())



# SourceFileEdit
#
# {
#   "file": FilePath
#   "fileStamp": long
#   "edits": List<SourceEdit>
# }
class SourceFileEdit(object):
  def __init__(self, file, fileStamp, edits=[]):
    # The file containing the code to be modified.
    self.file = file
    # The modification stamp of the file at the moment when the change was
    # created, in milliseconds since the "Unix epoch". Will be -1 if the file
    # did not exist and should be created. The client may use this field to
    # make sure that the file was not changed since then, so it is safe to
    # apply the change.
    self.fileStamp = fileStamp
    # A list of the edits used to effect the change.
    self.edits = edits
    self.edits = self.edits if self.edits else []



  @classmethod
  def from_json(cls, data):
    if not data:
      raise ValueError("SourceFileEdit" + " has no data")

    file = data["file"]
    fileStamp = data["fileStamp"]
    edits = [SourceEdit.from_json(x) for x in data["edits"]]

    return cls(file, fileStamp, edits=edits)

  def to_json(self):
    result = {}
    result["file"] = self.file
    result["fileStamp"] = self.fileStamp
    result["edits"] = [x.to_json() for x in self.edits]
    return result

  def __str__(self):
    return json.dumps(self.to_json())



# TypeHierarchyItem
#
# {
#   "classElement": Element
#   "displayName": optional String
#   "memberElement": optional Element
#   "superclass": optional int
#   "interfaces": List<int>
#   "mixins": List<int>
#   "subclasses": List<int>
# }
class TypeHierarchyItem(object):
  def __init__(self, classElement, displayName='', memberElement=None, superclass=0, interfaces=[], mixins=[], subclasses=[]):
    # The class element represented by this item.
    self.classElement = classElement
    # The name to be displayed for the class. This field will be omitted if the
    # display name is the same as the name of the element. The display name is
    # different if there is additional type information to be displayed, such
    # as type arguments.
    self.displayName = displayName
    # The member in the class corresponding to the member on which the
    # hierarchy was requested. This field will be omitted if the hierarchy was
    # not requested for a member or if the class does not have a corresponding
    # member.
    self.memberElement = memberElement
    # The index of the item representing the superclass of this class. This
    # field will be omitted if this item represents the class Object.
    self.superclass = superclass
    # The indexes of the items representing the interfaces implemented by this
    # class. The list will be empty if there are no implemented interfaces.
    self.interfaces = interfaces
    # The indexes of the items representing the mixins referenced by this
    # class. The list will be empty if there are no classes mixed in to this
    # class.
    self.mixins = mixins
    # The indexes of the items representing the subtypes of this class. The
    # list will be empty if there are no subtypes or if this item represents a
    # supertype of the pivot type.
    self.subclasses = subclasses
    self.interfaces = self.interfaces if self.interfaces else []

    self.mixins = self.mixins if self.mixins else []

    self.subclasses = self.subclasses if self.subclasses else []



  @classmethod
  def from_json(cls, data):
    if not data:
      raise ValueError("TypeHierarchyItem" + " has no data")

    classElement = Element.from_json(data["classElement"])
    displayName = data.get("displayName", '')
    if displayName:
      displayName = displayName
    memberElement = data.get("memberElement", None)
    if memberElement:
      memberElement = Element.from_json(memberElement)
    superclass = data.get("superclass", 0)
    if superclass:
      superclass = superclass
    interfaces = data["interfaces"]
    mixins = data["mixins"]
    subclasses = data["subclasses"]

    return cls(classElement, displayName=displayName, memberElement=memberElement, superclass=superclass, interfaces=interfaces, mixins=mixins, subclasses=subclasses)

  def to_json(self):
    result = {}
    result["classElement"] = self.classElement.to_json()
    if self.displayName:
      result["displayName"] = self.displayName
    if self.memberElement:
      result["memberElement"] = self.memberElement.to_json()
    if self.superclass:
      result["superclass"] = self.superclass
    result["interfaces"] = self.interfaces
    result["mixins"] = self.mixins
    result["subclasses"] = self.subclasses
    return result

  def __str__(self):
    return json.dumps(self.to_json())


# convertGetterToMethod feedback
class ConvertGetterToMethodFeedback(object):
  pass

# convertGetterToMethod options
class ConvertGetterToMethodOptions(object):
  pass

# convertMethodToGetter feedback
class ConvertMethodToGetterFeedback(object):
  pass

# convertMethodToGetter options
class ConvertMethodToGetterOptions(object):
  pass


# extractLocalVariable feedback
#
# {
#   "names": List<String>
#   "offsets": List<int>
#   "lengths": List<int>
# }
class ExtractLocalVariableFeedback(RefactoringFeedback):
  def __init__(self, names, offsets, lengths):
    # The proposed names for the local variable.
    self.names = names
    # The offsets of the expressions that would be replaced by a reference to
    # the variable.
    self.offsets = offsets
    # The lengths of the expressions that would be replaced by a reference to
    # the variable. The lengths correspond to the offsets. In other words, for
    # a given expression, if the offset of that expression is offsets[i], then
    # the length of that expression is lengths[i].
    self.lengths = lengths

  @classmethod
  def from_json(cls, data):
    if not data:
      raise ValueError("extractLocalVariable feedback" + " has no data")

    names = data["names"]
    offsets = data["offsets"]
    lengths = data["lengths"]

    return cls(names, offsets, lengths)

  def to_json(self):
    result = {}
    result["names"] = self.names
    result["offsets"] = self.offsets
    result["lengths"] = self.lengths
    return result

  def __str__(self):
    return json.dumps(self.to_json())



# extractLocalVariable options
#
# {
#   "name": String
#   "extractAll": bool
# }
class ExtractLocalVariableOptions(RefactoringOptions):
  def __init__(self, name, extractAll):
    # The name that the local variable should be given.
    self.name = name
    # True if all occurrences of the expression within the scope in which the
    # variable will be defined should be replaced by a reference to the local
    # variable. The expression used to initiate the refactoring will always be
    # replaced.
    self.extractAll = extractAll

  @classmethod
  def from_json(cls, data):
    if not data:
      raise ValueError("extractLocalVariable options" + " has no data")

    name = data["name"]
    extractAll = data["extractAll"]

    return cls(name, extractAll)

  def to_json(self):
    result = {}
    result["name"] = self.name
    result["extractAll"] = self.extractAll
    return result

  def __str__(self):
    return json.dumps(self.to_json())



# extractMethod feedback
#
# {
#   "offset": int
#   "length": int
#   "returnType": String
#   "names": List<String>
#   "canCreateGetter": bool
#   "parameters": List<RefactoringMethodParameter>
#   "offsets": List<int>
#   "lengths": List<int>
# }
class ExtractMethodFeedback(RefactoringFeedback):
  def __init__(self, offset, length, returnType, names, canCreateGetter, parameters, offsets, lengths):
    # The offset to the beginning of the expression or statements that will be
    # extracted.
    self.offset = offset
    # The length of the expression or statements that will be extracted.
    self.length = length
    # The proposed return type for the method. If the returned element does not
    # have a declared return type, this field will contain an empty string.
    self.returnType = returnType
    # The proposed names for the method.
    self.names = names
    # True if a getter could be created rather than a method.
    self.canCreateGetter = canCreateGetter
    # The proposed parameters for the method.
    self.parameters = parameters
    # The offsets of the expressions or statements that would be replaced by an
    # invocation of the method.
    self.offsets = offsets
    # The lengths of the expressions or statements that would be replaced by an
    # invocation of the method. The lengths correspond to the offsets. In other
    # words, for a given expression (or block of statements), if the offset of
    # that expression is offsets[i], then the length of that expression is
    # lengths[i].
    self.lengths = lengths

  @classmethod
  def from_json(cls, data):
    if not data:
      raise ValueError("extractMethod feedback" + " has no data")

    offset = data["offset"]
    length = data["length"]
    returnType = data["returnType"]
    names = data["names"]
    canCreateGetter = data["canCreateGetter"]
    parameters = [RefactoringMethodParameter.from_json(x) for x in data["parameters"]]
    offsets = data["offsets"]
    lengths = data["lengths"]

    return cls(offset, length, returnType, names, canCreateGetter, parameters, offsets, lengths)

  def to_json(self):
    result = {}
    result["offset"] = self.offset
    result["length"] = self.length
    result["returnType"] = self.returnType
    result["names"] = self.names
    result["canCreateGetter"] = self.canCreateGetter
    result["parameters"] = [x.to_json() for x in self.parameters]
    result["offsets"] = self.offsets
    result["lengths"] = self.lengths
    return result

  def __str__(self):
    return json.dumps(self.to_json())



# extractMethod options
#
# {
#   "returnType": String
#   "createGetter": bool
#   "name": String
#   "parameters": List<RefactoringMethodParameter>
#   "extractAll": bool
# }
class ExtractMethodOptions(RefactoringOptions):
  def __init__(self, returnType, createGetter, name, parameters, extractAll):
    # The return type that should be defined for the method.
    self.returnType = returnType
    # True if a getter should be created rather than a method. It is an error
    # if this field is true and the list of parameters is non-empty.
    self.createGetter = createGetter
    # The name that the method should be given.
    self.name = name
    # The parameters that should be defined for the method.
    #
    # It is an error if a REQUIRED or NAMED parameter follows a POSITIONAL
    # parameter. It is an error if a REQUIRED or POSITIONAL parameter follows a
    # NAMED parameter.
    #
    # - To change the order and/or update proposed parameters, add parameters
    #   with the same identifiers as proposed.
    # - To add new parameters, omit their identifier.
    # - To remove some parameters, omit them in this list.
    self.parameters = parameters
    # True if all occurrences of the expression or statements should be
    # replaced by an invocation of the method. The expression or statements
    # used to initiate the refactoring will always be replaced.
    self.extractAll = extractAll

  @classmethod
  def from_json(cls, data):
    if not data:
      raise ValueError("extractMethod options" + " has no data")

    returnType = data["returnType"]
    createGetter = data["createGetter"]
    name = data["name"]
    parameters = [RefactoringMethodParameter.from_json(x) for x in data["parameters"]]
    extractAll = data["extractAll"]

    return cls(returnType, createGetter, name, parameters, extractAll)

  def to_json(self):
    result = {}
    result["returnType"] = self.returnType
    result["createGetter"] = self.createGetter
    result["name"] = self.name
    result["parameters"] = [x.to_json() for x in self.parameters]
    result["extractAll"] = self.extractAll
    return result

  def __str__(self):
    return json.dumps(self.to_json())



# inlineLocalVariable feedback
#
# {
#   "name": String
#   "occurrences": int
# }
class InlineLocalVariableFeedback(RefactoringFeedback):
  def __init__(self, name, occurrences):
    # The name of the variable being inlined.
    self.name = name
    # The number of times the variable occurs.
    self.occurrences = occurrences

  @classmethod
  def from_json(cls, data):
    if not data:
      raise ValueError("inlineLocalVariable feedback" + " has no data")

    name = data["name"]
    occurrences = data["occurrences"]

    return cls(name, occurrences)

  def to_json(self):
    result = {}
    result["name"] = self.name
    result["occurrences"] = self.occurrences
    return result

  def __str__(self):
    return json.dumps(self.to_json())


# inlineLocalVariable options
class InlineLocalVariableOptions(object):
  pass


# inlineMethod feedback
#
# {
#   "className": optional String
#   "methodName": String
#   "isDeclaration": bool
# }
class InlineMethodFeedback(RefactoringFeedback):
  def __init__(self, methodName, isDeclaration, className=''):
    # The name of the class enclosing the method being inlined. If not a class
    # member is being inlined, this field will be absent.
    self.className = className
    # The name of the method (or function) being inlined.
    self.methodName = methodName
    # True if the declaration of the method is selected. So all references
    # should be inlined.
    self.isDeclaration = isDeclaration

  @classmethod
  def from_json(cls, data):
    if not data:
      raise ValueError("inlineMethod feedback" + " has no data")

    className = data.get("className", '')
    if className:
      className = className
    methodName = data["methodName"]
    isDeclaration = data["isDeclaration"]

    return cls(methodName, isDeclaration, className=className)

  def to_json(self):
    result = {}
    if self.className:
      result["className"] = self.className
    result["methodName"] = self.methodName
    result["isDeclaration"] = self.isDeclaration
    return result

  def __str__(self):
    return json.dumps(self.to_json())



# inlineMethod options
#
# {
#   "deleteSource": bool
#   "inlineAll": bool
# }
class InlineMethodOptions(RefactoringOptions):
  def __init__(self, deleteSource, inlineAll):
    # True if the method being inlined should be removed. It is an error if
    # this field is true and inlineAll is false.
    self.deleteSource = deleteSource
    # True if all invocations of the method should be inlined, or false if only
    # the invocation site used to create this refactoring should be inlined.
    self.inlineAll = inlineAll

  @classmethod
  def from_json(cls, data):
    if not data:
      raise ValueError("inlineMethod options" + " has no data")

    deleteSource = data["deleteSource"]
    inlineAll = data["inlineAll"]

    return cls(deleteSource, inlineAll)

  def to_json(self):
    result = {}
    result["deleteSource"] = self.deleteSource
    result["inlineAll"] = self.inlineAll
    return result

  def __str__(self):
    return json.dumps(self.to_json())


# moveFile feedback
class MoveFileFeedback(object):
  pass


# moveFile options
#
# {
#   "newFile": FilePath
# }
class MoveFileOptions(RefactoringOptions):
  def __init__(self, newFile):
    # The new file path to which the given file is being moved.
    self.newFile = newFile

  @classmethod
  def from_json(cls, data):
    if not data:
      raise ValueError("moveFile options" + " has no data")

    newFile = data["newFile"]

    return cls(newFile)

  def to_json(self):
    result = {}
    result["newFile"] = self.newFile
    return result

  def __str__(self):
    return json.dumps(self.to_json())



# rename feedback
#
# {
#   "offset": int
#   "length": int
#   "elementKindName": String
#   "oldName": String
# }
class RenameFeedback(RefactoringFeedback):
  def __init__(self, offset, length, elementKindName, oldName):
    # The offset to the beginning of the name selected to be renamed.
    self.offset = offset
    # The length of the name selected to be renamed.
    self.length = length
    # The human-readable description of the kind of element being renamed (such
    # as “class” or “function type alias”).
    self.elementKindName = elementKindName
    # The old name of the element before the refactoring.
    self.oldName = oldName

  @classmethod
  def from_json(cls, data):
    if not data:
      raise ValueError("rename feedback" + " has no data")

    offset = data["offset"]
    length = data["length"]
    elementKindName = data["elementKindName"]
    oldName = data["oldName"]

    return cls(offset, length, elementKindName, oldName)

  def to_json(self):
    result = {}
    result["offset"] = self.offset
    result["length"] = self.length
    result["elementKindName"] = self.elementKindName
    result["oldName"] = self.oldName
    return result

  def __str__(self):
    return json.dumps(self.to_json())



# rename options
#
# {
#   "newName": String
# }
class RenameOptions(RefactoringOptions):
  def __init__(self, newName):
    # The name that the element should have after the refactoring.
    self.newName = newName

  @classmethod
  def from_json(cls, data):
    if not data:
      raise ValueError("rename options" + " has no data")

    newName = data["newName"]

    return cls(newName)

  def to_json(self):
    result = {}
    result["newName"] = self.newName
    return result

  def __str__(self):
    return json.dumps(self.to_json())


