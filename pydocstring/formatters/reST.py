"""
reST Docstring Formatter
"""


def function_docstring(params, return_type, exceptions, return_statements):
    """
    Format a reST docstring for a function

    Args:
        params (OrderedDict): as returned by :py:func:`pydocstring.parse_utils.parse_function_declaration`
        return_type (string or None): the return type of the function, if it was annotated
        exceptions (list): List of exceptions raised in the function
        return_statements (list): List of tuples containing 'yield' or 'return' as the first element
            and the statement following that as the second.

    Returns:
        str: The formatted docstring
    """

    docstring = "\n"

    if params:
        docstring += "\n\n"
        for param_name in params:
            param = params[param_name]
            param_type = param['type'] if param['type'] else "TYPE"
            param_default = "default: ``" + \
                param['default'] + "``" if param['default'] else ""
            param_str = ":param {0}: {2}\n:type {0}: {1}\n".format(
                param_name, param_type, param_default)
            docstring += param_str

    return_expression = ""
    return_statement = "returns"
    decl_return_type = "TYPE"
    if return_type:
        decl_return_type = return_type
    if return_statements:
        return_expression = return_statements[0][1]
        return_statement = return_statements[0][0] + "s"

    if return_statements or return_type:
        docstring += "\n\n:{0}: {1}\n:rtype: {2}\n".format(return_statement,
                                                           return_expression,
                                                           decl_return_type)

    if exceptions:
        docstring += "\n\n:raises: " + ", ".join(exceptions) + "\n"

    docstring += "\n"
    return docstring


def class_docstring(attributes):
    """
    Format a reST docstring for a class

    Only accepts attributes, ``__init__`` method args can be documented on the ``__init__`` method

    Args:
        attributes (list of tuples): attribute names, expression and type (or None)

    Returns:
        str: The formatted docstring

    """
    docstring = "\n"

    if attributes:
        docstring += "\n\n"
        for attribute, expression, attr_type in attributes:
            if not attr_type:
                attr_type = "TYPE"
            attr_str = ":attr {0}: {2}\n:type {0}: {1}\n".format(
                attribute, attr_type, expression)
            docstring += attr_str

    docstring += "\n"
    return docstring


def module_docstring(attributes):
    """
    Format a reST docstring for a module

    Only accepts attributes, ``__init__`` method args can be documented on the ``__init__`` method

    Args:
        attributes (list of tuples): attribute names, expression and type (or None)

    Returns:
        str: The formatted docstring

    """
    docstring = "\n"

    if attributes:
        docstring += "\n\n"
        for attribute, expression, attr_type in attributes:
            if not attr_type:
                attr_type = "TYPE"
            attr_str = ":attr {0}: {2}\n:type {0}: {1}\n".format(
                attribute, attr_type, expression)
            docstring += attr_str

    docstring += "\n"
    return docstring
