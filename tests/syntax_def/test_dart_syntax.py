# Copyright (c) 2014, Guillermo L?ez-Anglada. Please see the AUTHORS file for details.
# All rights reserved. Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.)

from Dart.tests import DartSyntaxTestCase


class Test_DartSyntax_Comments(DartSyntaxTestCase):
    def testInLineCommentTripleSlash(self):
        self.append('''
/// foobar
0123456789
''')
        scope = self.getNarrowestScopeNameAtRowCol(1, 3)
        self.assertEqual(scope, 'comment.line.triple-slash.dart')

    def testInLineCommentDoubleSlash(self):
        self.append('''
// foobar
0123456789
''')
        scope = self.getNarrowestScopeNameAtRowCol(1, 3)
        self.assertEqual(scope, 'comment.line.double-slash.dart')

    def testCommentBlock(self):
        self.append('''
/** foobar
0123456789
''')
        scope = self.getNarrowestScopeNameAtRowCol(1, 3)
        self.assertEqual(scope, 'comment.block.dart')

    def testCommentBlockCanEnd(self):
        self.append('''
/**
 * foobar
**/ 100
0123456789
''')
        scope = self.getNarrowestScopeNameAtRowCol(3, 3)
        self.assertEqual(scope, 'source.dart')


class Test_DartSyntax_Doc_Comments(DartSyntaxTestCase):
    def testDetectsLinkNames(self):
        self.append('''
/// check [this](out)
0123456789
          0123456789
''')
        scope = self.getNarrowestScopeNameAtRowCol(1, 11)
        self.assertEqual(scope, 'string.other.link.title.dart-doccomments')

    def testDetectsItalics(self):
        self.append('''
/// check *this* out
0123456789
          0123456789
''')
        scope = self.getNarrowestScopeNameAtRowCol(1, 11)
        self.assertEqual(scope, 'markup.italic.dart-doccomments')
