// Copyright (c) 2015, <your name>. All rights reserved. Use of this source code
// is governed by a BSD-style license that can be found in the LICENSE file.

import 'dart:io';
import 'dart:async';

import 'package:glob/glob.dart';
import '../lib/environment.dart';

// top-level
final Glob pythonFiles = new Glob('*.py');
final Glob authorsFile = new Glob('AUTHORS');
final Glob changelogFile = new Glob('CHANGES.txt');
final Glob readmeFile = new Glob('README.md');
final Glob tmLanguageFiles = new Glob('*.tmLanguage');

// subdirs
final Glob gutterDirectory = new Glob('gutter/**');
final Glob libDirectory = new Glob('lib/**');
final Glob outthereDirectory = new Glob('out_there/**');
final Glob snippetsDirectory = new Glob('Snippets/**');
final Glob sublimepluginDirectory = new Glob('sublime_plugin_lib/**');
final Glob supportDirectory = new Glob('Support/**');

List<Glob> included = [
    pythonFiles,
    authorsFile,
    changelogFile,
    readmeFile,
    tmLanguageFiles,
    gutterDirectory,
    libDirectory,
    outthereDirectory,
    sublimepluginDirectory,
    supportDirectory
    ];

class Manifest {

  List<Glob> _globs;
  StreamController<FileSystemEntity> _controller;

  Map<Stream<FileSystemEntity>, StreamSubscription<FileSystemEntity>>
      _subscriptions;

  Environment _environment;

  Manifest(this._globs, this._environment)
      : _subscriptions = {},
        _controller = new StreamController<FileSystemEntity>();

  void close() {
    for (var subscription in _subscriptions.values) {
      subscription.cancel();
    }
    _subscriptions.clear();
    _controller.close();
  }

  void remove(stream) {
    var subscription = _subscriptions.remove(stream);
    if (subscription != null) subscription.cancel();
    if (_subscriptions.isEmpty) close();
  }

  void add(Stream<FileSystemEntity> stream) {
    if (_subscriptions.containsKey(stream)) return;
    _subscriptions[stream] = stream.listen(
        _controller.add,
        onError: _controller.addError,
        onDone: () => remove(stream));
  }

  Stream<FileSystemEntity> list() {
    for (var glob in _globs) {
      add(glob.list(root: _environment.root));
    }
    return _controller.stream;
  }
}
