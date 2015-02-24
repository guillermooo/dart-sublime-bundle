// Copyright (c) 2015, <your name>. All rights reserved. Use of this source code
// is governed by a BSD-style license that can be found in the LICENSE file.

library sublime_dart_plugin_tools;

import 'package:path/path.dart' as path;

import 'dart:io';

import 'manifest.dart';
import '../lib/environment.dart';

/// Returns the path to the project's top-level directory.
String get topLevel {
  var scriptRoot = path.dirname(Platform.script.toFilePath());
  return path.absolute(path.normalize(path.join(scriptRoot, '../../..')));
}

File copySync(File source, File destination) {
  destination.createSync(recursive: true);
  return source.copySync(destination.path);
}

int deploy() {
  var environment = new Environment(topLevel);

  try {
    var directory = new Directory(environment.destination);
    if (directory.existsSync()) directory.deleteSync(recursive: true);
    directory.createSync();
  } catch (Exception) {
    print(
        'cannot delete/create destination directory: ${environment.destination}');
    return 1;
  }

  var manifest = new Manifest(included, environment);
  manifest.list().where((entity) => entity is File).forEach((source) {
    var relative = path.relative(source.path, from: environment.root);
    var destination = new File(path.join(environment.destination, relative));
    print('  ${source.path}');
    copySync(source, destination);
  });

  return 0;
}

int main() {
  var environment = new Environment(topLevel);
  print('''Copying files
  from: ${environment.root}
  to: ${environment.destination}
...''');
  return deploy();
}
