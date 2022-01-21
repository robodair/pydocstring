"""
Top level API - all you need to integrate with an editor, just call
:py:func:`pydocstring.generate_docstring` with the source code and the position of your cursor.
"""

__version__ = "0.2.1"

import parso
from parso.python.tree import BaseNode, search_ancestor

import pydocstring.formatter
from pydocstring import exc

FORMATTER = {
    "google": {
        "start_args_block": "\n\nArgs:\n",
        "param_placeholder": "    {0} ({1}): {2}\n",
        "param_placeholder_args": "    *{0}: {1}\n",
        "param_placeholder_kwargs": "    **{0}: {1}\n",
        "start_return_block": "\n\nReturns:\n",
        "return_placeholder": "    {0}: {1}\n",
        "return_annotation_placeholder": "    {0}: \n",
        "start_yield_block": "\n\nYields:\n",
        "yield_placeholder": "    {0}: {1}\n",
        "start_raise_block": "\n\nRaises:\n",
        "raise_placeholder": "    {0}: \n",
        "start_attributes": "\n\nAttributes:\n",
        "attribute_placeholder": "    {0} ({1}): {2}\n",
    },
    "numpy": {
        "start_args_block": "\n\n    Parameters\n    ----------\n",
        "param_placeholder": "    {0} : {1}\n        {2}\n",
        "param_placeholder_args": "    *{0}\n        {1}\n",
        "param_placeholder_kwargs": "    **{0}\n        {1}\n",
        "start_return_block": "\n\n    Returns\n    -------\n",
        "return_placeholder": "    {0}\n        {1}\n",
        "return_annotation_placeholder": "    {0}\n        \n",
        "start_yield_block": "\n\n    Yields\n    ------\n",
        "yield_placeholder": "    {0}\n        {1}\n",
        "start_raise_block": "\n\n    Raises\n    ------\n",
        "raise_placeholder": "    {0}\n        \n",
        "start_attributes": "\n\n    Attributes\n    ----------\n",
        "attribute_placeholder": "    {0} : {1}\n        {2}\n",
    },
    "reST": {
        "start_args_block": "\n\n",
        "param_placeholder": ":param {0}: {2}\n:type {0}: {1}\n",
        "param_placeholder_args": ":param *{0}: {1}\n",
        "param_placeholder_kwargs": ":param **{0}: {1}\n",
        "start_return_block": "\n\n",
        "return_placeholder": ":return: {1}\n:rtype: {0}\n",
        "return_annotation_placeholder": ":return: \n:rtype: {0}\n",
        "start_yield_block": "\n\n",
        "yield_placeholder": ":yields: {1}\n:ytype: {0}\n",
        "start_raise_block": "\n\n",
        "raise_placeholder": ":raises {0}: \n",
        "start_attributes": "\n\n",
        "attribute_placeholder": ":var {0}: {2}\n:type {0}: {1}\n",
    },
}


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
        lines_before = lines[: position[0] - 1]
        # position in buffer is length of all those lines + the column position (starting at 0)
        bufferpos = sum(len(l) for l in lines_before) + position[1]
        # Splice the desired bits of the source together
        slice1 = source[: bufferpos - 3]
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
            "Could not find leaf at cursor position {}".format(position)
        )
    scopes = ("classdef", "funcdef", "file_input")
    scope = search_ancestor(leaf, *scopes)
    if not scope:
        if leaf.type == "file_input":
            scope = leaf
        else:  # pragma: no cover
            raise exc.FailedToGenerateDocstringError(
                "Could not find scope of leaf {} ".format(leaf)
            )

    if scope.type == "classdef":
        return pydocstring.formatter.class_docstring(scope, FORMATTER[formatter])
    elif scope.type == "funcdef":
        return pydocstring.formatter.function_docstring(scope, FORMATTER[formatter])
    elif scope.type == "file_input":
        return pydocstring.formatter.module_docstring(scope, FORMATTER[formatter])

    raise exc.FailedToGenerateDocstringError(
        "Failed to generate Docstring for: {}".format(scope)
    )  # pragma: no cover
