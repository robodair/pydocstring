"""
Google Docstring Formatter
"""


def function_docstring(params, return_type, exceptions, return_statements):
    """
    Format a google docstring

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
        docstring += "\n\nArgs:\n"
        for param_name in params:
            param = params[param_name]
            param_type = " (" +param['type'] + ")" if param['type'] else ""
            param_default = " default: `" + param['default'] + "`" if param['default'] else ""
            param_str = "    {0}{1}:{2}\n".format(
                param_name, param_type, param_default)
            docstring += param_str

    if return_type and return_statements:
        docstring += "\n\nReturns:\n"
        docstring += "    {0}: {1}\n".format(return_type,
                                             return_statements[0][1])
    elif return_type:
        docstring += "\n\nReturns:\n"
        docstring += "    {0}:\n".format(return_type)
    elif return_statements:
        if return_statements[0][0] == "yield":
            docstring += "\n\nYields:\n"
        else:
            docstring += "\n\nReturns:\n"
        docstring += "    {0}: {1}\n".format("TYPE", return_statements[0][1])

    if exceptions:
        docstring += "\n\nRaises:\n"
        for exception in exceptions:
            docstring += "    {0}: \n".format(exception)

    docstring += "\n"
    return docstring
