"""Utilities for manipulating python a document (provided as 'source') to many methods"""

# Much of the logic here has been adapted from the SublimeAutoDocstring Project,
# which is also MIT licenced.
# https://github.com/KristoforMaynard/SublimeAutoDocstring

# License for SublimeAutoDocstring:
# =================================

# The MIT License (MIT)

# Copyright (c) 2014 Kristofor Maynard

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from __future__ import print_function
import re

__CLASS_RE = r"(class)\s+([^\s\(\):]+)\s*(\(([\s\S]*?)\))?"
__FUNC_RE = r"(?:async\s*)?(def)\s+([^\s\(\):]+)\s*\(([\s\S]*?)\)\s*(->.*?)?"

ALL_DECL_RE = r"^[^\S\n]*({0}|{1})\s*:".format(__CLASS_RE, __FUNC_RE)
CLASS_DECL_RE = r"^[^\S\n]*{0}\s*:".format(__CLASS_RE)
FUNC_DECL_RE = r"^[^\S\n]*{0}\s*:".format(__FUNC_RE)

# Yes, this will swallow a large chunk of the document if there's an open string
# (like one for autocomplete), but in that case we're ignoring everythong after the cursor anyway
PYTHON_STRINGS = r"(\"\"\"[\s\S]*?\"\"\")|(\"[\s\S]*?\")|(\'\'\'[\s\S]*?\'\'\')|(\'[\s\S]*?\')"
PYTHON_COMMENTS = r"#.*"

class Document(object):
    """Represents the source of a document provides useful methods like find_all and the ability
    to retrieve ranges of text

    Args:
        source (string): the source of the document
    """

    def __init__(self, source):
        """Represents the source of a document provides useful methods like find_all and the ability
        to retrieve ranges of text

        Args:
            source (string): the source of the document
        """
        self.source = source


    def find_all(self, pattern, flags=0, excludes=None):
        """Return a list of tuples containing the start and end for non-overlapping matches in the
        document
        When using the ALL_DECL_RE pattern you'll want to use the re.MULTILINE flag, and when using
        the PYTHON_COMMENTS and PYTHON_STRINGS patterns you'll want to use the 0 flag

        Args:
            pattern (str): Regex pattern to find
            flags (int): Flags to use for `pattern`
            excludes (list): A list of tuples containing (pattern, flags). Matches for pattern
                argument will not be returned if they overlap with one of the patterns in excludes
                EXCEPT when the match from excludes is entirely within the match from pattern
                TODO: Refactor this logic out into a separate method so this is just a find all - that's easy because this method is just making a few recursive calls anyway

        Returns:
            list: of tuples, containing start and end indexes
        """
        regex = re.compile(pattern, flags)
        initial_ranges = []
        for match in regex.finditer(self.source):
            initial_ranges.append((match.start(), match.end()))

        return initial_ranges

    def find_all_declarations(self):
        """Get a list of all the class and method declarations in the document, excluding those that
        are inside an active string or comment. This method is just a wrapper around find_all()

        Returns:
            list: A list of tuples of the ranges found
        """
        initial_ranges = self.find_all(ALL_DECL_RE, re.MULTILINE)

        final_ranges = []
        exclude_ranges = self.find_all(PYTHON_COMMENTS)
        exclude_ranges += self.find_all(PYTHON_STRINGS)

        def overlap(min1, max1, min2, max2):
            return max(0, min(max1, max2) - max(min1, min2))

        for rng in initial_ranges:
            try:
                for exc in exclude_ranges:
                    if overlap(min(rng), max(rng), min(exc), max(exc)) > 0:
                        if max(rng) > max(exc) and min(rng) < min(exc):
                            continue # str is contained within the declaration - probably a default
                        raise StopIteration()
                final_ranges.append(rng)
            except StopIteration:
                pass

        return final_ranges



    def get_range(self, start, end):
        """Return the section of the document between start and end"""
        return self.source[start:end]
