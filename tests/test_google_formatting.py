import unittest
from pydocstring.formatters import google
from collections import OrderedDict

class TestGoogleFormatting(unittest.TestCase):

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
    p1:
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
