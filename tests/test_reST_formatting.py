"""
Test simple formatting of reST style docstrings
"""

import unittest
from pydocstring.formatters import reST
from collections import OrderedDict


class TestreSTFunctionFormatting(unittest.TestCase):

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
        docstring = reST.function_docstring(params, None, None, None)

        expected = """


:param p1: \n\
:type p1: TYPE
:param p2: \n\
:type p2: int
:param p3: default: ``2``
:type p3: int

"""
        self.assertEqual(docstring, expected)

    def test_return_type(self):
        docstring = reST.function_docstring(None, "int", None, None)

        expected = """


:returns: \n\
:rtype: int

"""
        self.assertEqual(docstring, expected)

    def test_none(self):
        docstring = reST.function_docstring(None, None, None, None)

        expected = """

"""
        self.assertEqual(docstring, expected)

    def test_return_type_and_statement(self):
        docstring = reST.function_docstring(
            None, "int", None, [("return", "var1")])

        expected = """


:returns: var1
:rtype: int

"""
        self.assertEqual(docstring, expected)

    def test_yields_statement(self):
        docstring = reST.function_docstring(
            None, None, None, [("yield", "var1")])

        expected = """


:yields: var1
:rtype: TYPE

"""

        self.assertEqual(docstring, expected)

    def test_returns_statement(self):
        docstring = reST.function_docstring(
            None, None, None, [("returns", "var1")])

        expected = """


:returns: var1
:rtype: TYPE

"""

    def test_exceptions(self):
        docstring = reST.function_docstring(
            None, None, ["MyException"], None)

        expected = """


:raises: MyException\n\n"""
        self.assertEqual(docstring, expected)


class TestreSTClassFormatting(unittest.TestCase):

    def test_class_attributes(self):
        attributes = [
            ("attr1", "3 * some_var", None),
            ("attr2", "2", "int")
        ]
        docstring = reST.class_docstring(attributes)

        expected = """


:attr attr1: 3 * some_var
:type attr1: TYPE
:attr attr2: 2
:type attr2: int\n\n"""
        self.assertEqual(docstring, expected)


class TestreSTModuleFormatting(unittest.TestCase):

    def test_module_attributes(self):
        attributes = [
            ("mattr1", "3 * some_var", None),
            ("mattr2", "2", "int")
        ]
        docstring = reST.module_docstring(attributes)

        expected = """


:attr mattr1: 3 * some_var
:type mattr1: TYPE
:attr mattr2: 2
:type mattr2: int\n\n"""
        self.assertEqual(docstring, expected)
