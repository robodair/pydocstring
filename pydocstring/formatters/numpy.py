"""
Numpy Docstring Formatter
"""


def function_docstring(params, return_type, exceptions, return_statements):
    """
    Format a Numpy docstring for a function

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
        docstring += "\n\nParameters\n----------\n"
        for param_name in params:
            param = params[param_name]
            param_type = param['type'] if param['type'] else "TYPE"
            param_default = "default: ``" + \
                param['default'] + "``" if param['default'] else ""
            param_str = "{0} : {1}\n    {2}\n".format(
                param_name, param_type, param_default)
            docstring += param_str

    if return_type and return_statements:
        docstring += "\n\nReturns\n-------\n"
        docstring += "{0}\n    {1}\n".format(return_type,
                                             return_statements[0][1])
    elif return_type:
        docstring += "\n\nReturns\n-------\n"
        docstring += "{0}\n    \n".format(return_type)
    elif return_statements:
        if return_statements[0][0] == "yield":
            docstring += "\n\nYields\n------\n"
        else:
            docstring += "\n\nReturns\n-------\n"
        docstring += "{0}\n    {1}\n".format("TYPE", return_statements[0][1])

    if exceptions:
        docstring += "\n\nRaises\n------\n"
        for exception in exceptions:
            docstring += "{0}\n    \n".format(exception)

    docstring += "\n"
    return docstring


def class_docstring(attributes):
    """
    Format a Numpy docstring for a class

    Only accepts attributes, ``__init__`` method args can be documented on the ``__init__`` method

    Args:
        attributes (list of tuples): attribute names, expression and type (or None)

    Returns:
        str: The formatted docstring

    """
    docstring = "\n"

    if attributes:
        docstring += "\n\nAttributes\n----------\n"
        for attribute, expression, attr_type in attributes:
            if not attr_type:
                attr_type = "TYPE"
            attr_str = "{0} : {1}\n    {2}\n".format(
                attribute, attr_type, expression)
            docstring += attr_str

    docstring += "\n"
    return docstring


def module_docstring(attributes):
    """
    Format a Numpy docstring for a module

    Only accepts attributes, ``__init__`` method args can be documented on the ``__init__`` method

    Args:
        attributes (list of tuples): attribute names, expression and type (or None)

    Returns:
        str: The formatted docstring

    """
    docstring = "\n"

    if attributes:
        docstring += "\n\nAttributes\n----------\n"
        for attribute, expression, attr_type in attributes:
            if not attr_type:
                attr_type = "TYPE"
            attr_str = "{0} : {1}\n    {2}\n".format(
                attribute, attr_type, expression)
            docstring += attr_str

    docstring += "\n"
    return docstring
