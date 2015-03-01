// Copyright (c) 2015, <your name>. All rights reserved. Use of this source code
// is governed by a BSD-style license that can be found in the LICENSE file.

import 'dart:io';
import 'dart:convert';

import 'package:path/path.dart' as path;
import 'package:path_for_server/path_for_server.dart';

/// Represents the Sublime Text package project.
///
/// Used to find common locations for deployment of files.
class Environment {
  /// Path to the Sublime Text project' top-level directory.
  String root;

  /// Path to Sublime Text 3 Data directory.
  String pathToData;

  final String pathToGlobalConfig;
  final String pathToLocalConfig;
  final String pathToDataOnOSX;
  final String pathToDataOnLinux;

  /// Path to the Sublime Text Data/Packages/Dart directory.
  String get destination =>
      expand_variables(toWindowsPath(path.join(pathToData, 'Packages/Dart')));


  Environment(String root)
  :
    this.root = root,
    this.pathToGlobalConfig = r'~\package-dev.json',
    this.pathToLocalConfig = path.join(root, 'package-dev.json'),
    this.pathToDataOnOSX = '~/Library/Application Support/Sublime Text 3/',
    this.pathToDataOnLinux = '~/.config/sublime-text-3/'
  {
    // On Windows, we can't reliably find Data unless the user tells us.
    if (Platform.isWindows) {
      pathToData = loadFromConfig('pathToData', required: true);
    } else if (Platform.isMacOS) {
      pathToData = pathToDataOnOSX;
    } else {
      pathToData = pathToDataOnLinux;
    }
  }

  String toWindowsPath(String p) {
    if (!Platform.isWindows) return p;
    return p.replaceAll('/', '\\');
  }

  String loadFromConfig(key, {required: false}) {
    if (!Platform.isWindows) throw 'call only on Windows';

    var globalDataFile = new File(pathToGlobalConfig);
    var globalData = globalDataFile.existsSync() ?
        JSON.decode(globalDataFile.readAsStringSync()) :
        {};

    var localDataFile = new File(path.join(pathToLocalConfig));
    var localData = localDataFile.existsSync() ?
        JSON.decode(localDataFile.readAsStringSync()) :
        throw 'file package-dev.json required at "$root"';

    var data = globalData..addAll(localData);
    if (!data.containsKey(key) && required) throw 'key $key is required';

    return data[key];
  }
}