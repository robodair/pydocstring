"""
Test simple formatting of reST style docstrings
"""
import sys
import unittest
import pytest
from pydocstring.exc import FailedToGenerateDocstringError
from pydocstring import generate_docstring


class TestreSTFunctionFormatting(unittest.TestCase):

    def test_params_args_kwargs(self):
        method = \
            """
def method(*args, **kwargs):
    pass
"""
        docstring = generate_docstring(
            method, position=(2, 2), formatter="reST")
        expected = """


:param *args: Variable length argument list.
:param **kwargs: Arbitrary keyword arguments.

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
            method, position=(2, 2), formatter="reST")
        expected = """


:param p1: \n\
:type p1: TYPE
:param p2:  default: ``2``
:type p2: int
:param p3:  default: ``3``
:type p3: int
:param p4:  default: ``{'a':'b'}``
:type p4: dict
:param p5:  default: ``[1,2,3]``
:type p5: list
:param p6:  default: ``True``
:type p6: bool
:param p7:  default: ``set([1,2,3])``
:type p7: set
:param p9:  default: ``(1,2,3)``
:type p9: tuple

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
            method, position=(2, 2), formatter="reST")
        expected = """


:param p1: \n\
:type p1: TYPE
:param p2:  default: ``2``
:type p2: int
:param p3:  default: ``3``
:type p3: int
:param p4:  default: ``{'a':'b'}``
:type p4: dict
:param p5:  default: ``[1,2,3]``
:type p5: list
:param p6:  default: ``True``
:type p6: bool
:param p7:  default: ``set([1,2,3])``
:type p7: set
:param p8:  default: ``{1,2,3}``
:type p8: set
:param p9:  default: ``(1,2,3)``
:type p9: tuple

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
            method, position=(2, 2), formatter="reST")
        expected = """


:param p1: \n\
:type p1: TYPE
:param p2: \n\
:type p2: int
:param p3:  default: ``3``
:type p3: int
:param p4:  default: ``{'a':'b'}``
:type p4: dict
:param p5:  default: ``[1,2,3]``
:type p5: list
:param p6:  default: ``True``
:type p6: bool
:param p7:  default: ``set([1,2,3])``
:type p7: set
:param p8:  default: ``{1,2,3}``
:type p8: set
:param p9:  default: ``(1,2,3)``
:type p9: tuple

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
            method, position=(2, 2), formatter="reST")

        expected = """


:return: \n\
:rtype: int

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
            method, position=(2, 2), formatter="reST")

        expected = """


:return: var1
:rtype: int

"""
        assert docstring == expected

    @pytest.mark.skipif(sys.version_info < (3, 0), reason="Requires Python 3.0")
    def test_yield_statement_simple(self):
        method = \
            """
def method():
    yield var1
"""
        docstring = generate_docstring(
            method, position=(2, 2), formatter="reST")

        expected = """


:yields: var1
:ytype: TYPE

"""

        assert docstring == expected

    def test_yield_statement_expression(self):
        method = \
            """
def method():
    yield 2*2
"""
        docstring = generate_docstring(
            method, position=(2, 2), formatter="reST")

        expected = """


:yields: 2*2
:ytype: TYPE

"""
        assert docstring == expected

    def test_yield_statement_multiline(self):
        method = \
            """
def method():
    yield {
        2:3
    }
"""
        docstring = generate_docstring(
            method, position=(2, 2), formatter="reST")

        expected = """


:yields: { 2:3 }
:ytype: TYPE

"""

        assert docstring == expected

    def test_return_statement_simple(self):
        method = \
            """
def method():
    return var1
"""
        docstring = generate_docstring(
            method, position=(2, 2), formatter="reST")
        expected = """


:return: var1
:rtype: TYPE

"""
        assert docstring == expected

    def test_return_statement_expression(self):
        method = \
            """
def method():
    return 2*2
"""
        docstring = generate_docstring(
            method, position=(2, 2), formatter="reST")
        expected = """


:return: 2*2
:rtype: TYPE

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
            method, position=(2, 2), formatter="reST")
        expected = """


:return: { 'a':'b' }
:rtype: TYPE

"""
        assert docstring == expected

    def test_one_exception_instantiated(self):
        method = \
            """
def method():
    raise MyException()
"""

        docstring = generate_docstring(
            method, position=(2, 2), formatter="reST")

        expected = """


:raises MyException: \n\

"""
        assert docstring == expected

    def test_one_exception_uninstantiated(self):
        method = \
            """
def method():
    raise MyExceptionUninstantiated
"""

        docstring = generate_docstring(
            method, position=(2, 2), formatter="reST")

        expected = """


:raises MyExceptionUninstantiated: \n\

"""
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
            method, position=(2, 2), formatter="reST")

        expected = """


:raises MyException: \n\
:raises Exception: \n\

"""
        assert docstring == expected


class TestreSTClassFormatting(unittest.TestCase):

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

        docstring = generate_docstring(code, position=(2, 2), formatter="reST")

        expected = """


:var attr1: 3 * some_var
:type attr1: TYPE
:var attr2: 2
:type attr2: int

"""
        assert docstring == expected


class TestreSTModuleFormatting(unittest.TestCase):

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
        docstring = generate_docstring(module, position=(2, 2), formatter="reST")

        expected = """


:var mattr1: 3 * var
:type mattr1: TYPE
:var mattr2: 2
:type mattr2: int

"""
        assert docstring == expected

    def test_none(self):
        module = ""
        docstring = generate_docstring(module, position=(1, 0), formatter="reST")

        expected = """

Empty Module

"""
        assert docstring == expected
