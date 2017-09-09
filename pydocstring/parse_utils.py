"""
Utilities for dealing with functions as blocks of text

e.g. parsing parameters, return values
"""
import re
import textwrap
from collections import OrderedDict
import ast
import itertools

def parse_function_declaration(declaration):
    """Parse function parameters into an OrderedDict of Parameters and the return type (if any)

    OrderedDict Structure:

    .. code-block:: python

        {
            "param_name": {
                "default": "default value as a string",
                "type": "parameter type as a string or None"
                }
        }

    Args:
        declaration: The function declaration (e.g. everything from 'def' to the final ':')

    Returns:
        tuple: OrderedDict of parameters, and a string or None for return type

    """
    # FIXME: This doesn't support recursive brackets e.g: param=((1, 2), (3, 4)), need better engine
    # but what we can do is split on = and make sure the trimmed first group is all alphanumeric
    param_sep = re.compile(r",(?![^({[]*[]})])") # match commas not inside brackets
    params_re = re.compile(r"\((.*)\)") # everything between outermost brackets
    params_str = params_re.search(declaration).group(1) # inside brackets
    params_str = "" if not params_str else params_str.strip()
    params_list = [x for x in param_sep.split(params_str) if x.strip() != "*" and x.strip()]

    param_dict = OrderedDict()

    for param in params_list:
        param_default = None
        param_name = None
        param_type = None

        paramstr = param.strip()
        param_segments = param.split('=', 1) # split only on the first occurrence of '='
        if len(param_segments) > 1:
            param_name = param_segments[0].strip()
            param_default = param_segments[1].strip()
            try:
                param_type = type(ast.literal_eval(param_default)).__name__
            except ValueError:
                if (param_default.startswith('{') and param_default.endswith('}')):
                    set_str = param_default
                    olds, news = ['{', '}'] , ['[',']']
                    for old, new in itertools.izip(olds, news):
                        set_str = set_str.replace(old, new)
                    try:
                        param_type = type(set(ast.literal_eval(set_str))).__name__
                    except ValueError:
                        pass # can't determine type, doesn't matter
        else:
            param_segments = param.split(':', 1)
            if len(param_segments) > 1:
                param_name = param_segments[0].strip()
                param_type = param_segments[1].strip()
            else:
                param_name = param.strip()
        param_dict[param_name] = {
            "default": param_default,
            "type": param_type
        }

    # find the return type, if specified in the declaration
    return_type = None
    return_type_re = re.compile(r"\)\s+->\s+(.*)\s*:")
    return_type_match = return_type_re.search(declaration)
    if return_type_match:
        return_type = return_type_match.group(1)

    return param_dict, return_type

def parse_return_keyword(text):
    """Scan a function's code to look for how it returns, and what follows the return or yield
    You should pass the block of code as returned by `Document`'s `get_block()` method

    Args:
        text: The text of a function

    Returns:
        list of tuples: 'return' or 'yield' and the statement following it
    """
    return_re = re.compile(r"^\s*(return|yield)\s*(.*)", re.MULTILINE)
    matches = set()
    for match in return_re.finditer(text):
        matches.add(match.groups())
    return list(matches)


def parse_function_exceptions(text):
    """Scan a function looking for where it raises exceptions
    Args:
        text: The text of a function

    Returns:
        list: The names of exceptions raised in the function
    """
    execp_re = re.compile(r"^[^\S\n]*(raise)[^\S\n]+([^\s\(]+)", re.MULTILINE)
    matches = set()
    for match in execp_re.finditer(text):
        matches.add(match.group(2))
    return list(matches)


def parse_class_attributes(text):
    """Scan a class for all of the attributes

    Args:
        text: The text of a function

    Returns:
        list of tuples: The attribute names and an expression following one of their assignments
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
    return list(matches_set)

def parse_module_attributes(text):
    """Scan a module to find all of it's attributes

    Args:
        text: the text of the module

    Returns:
        list of tuples: The attribute name and expression following a (module level) assignment
    """
    attrib_re = re.compile(r"^([A-Za-z0-9_]+)\s*=\s*(.*)", re.MULTILINE)
    matches = OrderedDict()
    for match in attrib_re.finditer(text):
        matches[match.group(1)] = match.group(2)
    matches_set = set([(key, matches[key]) for key in matches])
    return list(matches_set)
