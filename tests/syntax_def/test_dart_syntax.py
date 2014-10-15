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
