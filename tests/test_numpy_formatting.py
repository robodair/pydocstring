"""
Test simple formatting of numpy style docstrings
"""

import unittest
from pydocstring.formatters import numpy
from collections import OrderedDict


class TestNumpyFunctionFormatting(unittest.TestCase):

    def test_params(self):
        params = OrderedDict(
            [
                ("p1", {
                    "default": None,
                    "type": None
                }),
                ("p2", {
                    "default": None,
                    "type": "int"
                }),
                ("p3", {
                    "default": "2",
                    "type": "int"
                })
            ]
        )
        docstring = numpy.function_docstring(params, None, None, None)

        expected = """


Parameters
----------
p1 : TYPE
    \n\
p2 : int
    \n\
p3 : int
    default: ``2``

"""
        self.assertEqual(docstring, expected)

    def test_return_type(self):
        docstring = numpy.function_docstring(None, "int", None, None)

        expected = """


Returns
-------
int
    \n\

"""
        self.assertEqual(docstring, expected)

    def test_none(self):
        docstring = numpy.function_docstring(None, None, None, None)

        expected = """

"""
        self.assertEqual(docstring, expected)

    def test_return_type_and_statement(self):
        docstring = numpy.function_docstring(
            None, "int", None, [("return", "var1")])

        expected = """


Returns
-------
int
    var1

"""
        self.assertEqual(docstring, expected)

    def test_yields_statement(self):
        docstring = numpy.function_docstring(
            None, None, None, [("yield", "var1")])

        expected = """


Yields
------
TYPE
    var1

"""

        self.assertEqual(docstring, expected)

    def test_returns_statement(self):
        docstring = numpy.function_docstring(
            None, None, None, [("returns", "var1")])

        expected = """


Returns
-------
    TYPE: var1

"""

    def test_exceptions(self):
        docstring = numpy.function_docstring(
            None, None, ["MyException"], None)

        expected = """


Raises
------
MyException
    \n\n"""
        self.assertEqual(docstring, expected)


class TestNumpyClassFormatting(unittest.TestCase):

    def test_class_attributes(self):
        attributes = [
            ("attr1", "3 * some_var", None),
            ("attr2", "2", "int")
        ]
        docstring = numpy.class_docstring(attributes)

        expected = """


Attributes
----------
attr1 : TYPE
    3 * some_var
attr2 : int
    2\n\n"""
        self.assertEqual(docstring, expected)


class TestNumpyModuleFormatting(unittest.TestCase):

    def test_module_attributes(self):
        attributes = [
            ("mattr1", "3 * some_var", None),
            ("mattr2", "2", "int")
        ]
        docstring = numpy.module_docstring(attributes)

        expected = """


Attributes
----------
mattr1 : TYPE
    3 * some_var
mattr2 : int
    2\n\n"""
        self.assertEqual(docstring, expected)
