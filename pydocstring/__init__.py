"""
Python package for autogeneration of docstrings
"""

from pydocstring import _version
from pydocstring import parse_utils
from pydocstring.document import Document
from pydocstring import exc
from pydocstring.formatters import google


__version__ = _version.public_version

def generate_docstring(document, position=0, formatter="Google"): # pragma: no cover
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
        module_attributes = parse_utils.parse_module_attributes(document)
        return google.module_docstring(module_attributes)

    document = Document(document, position)
    decl_range = document.get_block()
    decl = document.get_range(*decl_range)

    if decl.strip().startswith("class"):
        class_attributes = parse_utils.parse_class_attributes(decl)
        if formatter == "Google":
            return google.class_docstring(class_attributes)
        else:
            raise exc.InvalidFormatter(formatter)
    elif decl.strip().startswith("def") or decl.strip().startswith("async"):
        params, return_type = parse_utils.parse_function_declaration(decl)
        exceptions = parse_utils.parse_function_exceptions(decl)
        return_statements = parse_utils.parse_return_keyword(decl)

        if formatter == "Google":
            return google.function_docstring(params, return_type, exceptions, return_statements)
        else:
            raise exc.InvalidFormatter(formatter)
    else:
        return None
