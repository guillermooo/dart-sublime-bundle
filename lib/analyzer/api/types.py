class AddContentOverlay(object):
    def __init__(self, data):
        self.data = data

    @property
    def type(self):
        return self.data["type"]

    @property
    def content(self):
        return self.data["content"]

class AnalysisError(object):
    def __init__(self, data):
        self.data = data

    @property
    def severity(self):
        return self.data["severity"]

    @property
    def type(self):
        return self.data["type"]

    @property
    def location(self):
        return self.data["location"]

    @property
    def message(self):
        return self.data["message"]

    @property
    def correction(self):
        return self.data["correction"]

class AnalysisErrorFixes(object):
    def __init__(self, data):
        self.data = data

    @property
    def error(self):
        return self.data["error"]

    @property
    def fixes(self):
        return self.data["fixes"]

class AnalysisErrorSeverity(object):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"

class AnalysisErrorType(object):
    ANGULAR = "ANGULAR"
    CHECKED_MODE_COMPILE_TIME_ERROR = "CHECKED_MODE_COMPILE_TIME_ERROR"
    COMPILE_TIME_ERROR = "COMPILE_TIME_ERROR"
    HINT = "HINT"
    POLYMER = "POLYMER"
    STATIC_TYPE_WARNING = "STATIC_TYPE_WARNING"
    STATIC_WARNING = "STATIC_WARNING"
    SYNTACTIC_ERROR = "SYNTACTIC_ERROR"
    TODO = "TODO"

class AnalysisOptions(object):
    def __init__(self, data):
        self.data = data

    @property
    def enableAsync(self):
        return self.data["enableAsync"]

    @property
    def enableDeferredLoading(self):
        return self.data["enableDeferredLoading"]

    @property
    def enableEnums(self):
        return self.data["enableEnums"]

    @property
    def generateDart2jsHints(self):
        return self.data["generateDart2jsHints"]

    @property
    def generateHints(self):
        return self.data["generateHints"]

class AnalysisService(object):
    FOLDING = "FOLDING"
    HIGHLIGHTS = "HIGHLIGHTS"
    NAVIGATION = "NAVIGATION"
    OCCURRENCES = "OCCURRENCES"
    OUTLINE = "OUTLINE"
    OVERRIDES = "OVERRIDES"

class AnalysisStatus(object):
    def __init__(self, data):
        self.data = data

    @property
    def isAnalyzing(self):
        return self.data["isAnalyzing"]

    @property
    def analysisTarget(self):
        return self.data["analysisTarget"]

class ChangeContentOverlay(object):
    def __init__(self, data):
        self.data = data

    @property
    def type(self):
        return self.data["type"]

    @property
    def edits(self):
        return self.data["edits"]

class CompletionRelevance(object):
    LOW = "LOW"
    DEFAULT = "DEFAULT"
    HIGH = "HIGH"

class CompletionSuggestion(object):
    def __init__(self, data):
        self.data = data

    @property
    def kind(self):
        return self.data["kind"]

    @property
    def relevance(self):
        return self.data["relevance"]

    @property
    def completion(self):
        return self.data["completion"]

    @property
    def selectionOffset(self):
        return self.data["selectionOffset"]

    @property
    def selectionLength(self):
        return self.data["selectionLength"]

    @property
    def isDeprecated(self):
        return self.data["isDeprecated"]

    @property
    def isPotential(self):
        return self.data["isPotential"]

    @property
    def docSummary(self):
        return self.data["docSummary"]

    @property
    def docComplete(self):
        return self.data["docComplete"]

    @property
    def declaringType(self):
        return self.data["declaringType"]

    @property
    def element(self):
        return self.data["element"]

    @property
    def returnType(self):
        return self.data["returnType"]

    @property
    def parameterNames(self):
        return self.data["parameterNames"]

    @property
    def parameterTypes(self):
        return self.data["parameterTypes"]

    @property
    def requiredParameterCount(self):
        return self.data["requiredParameterCount"]

    @property
    def positionalParameterCount(self):
        return self.data["positionalParameterCount"]

    @property
    def parameterName(self):
        return self.data["parameterName"]

    @property
    def parameterType(self):
        return self.data["parameterType"]

class CompletionSuggestionKind(object):
    ARGUMENT_LIST = "ARGUMENT_LIST"
    IMPORT = "IMPORT"
    IDENTIFIER = "IDENTIFIER"
    INVOCATION = "INVOCATION"
    KEYWORD = "KEYWORD"
    NAMED_ARGUMENT = "NAMED_ARGUMENT"
    OPTIONAL_ARGUMENT = "OPTIONAL_ARGUMENT"
    PARAMETER = "PARAMETER"

