# Copyright (c) 2014, the Dart project authors.  Please see the AUTHORS file
# for details. All rights reserved. Use of this source code is governed by a
# BSD-style license that can be found in the LICENSE file.
#
# This file has been automatically generated.  Please do not edit it manually.
# To regenerate the file, use the script
# "pkg/analysis_server/tool/spec/generate_files".

class AddContentOverlay(object):
  """
  A directive to begin overlaying the contents of a file. The supplied content
  will be used for analysis in place of the file contents in the filesystem.

  If this directive is used on a file that already has a file content overlay,
  the old overlay is discarded and replaced with the new one.
  """

  def __init__(self, content):
    self.type = "add"

    # The new content of the file.
    self.content = content


  def __str__(self):
    builder = []
    builder.append("[")
    builder.append("type=")
    builder.append(str(self.type) + ", ")
    builder.append("content=")
    builder.append(str(self.content))
    builder.append("]")
    return "".join(builder)

  @staticmethod
  def fromJson(data):
    type = data["type"]
    content = data["content"]
    return AddContentOverlay(content);

  def toJson(self):
    return {
      "type": self.type,
      "content": self.content,
    }

class AnalysisError(object):
  """
  An indication of an error, warning, or hint that was produced by the
  analysis.
  """

  def __init__(self, severity, type, location, message, correction):
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


  def __str__(self):
    builder = []
    builder.append("[")
    builder.append("severity=")
    builder.append(str(self.severity) + ", ")
    builder.append("type=")
    builder.append(str(self.type) + ", ")
    builder.append("location=")
    builder.append(str(self.location) + ", ")
    builder.append("message=")
    builder.append(str(self.message) + ", ")
    builder.append("correction=")
    builder.append(str(self.correction))
    builder.append("]")
    return "".join(builder)

  @staticmethod
  def fromJson(data):
    severity = data["severity"]
    type = data["type"]
    location = Location.fromJson(data["location"])
    message = data["message"]
    correction = None if not data.get("correction") else data["correction"]
    return AnalysisError(severity, type, location, message, correction);

  def toJson(self):
    return {
      "severity": self.severity,
      "type": self.type,
      "location": self.location.toJson(),
      "message": self.message,
      "correction": self.correction,
    }

class AnalysisErrorFixes(object):
  """
  A list of fixes associated with a specific error
  """

  def __init__(self, error, fixes):
    # The error with which the fixes are associated.
    self.error = error

    # The fixes associated with the error.
    self.fixes = fixes


  def __str__(self):
    builder = []
    builder.append("[")
    builder.append("error=")
    builder.append(str(self.error) + ", ")
    builder.append("fixes=")
    builder.append(", ".join(self.fixes))
    builder.append("]")
    return "".join(builder)

  @staticmethod
  def fromJson(data):
    error = AnalysisError.fromJson(data["error"])
    fixes = [SourceChange.fromJson(item) for item in data["fixes"]]
    return AnalysisErrorFixes(error, fixes);

  def toJson(self):
    return {
      "error": self.error.toJson(),
      "fixes": [x.toJson() for x in self.fixes],
    }

class AnalysisErrorSeverity:
  """
  An enumeration of the possible severities of analysis errors.
  """

  INFO = "INFO"

  WARNING = "WARNING"

  ERROR = "ERROR"

class AnalysisErrorType:
  """
  An enumeration of the possible types of analysis errors.
  """

  CHECKED_MODE_COMPILE_TIME_ERROR = "CHECKED_MODE_COMPILE_TIME_ERROR"

  COMPILE_TIME_ERROR = "COMPILE_TIME_ERROR"

  HINT = "HINT"

  LINT = "LINT"

  STATIC_TYPE_WARNING = "STATIC_TYPE_WARNING"

  STATIC_WARNING = "STATIC_WARNING"

  SYNTACTIC_ERROR = "SYNTACTIC_ERROR"

  TODO = "TODO"

class AnalysisOptions(object):
  """
  A set of options controlling what kind of analysis is to be performed. If the
  value of a field is omitted the value of the option will not be changed.
  """

  def __init__(self, enableAsync, enableDeferredLoading, enableEnums, generateDart2jsHints, generateHints, generateLints):
    # Deprecated/
    #
    # True if the client wants to enable support for the proposed async feature.
    self.enableAsync = enableAsync

    # Deprecated/
    #
    # True if the client wants to enable support for the proposed deferred
    # loading feature.
    self.enableDeferredLoading = enableDeferredLoading

    # Deprecated/
    #
    # True if the client wants to enable support for the proposed enum feature.
    self.enableEnums = enableEnums

    # True if hints that are specific to dart2js should be generated. This option
    # is ignored if generateHints is false.
    self.generateDart2jsHints = generateDart2jsHints

    # True if hints should be generated as part of generating errors and
    # warnings.
    self.generateHints = generateHints

    # True if lints should be generated as part of generating errors and
    # warnings.
    self.generateLints = generateLints


  def __str__(self):
    builder = []
    builder.append("[")
    builder.append("enableAsync=")
    builder.append(str(self.enableAsync) + ", ")
    builder.append("enableDeferredLoading=")
    builder.append(str(self.enableDeferredLoading) + ", ")
    builder.append("enableEnums=")
    builder.append(str(self.enableEnums) + ", ")
    builder.append("generateDart2jsHints=")
    builder.append(str(self.generateDart2jsHints) + ", ")
    builder.append("generateHints=")
    builder.append(str(self.generateHints) + ", ")
    builder.append("generateLints=")
    builder.append(str(self.generateLints))
    builder.append("]")
    return "".join(builder)

  @staticmethod
  def fromJson(data):
    enableAsync = None if not data.get("enableAsync") else data["enableAsync"]
    enableDeferredLoading = None if not data.get("enableDeferredLoading") else data["enableDeferredLoading"]
    enableEnums = None if not data.get("enableEnums") else data["enableEnums"]
    generateDart2jsHints = None if not data.get("generateDart2jsHints") else data["generateDart2jsHints"]
    generateHints = None if not data.get("generateHints") else data["generateHints"]
    generateLints = None if not data.get("generateLints") else data["generateLints"]
    return AnalysisOptions(enableAsync, enableDeferredLoading, enableEnums, generateDart2jsHints, generateHints, generateLints);

  def toJson(self):
    return {
      "enableAsync": self.enableAsync,
      "enableDeferredLoading": self.enableDeferredLoading,
      "enableEnums": self.enableEnums,
      "generateDart2jsHints": self.generateDart2jsHints,
      "generateHints": self.generateHints,
      "generateLints": self.generateLints,
    }

