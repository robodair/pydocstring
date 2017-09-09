"""Tests for parse_utils module"""

import unittest
from collections import OrderedDict
from pydocstring import parse_utils


class TestParseUtils(unittest.TestCase):
    """Test functionality of the parse_utils module"""

    def test_no_params(self):
        decl = "def method_norm():"
        print("Decl Was:", decl)
        expected_params = OrderedDict()
        expected_type = None
        result_params, result_type = parse_utils.parse_function_declaration(decl)
        self.assertEqual(result_params, expected_params)
        self.assertEqual(result_type, expected_type)

    def test_basic_params(self):
        decl = "def method_params(p1, p2):"
        print("Decl Was:", decl)
        expected_params = OrderedDict([
                ('p1', {'default': None, 'type': None}),
                ('p2', {'default': None, 'type': None})])
        expected_type = None
        result_params, result_type = parse_utils.parse_function_declaration(decl)
        self.assertEqual(result_params, expected_params)
        self.assertEqual(result_type, expected_type)

    def test__init__(self):
        decl = "    def __init__(self, c1, c2: int):"
        print("Decl Was:", decl)
        expected_params = OrderedDict([
                ('self', {'default': None, 'type': None}),
                ('c1', {'default': None, 'type': None}),
                ('c2', {'default': None, 'type': 'int'})])
        expected_type = None
        result_params, result_type = parse_utils.parse_function_declaration(decl)
        self.assertEqual(result_params, expected_params)
        self.assertEqual(result_type, expected_type)

    def test_class_method(self):
        decl = "    def class_method(self):"
        print("Decl Was:", decl)
        expected_params = OrderedDict([
                ('self', {'default': None, 'type': None})])
        expected_type = None
        result_params, result_type = parse_utils.parse_function_declaration(decl)
        self.assertEqual(result_params, expected_params)
        self.assertEqual(result_type, expected_type)

    def test_multiline_method(self):
        decl = "def method_multiline(param1,\
                        param2):"
        print("Decl Was:", decl)
        expected_params = OrderedDict([
                ('param1', {'default': None, 'type': None}),
                ('param2', {'default': None, 'type': None})])
        expected_type = None
        result_params, result_type = parse_utils.parse_function_declaration(decl)
        self.assertEqual(result_params, expected_params)
        self.assertEqual(result_type, expected_type)

    def test_kw_1(self):
        decl = 'def method_ag_kw_normal(p1, p2, ls=[1], st="string", tup=(1, 2), di={"key": "value"}):'
        print("Decl Was:", decl)
        expected_params = OrderedDict([
                ('p1', {'default': None, 'type': None}),
                ('p2', {'default': None, 'type': None}),
                ('ls', {'default': '[1]', 'type': 'list'}),
                ('st', {'default': '"string"', 'type': 'str'}),
                ('tup', {'default': '(1, 2)', 'type': 'tuple'}),
                ('di', {'default': '{"key": "value"}', 'type': 'dict'})])
        expected_type = None
        result_params, result_type = parse_utils.parse_function_declaration(decl)
        self.assertEqual(result_params, expected_params)
        self.assertEqual(result_type, expected_type)

    def test_kw_2(self):
        decl = "def method_kw_normal(ls=[1], st='string', tup=(1, 2), se={'one', 'two'}):"
        print("Decl Was:", decl)
        expected_params = OrderedDict([
                ('ls', {'default': '[1]', 'type': 'list'}),
                ('st', {'default': "'string'", 'type': 'str'}),
                ('tup', {'default': '(1, 2)', 'type': 'tuple'}),
                ('se', {'default': "{'one', 'two'}", 'type': 'set'})])
        expected_type = None
        result_params, result_type = parse_utils.parse_function_declaration(decl)
        self.assertEqual(result_params, expected_params)
        self.assertEqual(result_type, expected_type)

    def test_kw_3(self):
        decl = 'def method_kw_space(ls = [ 1 ], st = "string", tup = (1, 2), di = {"key": "value"}):'
        print("Decl Was:", decl)
        expected_params = OrderedDict([
                ('ls', {'default': '[ 1 ]', 'type': 'list'}),
                ('st', {'default': '"string"', 'type': 'str'}),
                ('tup', {'default': '(1, 2)', 'type': 'tuple'}),
                ('di', {'default': '{"key": "value"}', 'type': 'dict'})])
        expected_type = None
        result_params, result_type = parse_utils.parse_function_declaration(decl)
        self.assertEqual(result_params, expected_params)
        self.assertEqual(result_type, expected_type)

    def test_kw_4(self):
        decl = 'def force_kw(p1, p2, *, ls=[1], st="string", tup=(1, 2), di={"key": "value"}):'
        print("Decl Was:", decl)
        expected_params = OrderedDict([
                ('p1', {'default': None, 'type': None}),
                ('p2', {'default': None, 'type': None}),
                ('ls', {'default': '[1]', 'type': 'list'}),
                ('st', {'default': '"string"', 'type': 'str'}),
                ('tup', {'default': '(1, 2)', 'type': 'tuple'}),
                ('di', {'default': '{"key": "value"}', 'type': 'dict'})])
        expected_type = None
        result_params, result_type = parse_utils.parse_function_declaration(decl)
        import pprint
        pprint.pprint(result_params)
        pprint.pprint(expected_params)
        self.assertEqual(result_params, expected_params)
        self.assertEqual(result_type, expected_type)

    def test_kw_5(self):
        decl = "def method_kw_only(*, ls=[1], st='string', tup=(1, 2), di={'key': 'value'}):"
        print("Decl Was:", decl)
        expected_params = OrderedDict([
                ('ls', {'default': '[1]', 'type': 'list'}),
                ('st', {'default': "'string'", 'type': 'str'}),
                ('tup', {'default': '(1, 2)', 'type': 'tuple'}),
                ('di', {'default': "{'key': 'value'}", 'type': 'dict'})])
        expected_type = None
        result_params, result_type = parse_utils.parse_function_declaration(decl)
        self.assertEqual(result_params, expected_params)
        self.assertEqual(result_type, expected_type)

    def test_mixed_space(self):
        decl = 'def method_kw_mixed_space(ls= [1 ], st ="string", tup= (1, 2), di ={"key": "value"}):'
        print("Decl Was:", decl)
        expected_params = OrderedDict([
                ('ls', {'default': '[1 ]', 'type': 'list'}),
                ('st', {'default': '"string"', 'type': 'str'}),
                ('tup', {'default': '(1, 2)', 'type': 'tuple'}),
                ('di', {'default': '{"key": "value"}', 'type': 'dict'})])
        expected_type = None
        result_params, result_type = parse_utils.parse_function_declaration(decl)
        self.assertEqual(result_params, expected_params)
        self.assertEqual(result_type, expected_type)

    def test_type(self):
        decl = "def method_type(p1: str, p2: list) -> dict:"
        print("Decl Was:", decl)
        expected_params = OrderedDict([
                ('p1', {'default': None, 'type': 'str'}),
                ('p2', {'default': None, 'type': 'list'})])
        expected_type = 'dict'
        result_params, result_type = parse_utils.parse_function_declaration(decl)
        self.assertEqual(result_params, expected_params)
        self.assertEqual(result_type, expected_type)

    def test_expand(self):
        decl = "def method_expand(*args, **kwargs):"
        print("Decl Was:", decl)
        expected_params = OrderedDict([
                ('*args', {'default': None, 'type': None}),
                ('**kwargs', {'default': None, 'type': None})])
        expected_type = None
        result_params, result_type = parse_utils.parse_function_declaration(decl)
        self.assertEqual(result_params, expected_params)
        self.assertEqual(result_type, expected_type)

    def test_comment_after(self):
        decl = "def comment_following():#a comment"
        print("Decl Was:", decl)
        expected_params = OrderedDict()
        expected_type = None
        result_params, result_type = parse_utils.parse_function_declaration(decl)
        self.assertEqual(result_params, expected_params)
        self.assertEqual(result_type, expected_type)

    def test_return_kw_none(self):
        """Test the response when there is no return keyword"""
        source = \
            '''    def _handle_long_word(self, reversed_chunks, cur_line, cur_len, width):
        """_handle_long_word(chunks : [string],
                             cur_line : [string],
                             cur_len : int, width : int)

        Handle a chunk of text (most likely a word, not whitespace) that
        is too long to fit in any line.
        """
        # Figure out when indent is larger than the specified width, and make
        # sure at least one character is stripped off on every pass
        if width < 1:
            space_left = 1
        else:
            space_left = width - cur_len

        # If we're allowed to break long words, then do so: put as much
        # of the next chunk onto the current line as will fit.
        if self.break_long_words:
            cur_line.append(reversed_chunks[-1][:space_left])
            reversed_chunks[-1] = reversed_chunks[-1][space_left:]

        # Otherwise, we have to preserve the long word intact.  Only add
        # it to the current line if there's nothing already there --
        # that minimizes how much we violate the width constraint.
        elif not cur_line:
            cur_line.append(reversed_chunks.pop())

        # If we're not allowed to break long words, and there's already
        # text on the current line, do nothing.  Next time through the
        # main loop of _wrap_chunks(), we'll wind up here again, but
        # cur_len will be zero, so the next line will be entirely
        # devoted to the long word that we can't handle right now.
'''
        result = parse_utils.parse_return_keyword(source)
        self.assertEqual(result, [])

    def test_return_kw_return(self):
        """Test the response when there is a return keyword"""
        source = \
            '''def fill(text, width=70, **kwargs):
    """Fill a single paragraph of text, returning a new string.

    Reformat the single paragraph in 'text' to fit in lines of no more
    than 'width' columns, and return a new string containing the entire
    wrapped paragraph.  As with wrap(), tabs are expanded and other
    whitespace characters converted to space.  See TextWrapper class for
    available keyword args to customize wrapping behaviour.
    """
    w = TextWrapper(width=width, **kwargs)
    return w.fill(text)
'''
        result = parse_utils.parse_return_keyword(source)
        self.assertEqual(result, [('return', 'w.fill(text)')])

    def test_return_kw_yield(self):
        """Test the response when there is a yield keyword"""
        source = \
            '''def firstn(n):
     num = 0
     while num < n:
         yield num
         num += 1
         yield num+7
'''
        result = parse_utils.parse_return_keyword(source)
        self.assertEqual(sorted(result), sorted([('yield', 'num'), ('yield', 'num+7')]))

    def test_parse_exceptions(self):
        """Test that exceptions are found in functions"""
        source = \
            '''def demo_bad_catch():
    try:
        raise ValueError('represents a hidden bug, do not catch this')
        raise Exception('This is the exception you expect to handle')
        raise ValueError('Another Value Error, but it's only shown once')
    except Exception as error:
        print('caught this error: ' + repr(error))
'''
        result = parse_utils.parse_function_exceptions(source)
        self.assertEqual(sorted(result), sorted(['Exception', 'ValueError']))

    def test_parse_class_attributes_simple(self):
        """Test class attributes are correctly garnered from a simple class"""
        source = \
            '''class TestClass(object):
    class_attr_1 = 0
    class_attr_2 = 2
    class_attr_override = 3

    def __init__(self):
        self.inst_attr_1 = 1
        self.inst_attr_2 = 2
        self.class_attr_override = 0
'''
        result = parse_utils.parse_class_attributes(source)
        self.assertEqual(sorted(result), sorted([('class_attr_1', '0'),
                                      ('class_attr_2', '2'),
                                      ('class_attr_override', '0'),
                                      ('inst_attr_1', '1'),
                                      ('inst_attr_2', '2')]))

    def test_parse_class_attributes_nested_indented(self):
        """Test class attributes are correctly garnered from a simple class"""
        source = \
            '''    class TestClass(object):
        class_attr_1 = 0
        class_attr_2 = 2
        class_attr_override = 3

        def __init__(self):
            self.inst_attr_1 = 1
            self.inst_attr_2 = 2
            self.class_attr_override = 0

        class ChildClass(object):
            sub_class_attr = 0

            def __init__(self):
                self.inst_attr_1 = 1
                self.inst_attr_2 = 2
                self.class_attr_override = 0
'''
        result = parse_utils.parse_class_attributes(source)
        self.assertEqual(sorted(result), sorted([('class_attr_1', '0'),
                                      ('class_attr_2', '2'),
                                      ('class_attr_override', '0'),
                                      ('inst_attr_1', '1'),
                                      ('inst_attr_2', '2')]))

    def test_parse_class_attributes_ignored_nested_class(self):
        """Test class attributes from a nested class are ignored"""
        source = \
            '''class TestClass(object):
    class_attr_1 = 0
    class_attr_2 = 2
    class_attr_override = 3

    def __init__(self):
        self.inst_attr_1 = 1
        self.inst_attr_2 = 2
        self.class_attr_override = 0

    class ChildClass(object):
        sub_class_attr = 0

        def __init__(self):
            self.inst_attr_1 = 1
            self.inst_attr_2 = 2
            self.class_attr_override = 0
'''
        result = parse_utils.parse_class_attributes(source)
        self.assertEqual(sorted(result), sorted([('class_attr_1', '0'),
                                      ('class_attr_2', '2'),
                                      ('class_attr_override', '0'),
                                      ('inst_attr_1', '1'),
                                      ('inst_attr_2', '2')]))

    def test_parse_module_attributes(self):
        """Test module attributes are identified and returned correctly"""
        source = \
            '''"""A Module Docstring"""
CONST_MODULE_ATTR = "constant"
print "a print statement"
print("print with brackets")
print 0 == 0
module_attr_1 = 0
# commented_module_attr = 2
someothermodule.thing = 20
'''
        result = parse_utils.parse_module_attributes(source)
        self.assertEqual(sorted(result), sorted([("CONST_MODULE_ATTR", '"constant"'),
                                      ("module_attr_1", "0")]))

    def test_parse_module_attributes_none(self):
        """Test module attributes are identified and returned correctly, when there are none"""
        source = \
            '''"""A Module Docstring"""
# CONST_MODULE_ATTR = "constant"
print "a print statement"
print("print with brackets")
print 0 == 0
# commented_module_attr = 2
# someothermodule.thing = 20
'''
        result = parse_utils.parse_module_attributes(source)
        self.assertEqual(result, [])
