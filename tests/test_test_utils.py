import unittest2
from utils import line_split, line_cmp, doc_cmp


doc1 = """hello
world
!
"""

doc2 = """

hello

world
!

"""

doc3 = """hello
my
world
!
"""

doc4 = """hello
!
world
"""

doc5 = """
hello world !

who is you dady ?

"""

doc6 = """          hello  world  !
          who is  you dady  ?
"""

doc7 = """          hello  w orld  !
          who is  you dady  ?
"""


class TestUtils(unittest2.TestCase):
    def test_line_split(self):
        lines = line_split(doc1)
        self.assertEqual(len(lines), 3)

        lines = line_split(doc2)
        self.assertEqual(len(lines), 3)

        lines = line_split(doc3)
        self.assertEqual(len(lines), 4)

    def test_line_cmp(self):
        line0 = 'HELLO world !   '
        line1 = 'hello world !   '
        line2 = '  hello    world !'
        line3 = 'hello1 world !   '

        self.assertFalse(line_cmp(line0, line1))
        self.assertTrue(line_cmp(line1, line2))
        self.assertFalse(line_cmp(line2, line3))

    def test_doc_cmp(self):
        self.assertTrue(doc_cmp(doc1, doc2))
        self.assertFalse(doc_cmp(doc2, doc3))
        self.assertFalse(doc_cmp(doc1, doc4))

        self.assertTrue(doc_cmp(doc5, doc6))
        self.assertFalse(doc_cmp(doc5, doc7))