class AnalysisService:
  """
  An enumeration of the services provided by the analysis domain.
  """

  FOLDING = "FOLDING"

  HIGHLIGHTS = "HIGHLIGHTS"

  INVALIDATE = "INVALIDATE"

  NAVIGATION = "NAVIGATION"

  OCCURRENCES = "OCCURRENCES"

  OUTLINE = "OUTLINE"

  OVERRIDES = "OVERRIDES"

class AnalysisStatus(object):
  """
  An indication of the current state of analysis.
  """

  def __init__(self, isAnalyzing, analysisTarget):
    # True if analysis is currently being performed.
    self.isAnalyzing = isAnalyzing

    # The name of the current target of analysis. This field is omitted if
    # analyzing is false.
    self.analysisTarget = analysisTarget


  def __str__(self):
    builder = []
    builder.append("[")
    builder.append("isAnalyzing=")
    builder.append(str(self.isAnalyzing) + ", ")
    builder.append("analysisTarget=")
    builder.append(str(self.analysisTarget))
    builder.append("]")
    return "".join(builder)

  @staticmethod
  def fromJson(data):
    isAnalyzing = data["isAnalyzing"]
    analysisTarget = None if not data.get("analysisTarget") else data["analysisTarget"]
    return AnalysisStatus(isAnalyzing, analysisTarget);

  def toJson(self):
    return {
      "isAnalyzing": self.isAnalyzing,
      "analysisTarget": self.analysisTarget,
    }

class ChangeContentOverlay(object):
  """
  A directive to modify an existing file content overlay. One or more ranges of
  text are deleted from the old file content overlay and replaced with new
  text.

  The edits are applied in the order in which they occur in the list. This
  means that the offset of each edit must be correct under the assumption that
  all previous edits have been applied.

  It is an error to use this overlay on a file that does not yet have a file
  content overlay or that has had its overlay removed via RemoveContentOverlay.

  If any of the edits cannot be applied due to its offset or length being out
  of range, an INVALID_OVERLAY_CHANGE error will be reported.
  """

  def __init__(self, edits):
    self.type = "change"

    # The edits to be applied to the file.
    self.edits = edits


  def __str__(self):
    builder = []
    builder.append("[")
    builder.append("type=")
    builder.append(str(self.type) + ", ")
    builder.append("edits=")
    builder.append(", ".join(self.edits))
    builder.append("]")
    return "".join(builder)

  @staticmethod
  def fromJson(data):
    type = data["type"]
    edits = [SourceEdit.fromJson(item) for item in data["edits"]]
    return ChangeContentOverlay(edits);

  def toJson(self):
    return {
      "type": self.type,
      "edits": [x.toJson() for x in self.edits],
    }

class CompletionSuggestion(object):
  """
  A suggestion for how to complete partially entered text. Many of the fields
  are optional, depending on the kind of element being suggested.
  """

  def __init__(self, kind, relevance, completion, selectionOffset, selectionLength, isDeprecated, isPotential, docSummary, docComplete, declaringType, element, returnType, parameterNames, parameterTypes, requiredParameterCount, hasNamedParameters, parameterName, parameterType):
    # The kind of element being suggested.
    self.kind = kind

    # The relevance of this completion suggestion where a higher number indicates
    # a higher relevance.
    self.relevance = relevance

    # The identifier to be inserted if the suggestion is selected. If the
    # suggestion is for a method or function, the client might want to
    # additionally insert a template for the parameters. The information required
    # in order to do so is contained in other fields.
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
    # suggested, This field is omitted if there is no Dartdoc associated with the
    # element.
    self.docSummary = docSummary

    # The Dartdoc associated with the element being suggested, This field is
    # omitted if there is no Dartdoc associated with the element.
    self.docComplete = docComplete

    # The class that declares the element being suggested. This field is omitted
    # if the suggested element is not a member of a class.
    self.declaringType = declaringType

    # Information about the element reference being suggested.
    self.element = element

    # The return type of the getter, function or method or the type of the field
    # being suggested. This field is omitted if the suggested element is not a
    # getter, function or method.
    self.returnType = returnType

    # The names of the parameters of the function or method being suggested. This
    # field is omitted if the suggested element is not a setter, function or
    # method.
    self.parameterNames = parameterNames

    # The types of the parameters of the function or method being suggested. This
    # field is omitted if the parameterNames field is omitted.
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

    # The type of the options parameter being suggested. This field is omitted if
    # the parameterName field is omitted.
    self.parameterType = parameterType


  def __str__(self):
    builder = []
    builder.append("[")
    builder.append("kind=")
    builder.append(str(self.kind) + ", ")
    builder.append("relevance=")
    builder.append(str(self.relevance) + ", ")
    builder.append("completion=")
    builder.append(str(self.completion) + ", ")
    builder.append("selectionOffset=")
    builder.append(str(self.selectionOffset) + ", ")
    builder.append("selectionLength=")
    builder.append(str(self.selectionLength) + ", ")
    builder.append("isDeprecated=")
    builder.append(str(self.isDeprecated) + ", ")
    builder.append("isPotential=")
    builder.append(str(self.isPotential) + ", ")
    builder.append("docSummary=")
    builder.append(str(self.docSummary) + ", ")
    builder.append("docComplete=")
    builder.append(str(self.docComplete) + ", ")
    builder.append("declaringType=")
    builder.append(str(self.declaringType) + ", ")
    builder.append("element=")
    builder.append(str(self.element) + ", ")
    builder.append("returnType=")
    builder.append(str(self.returnType) + ", ")
    builder.append("parameterNames=")
    builder.append(", ".join(self.parameterNames) + ", ")
    builder.append("parameterTypes=")
    builder.append(", ".join(self.parameterTypes) + ", ")
    builder.append("requiredParameterCount=")
    builder.append(str(self.requiredParameterCount) + ", ")
    builder.append("hasNamedParameters=")
    builder.append(str(self.hasNamedParameters) + ", ")
    builder.append("parameterName=")
    builder.append(str(self.parameterName) + ", ")
    builder.append("parameterType=")
    builder.append(str(self.parameterType))
    builder.append("]")
    return "".join(builder)

  @staticmethod
  def fromJson(data):
    kind = data["kind"]
    relevance = data["relevance"]
    completion = data["completion"]
    selectionOffset = data["selectionOffset"]
    selectionLength = data["selectionLength"]
    isDeprecated = data["isDeprecated"]
    isPotential = data["isPotential"]
    docSummary = None if not data.get("docSummary") else data["docSummary"]
    docComplete = None if not data.get("docComplete") else data["docComplete"]
    declaringType = None if not data.get("declaringType") else data["declaringType"]
    element = None if not data.get("element") else Element.fromJson(data["element"])
    returnType = None if not data.get("returnType") else data["returnType"]
    parameterNames = None if not data.get("parameterNames") else data["parameterNames"]
    parameterTypes = None if not data.get("parameterTypes") else data["parameterTypes"]
    requiredParameterCount = None if not data.get("requiredParameterCount") else data["requiredParameterCount"]
    hasNamedParameters = None if not data.get("hasNamedParameters") else data["hasNamedParameters"]
    parameterName = None if not data.get("parameterName") else data["parameterName"]
    parameterType = None if not data.get("parameterType") else data["parameterType"]
    return CompletionSuggestion(kind, relevance, completion, selectionOffset, selectionLength, isDeprecated, isPotential, docSummary, docComplete, declaringType, element, returnType, parameterNames, parameterTypes, requiredParameterCount, hasNamedParameters, parameterName, parameterType);

  def toJson(self):
    return {
      "kind": self.kind,
      "relevance": self.relevance,
      "completion": self.completion,
      "selectionOffset": self.selectionOffset,
      "selectionLength": self.selectionLength,
      "isDeprecated": self.isDeprecated,
      "isPotential": self.isPotential,
      "docSummary": self.docSummary,
      "docComplete": self.docComplete,
      "declaringType": self.declaringType,
      "element": self.element.toJson(),
      "returnType": self.returnType,
      "parameterNames": self.parameterNames,
      "parameterTypes": self.parameterTypes,
      "requiredParameterCount": self.requiredParameterCount,
      "hasNamedParameters": self.hasNamedParameters,
      "parameterName": self.parameterName,
      "parameterType": self.parameterType,
    }

