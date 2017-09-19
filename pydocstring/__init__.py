"""
Python package for autogeneration of docstrings
"""

from pydocstring import _version
from pydocstring import parse_utils
from pydocstring.document import Document
from pydocstring import exc
from pydocstring.formatters import google, numpy, reST


__version__ = _version.public_version


def generate_docstring(source, position=0, formatter="Google"):  # pragma: no cover
    """Generate a docstring

    Args:
       source (str): the text of the source
       position: (int): the position of the cursor in the source
       formatter (str): the format of the docstring choose from; `["Google"]`
           (currently only google docstring supported)

    Raises:
        pydocstring.exec.InvalidFormatter: If the value provided to `formatter` is not a supported
            formatter name

    Returns:
       str or None: The contents of the docstring, excluding quotation marks, or None, if one could
           not be generated
    """
    formatter = formatter.lower()

    formatter_module = None
    if formatter == "google":
        formatter_module = google
    elif formatter == "numpy":
        formatter_module = numpy
    elif formatter == "rest":
        formatter_module = reST
    else:
        raise exc.InvalidFormatter(formatter)

    if position == 0:
        # scan module for attributes and create docstring
        module_attributes = parse_utils.parse_module_attributes(source)
        return formatter_module.module_docstring(module_attributes)

    document = Document(source, position)
    decl_range = document.get_block()
    decl = document.get_range(*decl_range)

    if decl.strip().startswith("class"):
        class_attributes = parse_utils.parse_class_attributes(decl)
        return formatter_module.class_docstring(class_attributes)
    elif decl.strip().startswith("def") or decl.strip().startswith("async"):
        params, return_type = parse_utils.parse_function_declaration(decl)
        exceptions = parse_utils.parse_function_exceptions(decl)
        return_statements = parse_utils.parse_return_keyword(decl)
        return formatter_module.function_docstring(params, return_type, exceptions, return_statements)
    else:
        return None
