"""Utilities for dealing with functions as blocks of text e.g. parsing parameters, return values"""
from __future__ import print_function
import re
import textwrap
from collections import OrderedDict

# TODO: parse_function_parameters method
# def parse_function_parameters():
#     """Parse function parameters into an OrderedDict of Parameters

#     Args:
#         s (str): everything in the parenthesis of a function
#             declaration
#         ret_annotation (str): return annotation if any
#         default_type (str): default type text
#         default_description (str): default text
#         optional_tag (str): tag included with type for kwargs when
#             they are created

#     Returns:
#         OrderedDict containing Parameter instances
#     """


def parse_return_keyword(text):
    """Scan a function's code to look for how it returns, and what follows the return or yield
    You should pass the block of code as returned by `Document`'s `get_block()` method

    Args:
        text: The text of a function

    Returns:
        set of tuples: 'return' or 'yield' and the statement following it
    """
    return_re = re.compile(r"^\s*(return|yield)\s*(.*)", re.MULTILINE)
    matches = set()
    for match in return_re.finditer(text):
        matches.add(match.groups())
    return matches


def parse_function_exceptions(text):
    """Scan a function looking for where it raises exceptions
    Args:
        text: The text of a function

    Returns:
        set of tuples: 'raise' and the Exception following it
    """
    execp_re = re.compile(r"^[^\S\n]*(raise)[^\S\n]+([^\s\(]+)", re.MULTILINE)
    matches = set()
    for match in execp_re.finditer(text):
        matches.add(match.groups())
    return matches


def parse_class_attributes(text):
    """Scan a class for all of the attributes

    Args:
        text: The text of a function

    Returns:
        set: A list of the class attributes
    """
    dedent_text = textwrap.dedent(text)
    # Determine the indentation used in the class
    indentations = [line[:len(line) - len(line.lstrip())] for line in dedent_text.splitlines()]
    indent = min([indent for indent in indentations if indent])
    execp_re = re.compile(r"^(^{0}([A-Za-z0-9_]+)|^{1}self\.([A-Za-z0-9_]+))\s*=\s*(.*)"
                          .format(indent, indent * 2), re.MULTILINE)
    matches = OrderedDict()
    for match in execp_re.finditer(dedent_text):
        if match.group(2): # class variable
            matches[match.group(2)] = match.group(4)
        elif match.group(3): # instance variable
            matches[match.group(3)] = match.group(4)
    matches_set = set([(key, matches[key]) for key in matches])
    return matches_set