class CompletionSuggestionKind:
  """
  An enumeration of the kinds of elements that can be included in a completion
  suggestion.
  """

  # A list of arguments for the method or function that is being invoked. For
  # this suggestion kind, the completion field is a textual representation of the
  # invocation and the parameterNames, parameterTypes, and requiredParameterCount
  # attributes are defined.
  ARGUMENT_LIST = "ARGUMENT_LIST"

  IMPORT = "IMPORT"

  # The element identifier should be inserted at the completion location. For
  # example "someMethod" in import 'myLib.dart' show someMethod; . For
  # suggestions of this kind, the element attribute is defined and the completion
  # field is the element's identifier.
  IDENTIFIER = "IDENTIFIER"

  # The element is being invoked at the completion location. For example,
  # "someMethod" in x.someMethod(); . For suggestions of this kind, the element
  # attribute is defined and the completion field is the element's identifier.
  INVOCATION = "INVOCATION"

  # A keyword is being suggested. For suggestions of this kind, the completion is
  # the keyword.
  KEYWORD = "KEYWORD"

  NAMED_ARGUMENT = "NAMED_ARGUMENT"

  OPTIONAL_ARGUMENT = "OPTIONAL_ARGUMENT"

  PARAMETER = "PARAMETER"

class Element(object):
  """
  Information about an element (something that can be declared in code).
  """

  ABSTRACT = 0x01

  CONST = 0x02

  FINAL = 0x04

  TOP_LEVEL_STATIC = 0x08

  PRIVATE = 0x10

  DEPRECATED = 0x20

  def __init__(self, kind, name, location, flags, parameters, returnType):
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
    # - 0x08 - set if the element is a static member of a class or is a top-level
    #   function or field
    # - 0x10 - set if the element is private
    # - 0x20 - set if the element is deprecated
    self.flags = flags

    # The parameter list for the element. If the element is not a method or
    # function this field will not be defined. If the element doesn't have
    # parameters (e.g. getter), this field will not be defined. If the element
    # has zero parameters, this field will have a value of "()".
    self.parameters = parameters

    # The return type of the element. If the element is not a method or function
    # this field will not be defined. If the element does not have a declared
    # return type, this field will contain an empty string.
    self.returnType = returnType


  def __str__(self):
    builder = []
    builder.append("[")
    builder.append("kind=")
    builder.append(str(self.kind) + ", ")
    builder.append("name=")
    builder.append(str(self.name) + ", ")
    builder.append("location=")
    builder.append(str(self.location) + ", ")
    builder.append("flags=")
    builder.append(str(self.flags) + ", ")
    builder.append("parameters=")
    builder.append(str(self.parameters) + ", ")
    builder.append("returnType=")
    builder.append(str(self.returnType))
    builder.append("]")
    return "".join(builder)

  @staticmethod
  def fromJson(data):
    kind = data["kind"]
    name = data["name"]
    location = None if not data.get("location") else Location.fromJson(data["location"])
    flags = data["flags"]
    parameters = None if not data.get("parameters") else data["parameters"]
    returnType = None if not data.get("returnType") else data["returnType"]
    return Element(kind, name, location, flags, parameters, returnType);

  def toJson(self):
    return {
      "kind": self.kind,
      "name": self.name,
      "location": self.location.toJson(),
      "flags": self.flags,
      "parameters": self.parameters,
      "returnType": self.returnType,
    }

class ElementKind:
  """
  An enumeration of the kinds of elements.
  """

  CLASS = "CLASS"

  CLASS_TYPE_ALIAS = "CLASS_TYPE_ALIAS"

  COMPILATION_UNIT = "COMPILATION_UNIT"

  CONSTRUCTOR = "CONSTRUCTOR"

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

class ExecutableFile(object):
  """
  A description of an executable file.
  """

  def __init__(self, file, kind):
    # The path of the executable file.
    self.file = file

    # The kind of the executable file.
    self.kind = kind


  def __str__(self):
    builder = []
    builder.append("[")
    builder.append("file=")
    builder.append(str(self.file) + ", ")
    builder.append("kind=")
    builder.append(str(self.kind))
    builder.append("]")
    return "".join(builder)

  @staticmethod
  def fromJson(data):
    file = data["file"]
    kind = data["kind"]
    return ExecutableFile(file, kind);

  def toJson(self):
    return {
      "file": self.file,
      "kind": self.kind,
    }

class ExecutableKind:
  """
  An enumeration of the kinds of executable files.
  """

  CLIENT = "CLIENT"

  EITHER = "EITHER"

  NOT_EXECUTABLE = "NOT_EXECUTABLE"

  SERVER = "SERVER"

class ExecutionService:
  """
  An enumeration of the services provided by the execution domain.
  """

  LAUNCH_DATA = "LAUNCH_DATA"

class FoldingKind:
  """
  An enumeration of the kinds of folding regions.
  """

  COMMENT = "COMMENT"

  CLASS_MEMBER = "CLASS_MEMBER"

  DIRECTIVES = "DIRECTIVES"

  DOCUMENTATION_COMMENT = "DOCUMENTATION_COMMENT"

  TOP_LEVEL_DECLARATION = "TOP_LEVEL_DECLARATION"

