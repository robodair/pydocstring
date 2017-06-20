"""Tests for document module"""
import unittest
import os
import re

from .. import document

FIND_DECL_FILE = os.path.join(os.path.dirname(__file__), "resources", "find_declarations.py")

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
            (1317, 1343)
        ]

        with open(FIND_DECL_FILE) as content_file:
            source = content_file.read()

        matches = document.Document(source).find_all(document.ALL_DECL_RE, flags=re.MULTILINE)
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
            # the declaration in the comment anyway
            # (only whitespace before allowed)
            (559, 645),
            (726, 801),
            (866, 950),
            (1016, 1101),
            (1143, 1186),
            (1237, 1272),
            (1317, 1343)
        ]

        with open(FIND_DECL_FILE) as content_file:
            source = content_file.read()
        doc = document.Document(source)
        matches = doc.find_all_declarations()

        self.assertEqual(matches, expected)