class Element(object):
    def __init__(self, data):
        self.data = data

    @property
    def kind(self):
        return self.data["kind"]

    @property
    def name(self):
        return self.data["name"]

    @property
    def location(self):
        return self.data["location"]

    @property
    def flags(self):
        return self.data["flags"]

    @property
    def parameters(self):
        return self.data["parameters"]

    @property
    def returnType(self):
        return self.data["returnType"]

class ElementKind(object):
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
    def __init__(self, data):
        self.data = data

    @property
    def file(self):
        return self.data["file"]

    @property
    def kind(self):
        return self.data["kind"]

class ExecutableKind(object):
    CLIENT = "CLIENT"
    EITHER = "EITHER"
    NOT_EXECUTABLE = "NOT_EXECUTABLE"
    SERVER = "SERVER"

class ExecutionService(object):
    LAUNCH_DATA = "LAUNCH_DATA"

class FoldingKind(object):
    COMMENT = "COMMENT"
    CLASS_MEMBER = "CLASS_MEMBER"
    DIRECTIVES = "DIRECTIVES"
    DOCUMENTATION_COMMENT = "DOCUMENTATION_COMMENT"
    TOP_LEVEL_DECLARATION = "TOP_LEVEL_DECLARATION"

class FoldingRegion(object):
    def __init__(self, data):
        self.data = data

    @property
    def kind(self):
        return self.data["kind"]

    @property
    def offset(self):
        return self.data["offset"]

    @property
    def length(self):
        return self.data["length"]

class HighlightRegion(object):
    def __init__(self, data):
        self.data = data

    @property
    def type(self):
        return self.data["type"]

    @property
    def offset(self):
        return self.data["offset"]

    @property
    def length(self):
        return self.data["length"]

class HighlightRegionType(object):
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
    def __init__(self, data):
        self.data = data

    @property
    def offset(self):
        return self.data["offset"]

    @property
    def length(self):
        return self.data["length"]

    @property
    def containingLibraryPath(self):
        return self.data["containingLibraryPath"]

    @property
    def containingLibraryName(self):
        return self.data["containingLibraryName"]

    @property
    def dartdoc(self):
        return self.data["dartdoc"]

    @property
    def elementDescription(self):
        return self.data["elementDescription"]

    @property
    def elementKind(self):
        return self.data["elementKind"]

    @property
    def parameter(self):
        return self.data["parameter"]

    @property
    def propagatedType(self):
        return self.data["propagatedType"]

    @property
    def staticType(self):
        return self.data["staticType"]

class LinkedEditGroup(object):
    def __init__(self, data):
        self.data = data

    @property
    def positions(self):
        return self.data["positions"]

    @property
    def length(self):
        return self.data["length"]

    @property
    def suggestions(self):
        return self.data["suggestions"]

class LinkedEditSuggestion(object):
    def __init__(self, data):
        self.data = data

    @property
    def value(self):
        return self.data["value"]

    @property
    def kind(self):
        return self.data["kind"]

class LinkedEditSuggestionKind(object):
    METHOD = "METHOD"
    PARAMETER = "PARAMETER"
    TYPE = "TYPE"
    VARIABLE = "VARIABLE"

class Location(object):
    def __init__(self, data):
        self.data = data

    @property
    def file(self):
        return self.data["file"]

    @property
    def offset(self):
        return self.data["offset"]

    @property
    def length(self):
        return self.data["length"]

    @property
    def startLine(self):
        return self.data["startLine"]

    @property
    def startColumn(self):
        return self.data["startColumn"]

class NavigationRegion(object):
    def __init__(self, data):
        self.data = data

    @property
    def offset(self):
        return self.data["offset"]

    @property
    def length(self):
        return self.data["length"]

    @property
    def targets(self):
        return self.data["targets"]

class Occurrences(object):
    def __init__(self, data):
        self.data = data

    @property
    def element(self):
        return self.data["element"]

    @property
    def offsets(self):
        return self.data["offsets"]

    @property
    def length(self):
        return self.data["length"]

class Outline(object):
    def __init__(self, data):
        self.data = data

    @property
    def element(self):
        return self.data["element"]

    @property
    def offset(self):
        return self.data["offset"]

    @property
    def length(self):
        return self.data["length"]

    @property
    def children(self):
        return self.data["children"]

class Override(object):
    def __init__(self, data):
        self.data = data

    @property
    def offset(self):
        return self.data["offset"]

    @property
    def length(self):
        return self.data["length"]

    @property
    def superclassMember(self):
        return self.data["superclassMember"]

    @property
    def interfaceMembers(self):
        return self.data["interfaceMembers"]

class OverriddenMember(object):
    def __init__(self, data):
        self.data = data

    @property
    def element(self):
        return self.data["element"]

    @property
    def className(self):
        return self.data["className"]