class FoldingRegion(object):
  """
  A description of a region that can be folded.
  """

  def __init__(self, kind, offset, length):
    # The kind of the region.
    self.kind = kind

    # The offset of the region to be folded.
    self.offset = offset

    # The length of the region to be folded.
    self.length = length


  def __str__(self):
    builder = []
    builder.append("[")
    builder.append("kind=")
    builder.append(str(self.kind) + ", ")
    builder.append("offset=")
    builder.append(str(self.offset) + ", ")
    builder.append("length=")
    builder.append(str(self.length))
    builder.append("]")
    return "".join(builder)

  @staticmethod
  def fromJson(data):
    kind = data["kind"]
    offset = data["offset"]
    length = data["length"]
    return FoldingRegion(kind, offset, length);

  def toJson(self):
    return {
      "kind": self.kind,
      "offset": self.offset,
      "length": self.length,
    }

class HighlightRegion(object):
  """
  A description of a region that could have special highlighting associated
  with it.
  """

  def __init__(self, type, offset, length):
    # The type of highlight associated with the region.
    self.type = type

    # The offset of the region to be highlighted.
    self.offset = offset

    # The length of the region to be highlighted.
    self.length = length


  def __str__(self):
    builder = []
    builder.append("[")
    builder.append("type=")
    builder.append(str(self.type) + ", ")
    builder.append("offset=")
    builder.append(str(self.offset) + ", ")
    builder.append("length=")
    builder.append(str(self.length))
    builder.append("]")
    return "".join(builder)

  def containsInclusive(self, x):
    return self.offset <= x and x <= self.offset + self.length

  @staticmethod
  def fromJson(data):
    type = data["type"]
    offset = data["offset"]
    length = data["length"]
    return HighlightRegion(type, offset, length);

  def toJson(self):
    return {
      "type": self.type,
      "offset": self.offset,
      "length": self.length,
    }

class HighlightRegionType:
  """
  An enumeration of the kinds of highlighting that can be applied to files.
  """

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

class HoverInformation(object):
  """
  The hover information associated with a specific location.
  """

  def __init__(self, offset, length, containingLibraryPath, containingLibraryName, dartdoc, elementDescription, elementKind, parameter, propagatedType, staticType):
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

    # The dartdoc associated with the referenced element. Other than the removal
    # of the comment delimiters, including leading asterisks in the case of a
    # block comment, the dartdoc is unprocessed markdown. This data is omitted if
    # there is no referenced element, or if the element has no dartdoc.
    self.dartdoc = dartdoc

    # A human-readable description of the element being referenced. This data is
    # omitted if there is no referenced element.
    self.elementDescription = elementDescription

    # A human-readable description of the kind of element being referenced (such
    # as “class” or “function type alias”). This data is omitted if there is no
    # referenced element.
    self.elementKind = elementKind

    # A human-readable description of the parameter corresponding to the
    # expression being hovered over. This data is omitted if the location is not
    # in an argument to a function.
    self.parameter = parameter

    # The name of the propagated type of the expression. This data is omitted if
    # the location does not correspond to an expression or if there is no
    # propagated type information.
    self.propagatedType = propagatedType

    # The name of the static type of the expression. This data is omitted if the
    # location does not correspond to an expression.
    self.staticType = staticType


  def __str__(self):
    builder = []
    builder.append("[")
    builder.append("offset=")
    builder.append(str(self.offset) + ", ")
    builder.append("length=")
    builder.append(str(self.length) + ", ")
    builder.append("containingLibraryPath=")
    builder.append(str(self.containingLibraryPath) + ", ")
    builder.append("containingLibraryName=")
    builder.append(str(self.containingLibraryName) + ", ")
    builder.append("dartdoc=")
    builder.append(str(self.dartdoc) + ", ")
    builder.append("elementDescription=")
    builder.append(str(self.elementDescription) + ", ")
    builder.append("elementKind=")
    builder.append(str(self.elementKind) + ", ")
    builder.append("parameter=")
    builder.append(str(self.parameter) + ", ")
    builder.append("propagatedType=")
    builder.append(str(self.propagatedType) + ", ")
    builder.append("staticType=")
    builder.append(str(self.staticType))
    builder.append("]")
    return "".join(builder)

  @staticmethod
  def fromJson(data):
    offset = data["offset"]
    length = data["length"]
    containingLibraryPath = None if not data.get("containingLibraryPath") else data["containingLibraryPath"]
    containingLibraryName = None if not data.get("containingLibraryName") else data["containingLibraryName"]
    dartdoc = None if not data.get("dartdoc") else data["dartdoc"]
    elementDescription = None if not data.get("elementDescription") else data["elementDescription"]
    elementKind = None if not data.get("elementKind") else data["elementKind"]
    parameter = None if not data.get("parameter") else data["parameter"]
    propagatedType = None if not data.get("propagatedType") else data["propagatedType"]
    staticType = None if not data.get("staticType") else data["staticType"]
    return HoverInformation(offset, length, containingLibraryPath, containingLibraryName, dartdoc, elementDescription, elementKind, parameter, propagatedType, staticType);

  def toJson(self):
    return {
      "offset": self.offset,
      "length": self.length,
      "containingLibraryPath": self.containingLibraryPath,
      "containingLibraryName": self.containingLibraryName,
      "dartdoc": self.dartdoc,
      "elementDescription": self.elementDescription,
      "elementKind": self.elementKind,
      "parameter": self.parameter,
      "propagatedType": self.propagatedType,
      "staticType": self.staticType,
    }

class LinkedEditGroup(object):
  """
  A collection of positions that should be linked (edited simultaneously) for
  the purposes of updating code after a source change. For example, if a set of
  edits introduced a new variable name, the group would contain all of the
  positions of the variable name so that if the client wanted to let the user
  edit the variable name after the operation, all occurrences of the name could
  be edited simultaneously.
  """

  def __init__(self, positions, length, suggestions):
    # The positions of the regions that should be edited simultaneously.
    self.positions = positions

    # The length of the regions that should be edited simultaneously.
    self.length = length

    # Pre-computed suggestions for what every region might want to be changed to.
    self.suggestions = suggestions


  def __str__(self):
    builder = []
    builder.append("[")
    builder.append("positions=")
    builder.append(", ".join(self.positions) + ", ")
    builder.append("length=")
    builder.append(str(self.length) + ", ")
    builder.append("suggestions=")
    builder.append(", ".join(self.suggestions))
    builder.append("]")
    return "".join(builder)

  @staticmethod
  def fromJson(data):
    positions = [Position.fromJson(item) for item in data["positions"]]
    length = data["length"]
    suggestions = [LinkedEditSuggestion.fromJson(item) for item in data["suggestions"]]
    return LinkedEditGroup(positions, length, suggestions);

  def toJson(self):
    return {
      "positions": [x.toJson() for x in self.positions],
      "length": self.length,
      "suggestions": [x.toJson() for x in self.suggestions],
    }

