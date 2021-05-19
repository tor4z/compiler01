import unittest2
import os
from lex.lex import Lex

from utils import doc_cmp


class LexTest(unittest2.TestCase):
    def _test_case(self, lex_in, lex_out, lex_gen):
        Lex.generate(lex_in, lex_gen)

        with open(lex_out, 'r') as f:
            doc_out = f.read()
        with open(lex_gen, 'r') as f:
            doc_gen = f.read()
 
        self.assertTrue(doc_cmp(doc_out, doc_gen))
        os.remove(lex_gen)

    def test_lex(self):
        lex_in = './data/lex_test1.in'
        lex_out = './data/lex_test1.out'
        lex_gen = './data/lex_test1.gen'
        self._test_case(lex_in, lex_out, lex_gen)

        lex_in = './data/lex_test2.in'
        lex_out = './data/lex_test2.out'
        lex_gen = './data/lex_test2.gen'
        self._test_case(lex_in, lex_out, lex_gen)

        lex_in = './data/lex_test3.in'
        lex_out = './data/lex_test3.out'
        lex_gen = './data/lex_test3.gen'
        self._test_case(lex_in, lex_out, lex_gen)

        lex_in = './data/lex_test4.in'
        lex_out = './data/lex_test4.out'
        lex_gen = './data/lex_test4.gen'
        self._test_case(lex_in, lex_out, lex_gen)