class Position(object):
    def __init__(self, data):
        self.data = data

    @property
    def file(self):
        return self.data["file"]

    @property
    def offset(self):
        return self.data["offset"]

class RefactoringKind(object):
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
    def __init__(self, data):
        self.data = data

    @property
    def id(self):
        return self.data["id"]

    @property
    def kind(self):
        return self.data["kind"]

    @property
    def type(self):
        return self.data["type"]

    @property
    def name(self):
        return self.data["name"]

    @property
    def parameters(self):
        return self.data["parameters"]

class RefactoringFeedback(object):
    def __init__(self, data):
        self.data = data

class RefactoringOptions(object):
    def __init__(self, data):
        self.data = data

class RefactoringMethodParameterKind(object):
    REQUIRED = "REQUIRED"
    POSITIONAL = "POSITIONAL"
    NAMED = "NAMED"

class RefactoringProblem(object):
    def __init__(self, data):
        self.data = data

    @property
    def severity(self):
        return self.data["severity"]

    @property
    def message(self):
        return self.data["message"]

    @property
    def location(self):
        return self.data["location"]

class RefactoringProblemSeverity(object):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    FATAL = "FATAL"

class RemoveContentOverlay(object):
    def __init__(self, data):
        self.data = data

    @property
    def type(self):
        return self.data["type"]

class RequestError(object):
    def __init__(self, data):
        self.data = data

    @property
    def code(self):
        return self.data["code"]

    @property
    def message(self):
        return self.data["message"]

    @property
    def stackTrace(self):
        return self.data["stackTrace"]

class RequestErrorCode(object):
    GET_ERRORS_INVALID_FILE = "GET_ERRORS_INVALID_FILE"
    INVALID_OVERLAY_CHANGE = "INVALID_OVERLAY_CHANGE"
    INVALID_PARAMETER = "INVALID_PARAMETER"
    INVALID_REQUEST = "INVALID_REQUEST"
    SERVER_ALREADY_STARTED = "SERVER_ALREADY_STARTED"
    SERVER_ERROR = "SERVER_ERROR"
    SORT_MEMBERS_INVALID_FILE = "SORT_MEMBERS_INVALID_FILE"
    SORT_MEMBERS_PARSE_ERRORS = "SORT_MEMBERS_PARSE_ERRORS"
    UNANALYZED_PRIORITY_FILES = "UNANALYZED_PRIORITY_FILES"
    UNKNOWN_REQUEST = "UNKNOWN_REQUEST"
    UNSUPPORTED_FEATURE = "UNSUPPORTED_FEATURE"

class SearchResult(object):
    def __init__(self, data):
        self.data = data

    @property
    def location(self):
        return self.data["location"]

    @property
    def kind(self):
        return self.data["kind"]

    @property
    def isPotential(self):
        return self.data["isPotential"]

    @property
    def path(self):
        return self.data["path"]

class SearchResultKind(object):
    DECLARATION = "DECLARATION"
    INVOCATION = "INVOCATION"
    READ = "READ"
    READ_WRITE = "READ_WRITE"
    REFERENCE = "REFERENCE"
    UNKNOWN = "UNKNOWN"
    WRITE = "WRITE"

class ServerService(object):
    STATUS = "STATUS"

class SourceChange(object):
    def __init__(self, data):
        self.data = data

    @property
    def message(self):
        return self.data["message"]

    @property
    def edits(self):
        return self.data["edits"]

    @property
    def linkedEditGroups(self):
        return self.data["linkedEditGroups"]

    @property
    def selection(self):
        return self.data["selection"]

class SourceEdit(object):
    def __init__(self, data):
        self.data = data

    @property
    def offset(self):
        return self.data["offset"]

    @property
    def length(self):
        return self.data["length"]

    @property
    def replacement(self):
        return self.data["replacement"]

    @property
    def id(self):
        return self.data["id"]

class SourceFileEdit(object):
    def __init__(self, data):
        self.data = data

    @property
    def file(self):
        return self.data["file"]

    @property
    def fileStamp(self):
        return self.data["fileStamp"]

    @property
    def edits(self):
        return self.data["edits"]

class TypeHierarchyItem(object):
    def __init__(self, data):
        self.data = data

    @property
    def classElement(self):
        return self.data["classElement"]

    @property
    def displayName(self):
        return self.data["displayName"]

    @property
    def memberElement(self):
        return self.data["memberElement"]

    @property
    def superclass(self):
        return self.data["superclass"]

    @property
    def interfaces(self):
        return self.data["interfaces"]

    @property
    def mixins(self):
        return self.data["mixins"]

    @property
    def subclasses(self):
        return self.data["subclasses"]