class LinkedEditSuggestion(object):
  """
  A suggestion of a value that could be used to replace all of the linked edit
  regions in a LinkedEditGroup.
  """

  def __init__(self, value, kind):
    # The value that could be used to replace all of the linked edit regions.
    self.value = value

    # The kind of value being proposed.
    self.kind = kind


  def __str__(self):
    builder = []
    builder.append("[")
    builder.append("value=")
    builder.append(str(self.value) + ", ")
    builder.append("kind=")
    builder.append(str(self.kind))
    builder.append("]")
    return "".join(builder)

  @staticmethod
  def fromJson(data):
    value = data["value"]
    kind = data["kind"]
    return LinkedEditSuggestion(value, kind);

  def toJson(self):
    return {
      "value": self.value,
      "kind": self.kind,
    }

class LinkedEditSuggestionKind:
  """
  An enumeration of the kind of values that can be suggested for a linked edit.
  """

  METHOD = "METHOD"

  PARAMETER = "PARAMETER"

  TYPE = "TYPE"

  VARIABLE = "VARIABLE"

class Location(object):
  """
  A location (character range) within a file.
  """

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


  def __str__(self):
    builder = []
    builder.append("[")
    builder.append("file=")
    builder.append(str(self.file) + ", ")
    builder.append("offset=")
    builder.append(str(self.offset) + ", ")
    builder.append("length=")
    builder.append(str(self.length) + ", ")
    builder.append("startLine=")
    builder.append(str(self.startLine) + ", ")
    builder.append("startColumn=")
    builder.append(str(self.startColumn))
    builder.append("]")
    return "".join(builder)

  @staticmethod
  def fromJson(data):
    file = data["file"]
    offset = data["offset"]
    length = data["length"]
    startLine = data["startLine"]
    startColumn = data["startColumn"]
    return Location(file, offset, length, startLine, startColumn);

  def toJson(self):
    return {
      "file": self.file,
      "offset": self.offset,
      "length": self.length,
      "startLine": self.startLine,
      "startColumn": self.startColumn,
    }

class NavigationRegion(object):
  """
  A description of a region from which the user can navigate to the declaration
  of an element.
  """

  def __init__(self, offset, length, targets):
    # The offset of the region from which the user can navigate.
    self.offset = offset

    # The length of the region from which the user can navigate.
    self.length = length

    # The indexes of the targets (in the enclosing navigation response) to which
    # the given region is bound. By opening the target, clients can implement one
    # form of navigation.
    self.targets = targets

    self.targetObjects = None

  def __str__(self):
    builder = []
    builder.append("[")
    builder.append("offset=")
    builder.append(str(self.offset) + ", ")
    builder.append("length=")
    builder.append(str(self.length) + ", ")
    builder.append("targets=")
    builder.append(", ".join(self.targets))
    builder.append("]")
    return "".join(builder)

  def containsInclusive(self, x):
    return self.offset <= x and x <= self.offset + self.length

  @staticmethod
  def fromJson(data):
    offset = data["offset"]
    length = data["length"]
    targets = data["targets"]
    return NavigationRegion(offset, length, targets);

  def toJson(self):
    return {
      "offset": self.offset,
      "length": self.length,
      "targets": self.targets,
    }

class NavigationTarget(object):
  """
  A description of a target to which the user can navigate.
  """

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

    self.file = None

  def __str__(self):
    builder = []
    builder.append("[")
    builder.append("kind=")
    builder.append(str(self.kind) + ", ")
    builder.append("fileIndex=")
    builder.append(str(self.fileIndex) + ", ")
    builder.append("offset=")
    builder.append(str(self.offset) + ", ")
    builder.append("length=")
    builder.append(str(self.length) + ", ")
    builder.append("startLine=")
    builder.append(str(self.startLine) + ", ")
    builder.append("startColumn=")
    builder.append(str(self.startColumn))
    builder.append("]")
    return "".join(builder)

  @staticmethod
  def fromJson(data):
    kind = data["kind"]
    fileIndex = data["fileIndex"]
    offset = data["offset"]
    length = data["length"]
    startLine = data["startLine"]
    startColumn = data["startColumn"]
    return NavigationTarget(kind, fileIndex, offset, length, startLine, startColumn);

  def toJson(self):
    return {
      "kind": self.kind,
      "fileIndex": self.fileIndex,
      "offset": self.offset,
      "length": self.length,
      "startLine": self.startLine,
      "startColumn": self.startColumn,
    }

class Occurrences(object):
  """
  A description of the references to a single element within a single file.
  """

  def __init__(self, element, offsets, length):
    # The element that was referenced.
    self.element = element

    # The offsets of the name of the referenced element within the file.
    self.offsets = offsets

    # The length of the name of the referenced element.
    self.length = length


  def __str__(self):
    builder = []
    builder.append("[")
    builder.append("element=")
    builder.append(str(self.element) + ", ")
    builder.append("offsets=")
    builder.append(", ".join(self.offsets) + ", ")
    builder.append("length=")
    builder.append(str(self.length))
    builder.append("]")
    return "".join(builder)

  def contains(self, x):
    for offset in self.offsets:
      if self.offset <= x and x < (self.offset + self.length):
        return True
    return False

  @staticmethod
  def fromJson(data):
    element = Element.fromJson(data["element"])
    offsets = data["offsets"]
    length = data["length"]
    return Occurrences(element, offsets, length);

  def toJson(self):
    return {
      "element": self.element.toJson(),
      "offsets": self.offsets,
      "length": self.length,
    }

class Outline(object):
  """
  An node in the outline structure of a file.
  """

  def __init__(self, parent, element, offset, length):
    self.parent = parent
    # A description of the element represented by this node.
    self.element = element

    # The offset of the first character of the element. This is different than
    # the offset in the Element, which if the offset of the name of the element.
    # It can be used, for example, to map locations in the file back to an
    # outline.
    self.offset = offset

    # The length of the element.
    self.length = length

    # The children of the node. The field will be omitted if the node has no
    # children.
    self.children = children


  def __str__(self):
    builder = []
    builder.append("[")
    builder.append("element=")
    builder.append(str(self.element) + ", ")
    builder.append("offset=")
    builder.append(str(self.offset) + ", ")
    builder.append("length=")
    builder.append(str(self.length) + ", ")
    builder.append("children=")
    builder.append(", ".join(self.children))
    builder.append("]")
    return "".join(builder)

  def containsInclusive(self, x):
    return self.offset <= x and x <= self.offset + self.length

  @staticmethod
  def from_json(parent, outlineObject):
    elObj = outlineObject["element"]
    el = Element.fromJson(elObj)
    offset = outlineObject["offset"]
    length = outlineObject["length"]

    outline = Outline(parent, element, offset, length)

    childrenList = []
    childrenArray = outlineObject["children"]
    if isinstance(childrenArray, list):
      childrenList = [self.fromJson(outline, item) for item in childrenArray]
    outline.setChildren(childrenList)
    return outline


  def getParent(self):
    return self.parent


  def setChildren(self, children):
    self.children = children


  def toJson(self):
    return {
      "element": self.element.toJson(),
      "offset": self.offset,
      "length": self.length,
      "children": [x.toJson() for x in self.children],
    }

