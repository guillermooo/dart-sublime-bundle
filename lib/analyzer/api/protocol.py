# Copyright (c) 2014, the Dart project authors.  Please see the AUTHORS file
# for details. All rights reserved. Use of this source code is governed by a
# BSD-style license that can be found in the LICENSE file.
#
# This file has been automatically generated.  Please do not edit it manually.
# To regenerate the file, use the script
# "pkg/analysis_server/tool/spec/generate_files".

from .base import *
import json


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
    result["location"] = Location.to_json()
    result["message"] = self.message
    if self.correction:
      result["correction"] = self.correction
    return result

  def __str__(self):
    return json.dumps(self.to_json())


