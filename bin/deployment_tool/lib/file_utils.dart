// Copyright (c) 2015, <your name>. All rights reserved. Use of this source code
// is governed by a BSD-style license that can be found in the LICENSE file.

import 'dart:io';

import 'package:path/path.dart' as path;

final RegExp unixEnvironmentVariable = new RegExp(r'^\$.*$');
final RegExp windowsEnvironmentVariable = new RegExp(r'^%.*%$');
final RegExp variableNameRegExp = new RegExp(r'^[\$%](.*?)%?$');

/// Expands environment variables in [filePath].
///
/// On Windows, $NAME as well as %NAME% variables will be expanded.
/// The '~' symbol will also be expanded on all platforms.
String expand_variables(String filePath) {
  assert(filePath != null);
  var segments = path.split(filePath);
  var expanded = [];

  for (var segment in segments) {
    if (unixEnvironmentVariable.hasMatch(segment) ||
        Platform.isWindows && windowsEnvironmentVariable.hasMatch(segment)) {
      var name = variableNameRegExp.allMatches(segment).toList()[0].group(1);
      var value = Platform.environment[name];
      expanded.add(value != null ? value : '');
    } else {
      expanded.add(segment);
    }
  }

  if (expanded[0] == '~') expanded[0] = Platform.environment['HOME'];

  return path.normalize(expanded.join(path.separator));
}