class Override(object):
  """
  A description of a member that overrides an inherited member.
  """

  def __init__(self, offset, length, superclassMember, interfaceMembers):
    # The offset of the name of the overriding member.
    self.offset = offset

    # The length of the name of the overriding member.
    self.length = length

    # The member inherited from a superclass that is overridden by the overriding
    # member. The field is omitted if there is no superclass member, in which
    # case there must be at least one interface member.
    self.superclassMember = superclassMember

    # The members inherited from interfaces that are overridden by the overriding
    # member. The field is omitted if there are no interface members, in which
    # case there must be a superclass member.
    self.interfaceMembers = interfaceMembers


  def __str__(self):
    builder = []
    builder.append("[")
    builder.append("offset=")
    builder.append(str(self.offset) + ", ")
    builder.append("length=")
    builder.append(str(self.length) + ", ")
    builder.append("superclassMember=")
    builder.append(str(self.superclassMember) + ", ")
    builder.append("interfaceMembers=")
    builder.append(", ".join(self.interfaceMembers))
    builder.append("]")
    return "".join(builder)

  @staticmethod
  def fromJson(data):
    offset = data["offset"]
    length = data["length"]
    superclassMember = None if not data.get("superclassMember") else OverriddenMember.fromJson(data["superclassMember"])
    interfaceMembers = None if not data.get("interfaceMembers") else [OverriddenMember.fromJson(item) for item in data["interfaceMembers"]]
    return Override(offset, length, superclassMember, interfaceMembers);

  def toJson(self):
    return {
      "offset": self.offset,
      "length": self.length,
      "superclassMember": self.superclassMember.toJson(),
      "interfaceMembers": [x.toJson() for x in self.interfaceMembers],
    }

class OverriddenMember(object):
  """
  A description of a member that is being overridden.
  """

  def __init__(self, element, className):
    # The element that is being overridden.
    self.element = element

    # The name of the class in which the member is defined.
    self.className = className


  def __str__(self):
    builder = []
    builder.append("[")
    builder.append("element=")
    builder.append(str(self.element) + ", ")
    builder.append("className=")
    builder.append(str(self.className))
    builder.append("]")
    return "".join(builder)

  @staticmethod
  def fromJson(data):
    element = Element.fromJson(data["element"])
    className = data["className"]
    return OverriddenMember(element, className);

  def toJson(self):
    return {
      "element": self.element.toJson(),
      "className": self.className,
    }

class Position(object):
  """
  A position within a file.
  """

  def __init__(self, file, offset):
    # The file containing the position.
    self.file = file

    # The offset of the position.
    self.offset = offset


  def __str__(self):
    builder = []
    builder.append("[")
    builder.append("file=")
    builder.append(str(self.file) + ", ")
    builder.append("offset=")
    builder.append(str(self.offset))
    builder.append("]")
    return "".join(builder)

  @staticmethod
  def fromJson(data):
    file = data["file"]
    offset = data["offset"]
    return Position(file, offset);

  def toJson(self):
    return {
      "file": self.file,
      "offset": self.offset,
    }

class PubStatus(object):
  """
  An indication of the current state of pub execution.
  """

  def __init__(self, isListingPackageDirs):
    # True if the server is currently running pub to produce a list of package
    # directories.
    self.isListingPackageDirs = isListingPackageDirs


  def __str__(self):
    builder = []
    builder.append("[")
    builder.append("isListingPackageDirs=")
    builder.append(str(self.isListingPackageDirs))
    builder.append("]")
    return "".join(builder)

  @staticmethod
  def fromJson(data):
    isListingPackageDirs = data["isListingPackageDirs"]
    return PubStatus(isListingPackageDirs);

  def toJson(self):
    return {
      "isListingPackageDirs": self.isListingPackageDirs,
    }

class RefactoringKind:
  """
  An enumeration of the kinds of refactorings that can be created.
  """

  CONVERT_GETTER_TO_METHOD = "CONVERT_GETTER_TO_METHOD"

  CONVERT_METHOD_TO_GETTER = "CONVERT_METHOD_TO_GETTER"

  EXTRACT_LOCAL_VARIABLE = "EXTRACT_LOCAL_VARIABLE"

  EXTRACT_METHOD = "EXTRACT_METHOD"

  INLINE_LOCAL_VARIABLE = "INLINE_LOCAL_VARIABLE"

  INLINE_METHOD = "INLINE_METHOD"

  MOVE_FILE = "MOVE_FILE"

  RENAME = "RENAME"

  SORT_MEMBERS = "SORT_MEMBERS"

class RefactoringMethodParameter(object):
  """
  A description of a parameter in a method refactoring.
  """

  def __init__(self, item_id, kind, type, name, parameters):
    # The unique identifier of the parameter. Clients may omit this field for the
    # parameters they want to add.
    self.item_id = item_id

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


  def __str__(self):
    builder = []
    builder.append("[")
    builder.append("item_id=")
    builder.append(str(self.item_id) + ", ")
    builder.append("kind=")
    builder.append(str(self.kind) + ", ")
    builder.append("type=")
    builder.append(str(self.type) + ", ")
    builder.append("name=")
    builder.append(str(self.name) + ", ")
    builder.append("parameters=")
    builder.append(str(self.parameters))
    builder.append("]")
    return "".join(builder)

  @staticmethod
  def fromJson(data):
    item_id = None if not data.get("id") else data["id"]
    kind = data["kind"]
    type = data["type"]
    name = data["name"]
    parameters = None if not data.get("parameters") else data["parameters"]
    return RefactoringMethodParameter(item_id, kind, type, name, parameters);

  def toJson(self):
    return {
      "id": self.id,
      "kind": self.kind,
      "type": self.type,
      "name": self.name,
      "parameters": self.parameters,
    }

class RefactoringFeedback(object):
  """
  An abstract superclass of all refactoring feedbacks.
  """

  def __init__(self):
    pass

  def __str__(self):
    builder = []
    builder.append("[")
    builder.append("]")
    return "".join(builder)

  @staticmethod
  def fromJson(data):
    return RefactoringFeedback();

  def toJson(self):
    return {
    }

class RefactoringOptions(object):
  """
  An abstract superclass of all refactoring options.
  """

  def __init__(self):
    pass

  def __str__(self):
    builder = []
    builder.append("[")
    builder.append("]")
    return "".join(builder)

  @staticmethod
  def fromJson(data):
    return RefactoringOptions();

  def toJson(self):
    return {
    }

class RefactoringMethodParameterKind:
  """
  An enumeration of the kinds of parameters.
  """

  REQUIRED = "REQUIRED"

  POSITIONAL = "POSITIONAL"

  NAMED = "NAMED"

