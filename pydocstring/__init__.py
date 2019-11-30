"""
Top level API - all you need to integrate with an editor, just call
:py:func:`pydocstring.generate_docstring` with the source code and the position of your cursor.
"""

__version__ = "0.2.0"

import parso
from parso.python.tree import search_ancestor, BaseNode
from pydocstring import exc, formatters

def generate_docstring(source, position=(1, 0), formatter="google", autocomplete=False):
    """Generate a docstring

    Args:
        source (str): the text of the source
        position (tuple): the position of the cursor in the source, row, column. Rows start at 1
            Columns start at 0
        formatter (str): the format of the docstring choose from google, numpy, reST.
        autocomplete (bool): Whether or not to remove three characters from before the position prior
            to parsing the code. THis is to remove the \"\"\" before a docstring default: False

    Raises:
        exc.InvalidFormatter: If the value provided to `formatter` is not a supported
            formatter name

    Returns:
       str or None: docstring, excluding quotation marks, or None, if one could not be generated
    """
    if autocomplete:
        lines = source.splitlines(True)
        # all full lines before the one the position is on
        lines_before = lines[:position[0] - 1]
        # position in buffer is length of all those lines + the column position (starting at 0)
        bufferpos = sum(len(l) for l in lines_before) + position[1]
        # Splice the desired bits of the source together
        slice1 = source[:bufferpos - 3]
        slice2 = source[bufferpos:]
        source = slice1 + slice2
        # Shift the position to account for the removed quotes
        position = (position[0], position[1] - 3)

    tree = parso.parse(source)
    assert isinstance(tree, BaseNode)
    try:
        leaf = tree.get_leaf_for_position(position, include_prefixes=True)
    except ValueError as e:
        leaf = tree
    if not leaf:  # pragma: no cover
        raise exc.FailedToGenerateDocstringError(
            "Could not find leaf at cursor position {}".format(position))
    scopes = ('classdef', 'funcdef', 'file_input')
    scope = search_ancestor(leaf, *scopes)
    if not scope:
        if leaf.type == 'file_input':
            scope = leaf
        else:  # pragma: no cover
            raise exc.FailedToGenerateDocstringError(
                "Could not find scope of leaf {} ".format(leaf))

    formatter_module = formatters.get(formatter)
    if scope.type == 'classdef':
        return formatter_module.class_docstring(scope)
    elif scope.type == 'funcdef':
        return formatter_module.function_docstring(scope)
    elif scope.type == 'file_input':
        return formatter_module.module_docstring(scope)

    raise exc.FailedToGenerateDocstringError(
        "Failed to generate Docstring for: {}".format(scope)) # pragma: no cover
