"""Responses from the analyzer.
"""

import sublime


class StatusInfo(object):
    def __init__(self, data):
        self.data = data

    @property
    def is_analyzing(self):
        return self.data['params']['analysis']['analyzing']

    @property
    def message(self):
        if self.is_analyzing:
            return "Analysis started"
        return "Analysis finished"


class ErrorInfoCollection(object):
    def __init__(self, data):
        self.data = data
        self._errors = []
        self._warnings = []

    def errors_to_regions(self):
        for ei in self.errors:
            yield ei.to_region()

    def warnings_to_regions(self):
        for ei in self.warnings:
            yield ei.to_region()

    @property
    def errors(self):
        if self._errors:
            yield from self._errors

        for err in  self.data['params']['errors']:
            ei = ErrorInfo(err)
            if ei.severity == 'ERROR':
                self._errors.append(ei)
                yield ei
            elif ei.severity == 'WARNING':
                self._warnings.append(ei)

    @property
    def warnings(self):
        if self._warnings:
            yield from self._warnings

        for err in  self.data['params']['errors']:
            ei = ErrorInfo(err)
            if ei.severity == 'WARNING':
                self._warnings.append(ei)
                yield ei
            elif ei.severity == 'ERROR':
                self._errors.append(ei)



class ErrorInfo(object):
    def __init__(self, data):
        self.data = data

    def __str__(self):
        return "{self.severity}:{self.type}:{self.file}:{self.start_line}:{self.start_column}".format(self=self)

    @property
    def location(self):
        self.data['location']

    @property
    def severity(self):
        return self.data['severity']

    @property
    def type(self):
        return self.data['type']

    @property
    def file(self):
        return self.data['location']['file']

    @property
    def offset(self):
        return self.data['location']['offset'] - 1

    @property
    def length(self):
        return self.data['location']['length']

    @property
    def start_line(self):
        return self.data['location']['startLine']

    @property
    def start_column(self):
        return self.data['location']['startColumn']

    @property
    def message(self):
        return self.data['message']

    def to_region(self):
        return sublime.Region(self.offset, self.offset + self.length)


class Response(object):
    def __init__(self, data):
        self.data = data

    @property
    def type(self):
        return self.data.get('event', '<unknown>')

    @property
    def has_errors(self):
        return (self.data.get('event') == 'analysis.errors' and
            len(self.data['params']['errors']) > 0)

    @property
    def errors(self):
        if self.has_errors:
            return ErrorInfoCollection(self.data)

    @property
    def has_status(self):
        if self.data.get('event') == 'server.status':
            return True

    @property
    def status(self):
         if self.has_status:
            return StatusInfo(self.data)
