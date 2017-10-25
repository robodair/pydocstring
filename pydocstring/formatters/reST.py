"""
reST Docstring Formatter
"""
from parso.python.tree import Function, Class, Module, KeywordStatement, Name, PythonNode, ExprStmt

from pydocstring.formatters.format_utils import (
    safe_determine_type,
    get_param_info,
    get_return_info,
    get_exception_name
)


def function_docstring(parso_function):
    """
    Format a reST docstring for a function

    Args:
        parso_function (Function): The function tree node

    Returns:
        str: The formatted docstring
    """
    assert isinstance(parso_function, Function)

    docstring = "\n"

    params = parso_function.get_params()
    if params:
        docstring += "\n\n"
        for param in params:
            if param.star_count == 1:
                docstring += ":param *{0}: {1}\n".format(param.name.value,
                                                        "Variable length argument list.")
            elif param.star_count == 2:
                docstring += ":param **{0}: {1}\n".format(param.name.value,
                                                        "Arbitrary keyword arguments.")
            else:
                docstring += ":param {0}: {2}\n:type {0}: {1}\n".format(*get_param_info(param))

    returns = list(parso_function.iter_return_stmts())
    if returns:
        docstring += "\n\n"
        for ret in returns:
            docstring += ":return: {1}\n:rtype: {0}\n".format(
                *get_return_info(ret, parso_function.annotation))
    elif parso_function.annotation:
        docstring += "\n\n"
        docstring += ":return: \n:rtype: {0}\n".format(parso_function.annotation.value)

    yields = list(parso_function.iter_yield_exprs())
    if yields:
        docstring += "\n\n"
        for yie in yields:
            docstring += ":yields: {1}\n:ytype: {0}\n".format(
                *get_return_info(yie, parso_function.annotation))

    raises = list(parso_function.iter_raise_stmts())
    if raises:
        docstring += "\n\n"
        for exception in raises:
            docstring += ":raises {0}: \n".format(get_exception_name(exception))

    docstring += "\n"
    return docstring

def class_docstring(parso_class):
    """
    Format a reST docstring for a class

    Only documents attributes, ``__init__`` method args can be documented on the ``__init__`` method

    Args:
        parso_class (Class): The class tree node

    Returns:
        str: The formatted docstring

    """
    assert isinstance(parso_class, Class)
    docstring = "\n"
    attribute_expressions = []

    for child in parso_class.children:
        if child.type == 'suite':
            for child2 in child.children:
                if child2.type == 'simple_stmt':
                    for child3 in child2.children:
                        if child3.type == 'expr_stmt':
                            attribute_expressions.append(child3)

    if attribute_expressions:
        docstring += "\n\n"
        for attribute in attribute_expressions:
            name = attribute.children[0].value
            code = attribute.get_rhs().get_code().strip()
            attr_type = safe_determine_type(code)
            attr_str = ":var {0}: {2}\n:type {0}: {1}\n".format(name, attr_type, code)
            docstring += attr_str

    docstring += "\n"
    return docstring


def module_docstring(parso_module):
    """
    Format a reST docstring for a module

    Only documents attributes, ``__init__`` method args can be documented on the ``__init__`` method

    Args:
        parso_module (Module): The module tree node

    Returns:
        str: The formatted docstring

    """
    assert isinstance(parso_module, Module)
    docstring = "\n"
    attribute_expressions = []

    for child in parso_module.children:
        if child.type == 'simple_stmt':
            for child2 in child.children:
                if child2.type == 'expr_stmt':
                    attribute_expressions.append(child2)

    if attribute_expressions:
        docstring += "\n\n"
        for attribute in attribute_expressions:
            name = attribute.children[0].value
            code = attribute.get_rhs().get_code().strip()
            attr_type = safe_determine_type(code)
            attr_str = ":var {0}: {2}\n:type {0}: {1}\n".format(name, attr_type, code)
            docstring += attr_str

    docstring += "\n"
    if not docstring.strip():
        docstring = "\n\nEmpty Module\n\n"
    return docstring