class RefactoringProblem(object):
  """
  A description of a problem related to a refactoring.
  """

  def __init__(self, severity, message, location):
    # The severity of the problem being represented.
    self.severity = severity

    # A human-readable description of the problem being represented.
    self.message = message

    # The location of the problem being represented. This field is omitted unless
    # there is a specific location associated with the problem (such as a
    # location where an element being renamed will be shadowed).
    self.location = location


  def __str__(self):
    builder = []
    builder.append("[")
    builder.append("severity=")
    builder.append(str(self.severity) + ", ")
    builder.append("message=")
    builder.append(str(self.message) + ", ")
    builder.append("location=")
    builder.append(str(self.location))
    builder.append("]")
    return "".join(builder)

  @staticmethod
  def fromJson(data):
    severity = data["severity"]
    message = data["message"]
    location = None if not data.get("location") else Location.fromJson(data["location"])
    return RefactoringProblem(severity, message, location);

  def toJson(self):
    return {
      "severity": self.severity,
      "message": self.message,
      "location": self.location.toJson(),
    }

class RefactoringProblemSeverity:
  """
  An enumeration of the severities of problems that can be returned by the
  refactoring requests.
  """

  INFO = "INFO"

  WARNING = "WARNING"

  ERROR = "ERROR"

  FATAL = "FATAL"

class RemoveContentOverlay(object):
  """
  A directive to remove an existing file content overlay. After processing this
  directive, the file contents will once again be read from the file system.

  If this directive is used on a file that doesn't currently have a content
  overlay, it has no effect.
  """

  def __init__(self):
    self.type = "remove"


  def __str__(self):
    builder = []
    builder.append("[")
    builder.append("type=")
    builder.append(str(self.type))
    builder.append("]")
    return "".join(builder)

  @staticmethod
  def fromJson(data):
    type = data["type"]
    return RemoveContentOverlay();

  def toJson(self):
    return {
      "type": self.type,
    }

class RequestError(object):
  """
  An indication of a problem with the execution of the server, typically in
  response to a request.
  """

  def __init__(self, code, message, stackTrace):
    # A code that uniquely identifies the error that occurred.
    self.code = code

    # A short description of the error.
    self.message = message

    # The stack trace associated with processing the request, used for debugging
    # the server.
    self.stackTrace = stackTrace


  def __str__(self):
    builder = []
    builder.append("[")
    builder.append("code=")
    builder.append(str(self.code) + ", ")
    builder.append("message=")
    builder.append(str(self.message) + ", ")
    builder.append("stackTrace=")
    builder.append(str(self.stackTrace))
    builder.append("]")
    return "".join(builder)

  @staticmethod
  def fromJson(data):
    code = data["code"]
    message = data["message"]
    stackTrace = None if not data.get("stackTrace") else data["stackTrace"]
    return RequestError(code, message, stackTrace);

  def toJson(self):
    return {
      "code": self.code,
      "message": self.message,
      "stackTrace": self.stackTrace,
    }

class RequestErrorCode:
  """
  An enumeration of the types of errors that can occur in the execution of the
  server.
  """

  # An "analysis.getErrors" or "analysis.getNavigation" request could not be
  # satisfied because the content of the file changed before the requested
  # results could be computed.
  CONTENT_MODIFIED = "CONTENT_MODIFIED"

  # An "edit.format" request specified a FilePath which does not match a Dart
  # file in an analysis root.
  FORMAT_INVALID_FILE = "FORMAT_INVALID_FILE"

  # An "analysis.getErrors" request specified a FilePath which does not match a
  # file currently subject to analysis.
  GET_ERRORS_INVALID_FILE = "GET_ERRORS_INVALID_FILE"

  # An analysis.updateContent request contained a ChangeContentOverlay object
  # which can't be applied, due to an edit having an offset or length that is out
  # of range.
  INVALID_OVERLAY_CHANGE = "INVALID_OVERLAY_CHANGE"

  # One of the method parameters was invalid.
  INVALID_PARAMETER = "INVALID_PARAMETER"

  # A malformed request was received.
  INVALID_REQUEST = "INVALID_REQUEST"

  # The analysis server has already been started (and hence won't accept new
  # connections).
  #
  # This error is included for future expansion; at present the analysis server
  # can only speak to one client at a time so this error will never occur.
  SERVER_ALREADY_STARTED = "SERVER_ALREADY_STARTED"

  # An internal error occurred in the analysis server. Also see the server.error
  # notification.
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

  # The analysis server was requested to perform an action which is not
  # supported.
  #
  # This is a legacy error; it will be removed before the API reaches version
  # 1.0.
  UNSUPPORTED_FEATURE = "UNSUPPORTED_FEATURE"

class SearchResult(object):
  """
  A single result from a search request.
  """

  def __init__(self, location, kind, isPotential, path):
    # The location of the code that matched the search criteria.
    self.location = location

    # The kind of element that was found or the kind of reference that was found.
    self.kind = kind

    # True if the result is a potential match but cannot be confirmed to be a
    # match. For example, if all references to a method m defined in some class
    # were requested, and a reference to a method m from an unknown class were
    # found, it would be marked as being a potential match.
    self.isPotential = isPotential

    # The elements that contain the result, starting with the most immediately
    # enclosing ancestor and ending with the library.
    self.path = path


  def __str__(self):
    builder = []
    builder.append("[")
    builder.append("location=")
    builder.append(str(self.location) + ", ")
    builder.append("kind=")
    builder.append(str(self.kind) + ", ")
    builder.append("isPotential=")
    builder.append(str(self.isPotential) + ", ")
    builder.append("path=")
    builder.append(", ".join(self.path))
    builder.append("]")
    return "".join(builder)

  @staticmethod
  def fromJson(data):
    location = Location.fromJson(data["location"])
    kind = data["kind"]
    isPotential = data["isPotential"]
    path = [Element.fromJson(item) for item in data["path"]]
    return SearchResult(location, kind, isPotential, path);

  def toJson(self):
    return {
      "location": self.location.toJson(),
      "kind": self.kind,
      "isPotential": self.isPotential,
      "path": [x.toJson() for x in self.path],
    }

class SearchResultKind:
  """
  An enumeration of the kinds of search results returned by the search domain.
  """

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

class ServerService:
  """
  An enumeration of the services provided by the server domain.
  """

  STATUS = "STATUS"

