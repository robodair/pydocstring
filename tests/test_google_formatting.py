"""
Test simple formatting of google style docstrings
"""

import unittest
from pydocstring.formatters import google
from collections import OrderedDict

class TestGoogleFunctionFormatting(unittest.TestCase):

    def test_params(self):
        params = OrderedDict(
            [("p1", {
                "default": None,
                "type": None
            }),
            ("p2", {
                "default": None,
                "type": "int"
            })]
        )
        docstring = google.function_docstring(params, None, None, None)

        expected = """


Args:
    p1 (TYPE):
    p2 (int):

"""
        self.assertEqual(docstring, expected)

    def test_return_type(self):
        docstring = google.function_docstring(None, "int", None, None)

        expected = """


Returns:
    int:

"""
        self.assertEqual(docstring, expected)

    def test_none(self):
        docstring = google.function_docstring(None, None, None, None)

        expected = """

"""
        self.assertEqual(docstring, expected)

    def test_return_type_and_statement(self):
        docstring = google.function_docstring(None, "int", None, [("return", "var1")])

        expected = """


Returns:
    int: var1

"""
        self.assertEqual(docstring, expected)


    def test_yields_statement(self):
        docstring = google.function_docstring(None, None, None, [("yield", "var1")])

        expected = """


Yields:
    TYPE: var1

"""

        self.assertEqual(docstring, expected)

    def test_returns_statement(self):
        docstring = google.function_docstring(None, None, None, [("returns", "var1")])

        expected = """


Returns:
    TYPE: var1

"""

    def test_exceptions(self):
        docstring = google.function_docstring(None, None, ["MyException"], None)

        expected = """


Raises:
    MyException: \n\n"""
        self.assertEqual(docstring, expected)

class TestGoogleClassFormatting(unittest.TestCase):

    def test_class_attributes(self):
        attributes = [
            ("attr1", "3 * some_var", None),
            ("attr2", "2", "int")
        ]
        docstring = google.class_docstring(attributes)

        expected = """


Attributes:
    attr1 (TYPE): 3 * some_var
    attr2 (int): 2\n\n"""
        self.assertEqual(docstring, expected)

class TestGoogleModuleFormatting(unittest.TestCase):

    def test_module_attributes(self):
        attributes = [
            ("mattr1", "3 * some_var", None),
            ("mattr2", "2", "int")
        ]
        docstring = google.module_docstring(attributes)

        expected = """


Attributes:
    mattr1 (TYPE): 3 * some_var
    mattr2 (int): 2\n\n"""
        self.assertEqual(docstring, expected)
