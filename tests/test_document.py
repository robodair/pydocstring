"""Tests for document module"""
import unittest
import os
import re

from pydocstring import document

FIND_DECL_FILE = os.path.join(os.path.dirname(
    __file__), "resources", "find_declarations.py")


class TestDocument(unittest.TestCase):
    """Test functionality of the Document class"""

    def test_find_all(self):
        """Test the ranges returned by a find_all call are correct"""
        match_re = r"a+"
        expected = [
            (0, 11),
            (35, 39)
        ]
        test_source = \
            """aaaaaaaaaaa
nothing
more nothing
  aaaa
"""
        doc = document.Document(test_source)
        matches = doc.find_all(match_re)
        self.assertEqual(matches, expected)

    def test_find_all_multiline(self):
        """Test the ranges returned by a find_all call are correct, multiple lines"""
        match_re = r"a+\s*?a+"
        expected = [
            (0, 14),
            (38, 42)
        ]
        test_source = \
            """aaaaaaaaaaa
aa
nothing
more nothing
  aaaa
"""
        doc = document.Document(test_source)
        matches = doc.find_all(match_re)
        self.assertEqual(matches, expected)

    def test_find_all_real_file(self):
        """Test finding all declarations in a real file"""
        expected = [
            (16, 34),
            (66, 92),
            (121, 138),
            (167, 190),
            (201, 237),
            (315, 342),
            (377, 426),
            (480, 505),
            (559, 645),
            (726, 801),
            (866, 950),
            (1016, 1101),
            (1143, 1186),
            (1237, 1272),
            (1317, 1341)
        ]

        with open(FIND_DECL_FILE) as content_file:
            source = content_file.read()

        matches = document.Document(source).find_all(document.ALL_DECL_RE,
                                                     flags=re.MULTILINE)
        self.assertEqual(matches, expected)

    def test_find_declarations(self):
        """Test finding declarations in a real file, excluding inside comments and strings"""
        expected = [
            (16, 34),
            (66, 92),
            (121, 138),
            (167, 190),
            (201, 237),
            (315, 342),
            (377, 426),
            # (480, 505), Not the match in a string, and regex avoids
            # the declaration in the comment anyway (only whitespace before the
            # decl allowed)
            (559, 645),
            (726, 801),
            (866, 950),
            (1016, 1101),
            (1143, 1186),
            (1237, 1272),
            (1317, 1341)
        ]

        with open(FIND_DECL_FILE) as content_file:
            source = content_file.read()
        doc = document.Document(source)
        matches = doc.find_all_declarations()

        self.assertEqual(matches, expected)

    def test_find_preceeding_start(self):
        """Test preceeding declaration returns None at the start of the file"""
        with open(FIND_DECL_FILE) as content_file:
            source = content_file.read()
        doc = document.Document(source, position=0)
        preceeding = doc.find_preceeding_declaration()
        self.assertEqual(preceeding, None)

    def test_find_preceeding_middle_after(self):
        """Test preceeding declaration correct in the middle of the file, after a declaration"""
        with open(FIND_DECL_FILE) as content_file:
            source = content_file.read()
        doc = document.Document(source, position=650)
        preceeding = doc.find_preceeding_declaration()
        self.assertEqual(preceeding, (559, 645))

    def test_find_preceeding_middle_inside(self):
        """Test preceeding declaration correct in the middle of the file, inside a declaration"""
        with open(FIND_DECL_FILE) as content_file:
            source = content_file.read()
        doc = document.Document(source, position=600)
        preceeding = doc.find_preceeding_declaration()
        self.assertEqual(preceeding, (559, 645))

    def test_find_next_start(self):
        """Test next declaration returns None at the end of the file"""
        with open(FIND_DECL_FILE) as content_file:
            source = content_file.read()
        doc = document.Document(source, position=len(source))
        nxt = doc.find_next_declaration()
        self.assertEqual(nxt, None)

    def test_find_next_middle_after(self):
        """Test next declaration correct in the middle of the file, after a declaration"""
        with open(FIND_DECL_FILE) as content_file:
            source = content_file.read()
        doc = document.Document(source, position=650)
        nxt = doc.find_next_declaration()
        self.assertEqual(nxt, (726, 801))

    def test_find_next_middle_inside(self):
        """Test next declaration correct in the middle of the file, inside a declaration"""
        with open(FIND_DECL_FILE) as content_file:
            source = content_file.read()
        doc = document.Document(source, position=600)
        nxt = doc.find_next_declaration()
        self.assertEqual(nxt, (726, 801))

    def test_get_block_middle(self):
        """Test getting the block the cursor is currently in"""
        with open(FIND_DECL_FILE) as content_file:
            source = content_file.read()
        doc = document.Document(source, position=600)
        block = doc.get_block()

        expected = \
            '''def method_ag_kw_normal(p1, p2, ls=[1], st="string", tup=(1, 2), di={"key", "value"}):
    pass

# method with keyword args of all types (no spaces) and single quotes
'''
        self.assertEqual(doc.get_range(*block), expected)

    def test_get_block_end(self):
        """Test getting the block the cursor is currently in, last method in the file"""
        with open(FIND_DECL_FILE) as content_file:
            source = content_file.read()
        doc = document.Document(source, position=1342)
        block = doc.get_block()

        expected = \
            '''def comment_following(): # comment
    pass
'''
        self.assertEqual(doc.get_range(*block), expected)