class SourceChange(object):
  """
  A description of a set of edits that implement a single conceptual change.
  """

  def __init__(self, message, edits, linkedEditGroups, selection):
    # A human-readable description of the change to be applied.
    self.message = message

    # A list of the edits used to effect the change, grouped by file.
    self.edits = edits

    # A list of the linked editing groups used to customize the changes that were
    # made.
    self.linkedEditGroups = linkedEditGroups

    # The position that should be selected after the edits have been applied.
    self.selection = selection


  def __str__(self):
    builder = []
    builder.append("[")
    builder.append("message=")
    builder.append(str(self.message) + ", ")
    builder.append("edits=")
    builder.append(", ".join(self.edits) + ", ")
    builder.append("linkedEditGroups=")
    builder.append(", ".join(self.linkedEditGroups) + ", ")
    builder.append("selection=")
    builder.append(str(self.selection))
    builder.append("]")
    return "".join(builder)

  @staticmethod
  def fromJson(data):
    message = data["message"]
    edits = [SourceFileEdit.fromJson(item) for item in data["edits"]]
    linkedEditGroups = [LinkedEditGroup.fromJson(item) for item in data["linkedEditGroups"]]
    selection = None if not data.get("selection") else Position.fromJson(data["selection"])
    return SourceChange(message, edits, linkedEditGroups, selection);

  def toJson(self):
    return {
      "message": self.message,
      "edits": [x.toJson() for x in self.edits],
      "linkedEditGroups": [x.toJson() for x in self.linkedEditGroups],
      "selection": self.selection.toJson(),
    }

class SourceEdit(object):
  """
  A description of a single change to a single file.
  """

  def __init__(self, offset, length, replacement, item_id):
    # The offset of the region to be modified.
    self.offset = offset

    # The length of the region to be modified.
    self.length = length

    # The code that is to replace the specified region in the original code.
    self.replacement = replacement

    # An identifier that uniquely identifies this source edit from other edits in
    # the same response. This field is omitted unless a containing structure
    # needs to be able to identify the edit for some reason.
    #
    # For example, some refactoring operations can produce edits that might not
    # be appropriate (referred to as potential edits). Such edits will have an id
    # so that they can be referenced. Edits in the same response that do not need
    # to be referenced will not have an id.
    self.item_id = item_id


  def __str__(self):
    builder = []
    builder.append("[")
    builder.append("offset=")
    builder.append(str(self.offset) + ", ")
    builder.append("length=")
    builder.append(str(self.length) + ", ")
    builder.append("replacement=")
    builder.append(str(self.replacement) + ", ")
    builder.append("item_id=")
    builder.append(str(self.item_id))
    builder.append("]")
    return "".join(builder)

  @staticmethod
  def fromJson(data):
    offset = data["offset"]
    length = data["length"]
    replacement = data["replacement"]
    item_id = None if not data.get("id") else data["id"]
    return SourceEdit(offset, length, replacement, item_id);

  def toJson(self):
    return {
      "offset": self.offset,
      "length": self.length,
      "replacement": self.replacement,
      "id": self.id,
    }

class SourceFileEdit(object):
  """
  A description of a set of changes to a single file.
  """

  def __init__(self, file, fileStamp, edits):
    # The file containing the code to be modified.
    self.file = file

    # The modification stamp of the file at the moment when the change was
    # created, in milliseconds since the "Unix epoch". Will be -1 if the file did
    # not exist and should be created. The client may use this field to make sure
    # that the file was not changed since then, so it is safe to apply the
    # change.
    self.fileStamp = fileStamp

    # A list of the edits used to effect the change.
    self.edits = edits


  def __str__(self):
    builder = []
    builder.append("[")
    builder.append("file=")
    builder.append(str(self.file) + ", ")
    builder.append("fileStamp=")
    builder.append(str(self.fileStamp) + ", ")
    builder.append("edits=")
    builder.append(", ".join(self.edits))
    builder.append("]")
    return "".join(builder)

  @staticmethod
  def fromJson(data):
    file = data["file"]
    fileStamp = data["fileStamp"]
    edits = [SourceEdit.fromJson(item) for item in data["edits"]]
    return SourceFileEdit(file, fileStamp, edits);

  def toJson(self):
    return {
      "file": self.file,
      "fileStamp": self.fileStamp,
      "edits": [x.toJson() for x in self.edits],
    }

class TypeHierarchyItem(object):
  """
  A representation of a class in a type hierarchy.
  """

  def __init__(self, classElement, displayName, memberElement, superclass, interfaces, mixins, subclasses):
    # The class element represented by this item.
    self.classElement = classElement

    # The name to be displayed for the class. This field will be omitted if the
    # display name is the same as the name of the element. The display name is
    # different if there is additional type information to be displayed, such as
    # type arguments.
    self.displayName = displayName

    # The member in the class corresponding to the member on which the hierarchy
    # was requested. This field will be omitted if the hierarchy was not
    # requested for a member or if the class does not have a corresponding
    # member.
    self.memberElement = memberElement

    # The index of the item representing the superclass of this class. This field
    # will be omitted if this item represents the class Object.
    self.superclass = superclass

    # The indexes of the items representing the interfaces implemented by this
    # class. The list will be empty if there are no implemented interfaces.
    self.interfaces = interfaces

    # The indexes of the items representing the mixins referenced by this class.
    # The list will be empty if there are no classes mixed in to this class.
    self.mixins = mixins

    # The indexes of the items representing the subtypes of this class. The list
    # will be empty if there are no subtypes or if this item represents a
    # supertype of the pivot type.
    self.subclasses = subclasses


  def __str__(self):
    builder = []
    builder.append("[")
    builder.append("classElement=")
    builder.append(str(self.classElement) + ", ")
    builder.append("displayName=")
    builder.append(str(self.displayName) + ", ")
    builder.append("memberElement=")
    builder.append(str(self.memberElement) + ", ")
    builder.append("superclass=")
    builder.append(str(self.superclass) + ", ")
    builder.append("interfaces=")
    builder.append(", ".join(self.interfaces) + ", ")
    builder.append("mixins=")
    builder.append(", ".join(self.mixins) + ", ")
    builder.append("subclasses=")
    builder.append(", ".join(self.subclasses))
    builder.append("]")
    return "".join(builder)

  @staticmethod
  def fromJson(data):
    classElement = Element.fromJson(data["classElement"])
    displayName = None if not data.get("displayName") else data["displayName"]
    memberElement = None if not data.get("memberElement") else Element.fromJson(data["memberElement"])
    superclass = None if not data.get("superclass") else data["superclass"]
    interfaces = data["interfaces"]
    mixins = data["mixins"]
    subclasses = data["subclasses"]
    return TypeHierarchyItem(classElement, displayName, memberElement, superclass, interfaces, mixins, subclasses);

  def getBestName(self):
    if not self.displayName:
      return self.classElement.getName()
    else:
      return self.displayName

  def toJson(self):
    return {
      "classElement": self.classElement.toJson(),
      "displayName": self.displayName,
      "memberElement": self.memberElement.toJson(),
      "superclass": self.superclass,
      "interfaces": self.interfaces,
      "mixins": self.mixins,
      "subclasses": self.subclasses,
    }

