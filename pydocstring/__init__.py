"""
Python package for autogeneration of docstrings
"""

from pydocstring import _version
from pydocstring import parse_utils
from pydocstring.document import Document
from pydocstring import exc


__version__ = _version.public_version

def generate_docstring(document, position=0, formatter="Google"):
    """Generate a docstring

    Args:
       document (str): the text of the document
       position: (int): the position of the cursor in the document
       formatter (str): the format of the docstring choose from; `["Google"]`
           (currently only google docstring supported)

    Raises:
        pydocstring.exec.InvalidFormatter: If the value provided to `formatter` is not a supported
            formatter name

    Returns:
       str or None: The contents of the docstring, excluding quotation marks, or None, if one could
           not be generated
    """

    if position == 0:
        # scan module for attributes and create docstring
        parse_utils.parse_module_attributes(document)
        raise NotImplementedError("Module Docstring")

    document = Document(document, position)
    decl_range = document.get_block()
    decl = document.get_range(*decl_range)

    if decl.strip().startswith("class"):
        raise NotImplementedError("Is Class")
    elif decl.strip().startswith("def") or decl.strip().startswith("async"):
        params, return_type = parse_utils.parse_function_declaration(decl)
        exceptions = parse_utils.parse_function_exceptions(decl)
        return_statements = parse_utils.parse_return_keyword(decl)

        if formatter == "Google":
            from pydocstring.formatters import google
            return google.function_docstring(params, return_type, exceptions, return_statements)
        else:
            raise exc.InvalidFormatter(formatter)
    else:
        return None
