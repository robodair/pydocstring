"""
Test simple formatting of google style docstrings
"""

import sys
import unittest
import pytest

from pydocstring import generate_docstring


class TestGoogleFunctionFormatting(unittest.TestCase):

    def test_params_args_kwargs(self):
        method = \
            """
def method(*args, **kwargs):
    pass
"""
        docstring = generate_docstring(
            method, position=(2, 2), formatter="google")
        expected = """


Args:
    *args: Variable length argument list.
    **kwargs: Arbitrary keyword arguments.

"""
        assert docstring == expected

    def test_params_no_literal_set(self):
        method = \
            """
def method(p1, p2=2,
           p3=3, p4={'a':'b'},
           p5=[1,2,3], p6=True,
           p7=set([1,2,3]),
           p9=(1,2,3)):
    pass
"""
        docstring = generate_docstring(
            method, position=(2, 2), formatter="google")
        expected = """


Args:
    p1 (TYPE): \n\
    p2 (int):  default: ``2``
    p3 (int):  default: ``3``
    p4 (dict):  default: ``{'a':'b'}``
    p5 (list):  default: ``[1,2,3]``
    p6 (bool):  default: ``True``
    p7 (set):  default: ``set([1,2,3])``
    p9 (tuple):  default: ``(1,2,3)``

"""
        assert docstring == expected

    @pytest.mark.skipif(sys.version_info < (2, 7), reason="Requires Python 2.7")
    def test_params_py27(self):
        method = \
            """
def method(p1, p2=2,
           p3=3, p4={'a':'b'},
           p5=[1,2,3], p6=True,
           p7=set([1,2,3]), p8={1,2,3},
           p9=(1,2,3)):
    pass
"""
        docstring = generate_docstring(
            method, position=(2, 2), formatter="google")
        expected = """


Args:
    p1 (TYPE): \n\
    p2 (int):  default: ``2``
    p3 (int):  default: ``3``
    p4 (dict):  default: ``{'a':'b'}``
    p5 (list):  default: ``[1,2,3]``
    p6 (bool):  default: ``True``
    p7 (set):  default: ``set([1,2,3])``
    p8 (set):  default: ``{1,2,3}``
    p9 (tuple):  default: ``(1,2,3)``

"""
        assert docstring == expected

    @pytest.mark.skipif(sys.version_info < (3, 0), reason="Requires Python 3.0")
    def test_params_py3(self):
        method = \
            """
def method(p1, p2: int,
           p3=3, p4={'a':'b'},
           p5=[1,2,3], p6=True,
           p7=set([1,2,3]), p8={1,2,3},
           p9=(1,2,3)):
    pass
"""
        docstring = generate_docstring(
            method, position=(2, 2), formatter="google")
        expected = """


Args:
    p1 (TYPE): \n\
    p2 (int): \n\
    p3 (int):  default: ``3``
    p4 (dict):  default: ``{'a':'b'}``
    p5 (list):  default: ``[1,2,3]``
    p6 (bool):  default: ``True``
    p7 (set):  default: ``set([1,2,3])``
    p8 (set):  default: ``{1,2,3}``
    p9 (tuple):  default: ``(1,2,3)``

"""
        assert docstring == expected

    @pytest.mark.skipif(sys.version_info < (3, 0), reason="Requires Python 3.0")
    def test_return_annotation_only(self):
        method = \
            """
def method() -> int:
    pass
"""
        docstring = generate_docstring(
            method, position=(2, 2), formatter="google")

        expected = """


Returns:
    int: \n\

"""
        assert docstring == expected

    @pytest.mark.skipif(sys.version_info < (3, 0), reason="Requires Python 3.0")
    def test_return_type_and_statement(self):
        method = \
            """
def method() -> int:
    return var1
"""
        docstring = generate_docstring(
            method, position=(2, 2), formatter="google")

        expected = """


Returns:
    int: var1

"""
        assert docstring == expected

    def test_yields_statement_simple(self):
        method = \
            """
def method():
    yield var1
"""
        docstring = generate_docstring(
            method, position=(2, 2), formatter="google")

        expected = """


Yields:
    TYPE: var1

"""

        assert docstring == expected

    def test_yields_statement_expression(self):
        method = \
            """
def method():
    yield 2*2
"""
        docstring = generate_docstring(
            method, position=(2, 2), formatter="google")

        expected = """


Yields:
    TYPE: 2*2

"""
        assert docstring == expected

    def test_yields_statement_multiline(self):
        method = \
            """
def method():
    yield {
        2:3
    }
"""
        docstring = generate_docstring(
            method, position=(2, 2), formatter="google")

        expected = """


Yields:
    TYPE: { 2:3 }

"""

        assert docstring == expected

    def test_return_statement_simple(self):
        method = \
            """
def method():
    return var1
"""
        docstring = generate_docstring(
            method, position=(2, 2), formatter="google")
        expected = """


Returns:
    TYPE: var1

"""
        assert docstring == expected

    def test_return_statement_expression(self):
        method = \
            """
def method():
    return 2*2
"""
        docstring = generate_docstring(
            method, position=(2, 2), formatter="google")
        expected = """


Returns:
    TYPE: 2*2

"""
        assert docstring == expected

    def test_return_statement_multiline(self):
        method = \
            """
def method():
    return {
        'a':'b'
    }
"""
        docstring = generate_docstring(
            method, position=(2, 2), formatter="google")
        expected = """


Returns:
    TYPE: { 'a':'b' }

"""
        assert docstring == expected

    def test_one_exception_instantiated(self):
        method = \
            """
def method():
    raise MyException()
"""

        docstring = generate_docstring(
            method, position=(2, 2), formatter="google")

        expected = """


Raises:
    MyException: \n\n"""
        assert docstring == expected

    def test_one_exception_uninstantiated(self):
        method = \
            """
def method():
    raise MyExceptionUninstantiated
"""

        docstring = generate_docstring(
            method, position=(2, 2), formatter="google")

        expected = """


Raises:
    MyExceptionUninstantiated: \n\n"""
        assert docstring == expected

    def test_two_exceptions(self):
        method = \
            """
def method():
    if 1==1:
        raise MyException()
    else:
        raise Exception
"""

        docstring = generate_docstring(
            method, position=(2, 2), formatter="google")

        expected = """


Raises:
    MyException: \n\
    Exception: \n
"""
        assert docstring == expected


class TestGoogleClassFormatting(unittest.TestCase):

    def test_class_attributes(self):
        code = \
            """
class HelloWorld():
    attr1 = 3 * some_var
    attr2 = 2
    def some_func():
        pass
    class InnerClass():
        pass
"""

        docstring = generate_docstring(
            code, position=(2, 2), formatter="google")

        expected = """


Attributes:
    attr1 (TYPE): 3 * some_var
    attr2 (int): 2\n
"""
        assert docstring == expected


class TestGoogleModuleFormatting(unittest.TestCase):

    def test_module_attributes(self):
        module = \
            """
from somewhere import var

mattr1 = 3 * var
mattr2 = 2
def some_func():
    pass
class InnerClass():
    pass
"""
        docstring = generate_docstring(
            module, position=(2, 2), formatter="google")

        expected = """


Attributes:
    mattr1 (TYPE): 3 * var
    mattr2 (int): 2\n
"""
        assert docstring == expected

    def test_none(self):
        module = ""
        docstring = generate_docstring(
            module, position=(1, 0), formatter="google")

        expected = """

Empty Module

"""
        assert docstring == expected
