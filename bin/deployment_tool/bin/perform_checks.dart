
library sublime_dart_plugin_tools.checks;

import 'package:path/path.dart' as path;

import 'dart:io';

import '../lib/environment.dart';
import './main.dart';


String get loggerLevelFile {
  var where = path.join(topLevel, 'sublime_plugin_lib/__init__.py');
  return path.normalize(where);
}

bool checkLoggingLevelIsError() {
  var file = new File(loggerLevelFile);
  var regex = new RegExp(r'setLevel\(logging\.ERROR\)');
  return regex.hasMatch(file.readAsStringSync());
}

main() {
  print ('performing checks...');
  
  if (!checkLoggingLevelIsError()) {
    print ('ERROR: wrong logging level used for release');
    print ('    check: $loggerLevelFile');
    exit(1);
  }
}

