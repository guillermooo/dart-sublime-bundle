import 'dart:io';

import 'package:grinder/grinder.dart';

import '../bin/main.dart';
import '../bin/perform_checks.dart';

// TODO(guillermooo): use grinder "decorators".
main([List<String> args]) {
  task('check', check);
  task('deploy', do_deploy);
  task('release', null, ['check', 'deploy']);
  startGrinder(args);
}

void check(GrinderContext context) {
  if (!checkLoggingLevelIsError()) {
    var msg =
        'ERROR: wrong logging level used for release\n'
        '    check: $loggerLevelFile';
    context.fail(msg);
  }
}

void do_deploy(GrinderContext context) {
  deploy();
}
