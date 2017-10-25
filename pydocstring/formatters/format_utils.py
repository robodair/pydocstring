"""Provides helper utilities for formatting"""

import ast


def safe_determine_type(string):
    """
    Determine the python type of the given literal, for use in docstrings

    Args:
        string (str): The string to evaluate

    Returns:
        ``str``: The type, or "TYPE" if the type could not be determined
    """
    try:
        return ast.literal_eval(string).__class__.__name__
    except ValueError:
        try:
            if (
                string.startswith('set(')
                or
                isinstance(ast.literal_eval(string.replace(
                    '{', '[').replace('}', ']')), list)
            ):
                return 'set'
        except ValueError:
            return 'TYPE'


def get_param_info(param):
    """
    Extract info from a parso parameter

    Args:
        param: the parameter

    Returns:
        tuple: name, type, default
    """
    param_type = param.annotation.value if param.annotation else "TYPE"
    param_default = " default: ``{0}``".format(
        param.default.get_code()) if param.default else ""
    if param_default and not param.annotation:
        param_type = safe_determine_type(param.default.get_code())
    return param.name.value, param_type, param_default


def get_return_info(ret, annotation):
    """
    Extract info from a node containing a return statement

    Args:
        ret: the return node
        annotation: the funcation annotation (may be None)

    Returns:
        tuple: type, expression after 'return' keyword
    """
    ret_type = annotation.value if annotation else 'TYPE'
    expression = "".join(x.get_code().strip() for x in ret.children[1:])
    expression = " ".join(expression.split())
    return ret_type, expression


def get_exception_name(node):
    """
    Find the name of an exception

    Args:
        node: Parso node containing the raises statement

    Returns:
        str: The exception name
    """
    name = node.children[1]
    while not name.type == 'name':
        name = name.children[0]
    return name.value
