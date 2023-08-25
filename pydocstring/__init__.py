"""
Top level API - all you need to integrate with an editor, just call
:py:func:`pydocstring.generate_docstring` with the source code and the position of your cursor.
"""

__version__ = "0.2.1"


from typing import Tuple
from pydocstring.format.docstring_styles import DocstringStyle
from pydocstring.format import format_docstring
from pydocstring.ingest import ingest_source


def remove_characters_from_source(source: str, position: Tuple[int, int], num_to_remove: int) -> str:
    lines = source.splitlines(True)
    
    # all full lines before the one the position is on
    lines_before = lines[: position[0] - 1]
    
    # position in buffer is length of all those lines + the column position (starting at 0)
    bufferpos = sum(len(l) for l in lines_before) + position[1]
    
    # Splice the desired bits of the source together
    slice1 = source[: bufferpos - num_to_remove]
    slice2 = source[bufferpos:]
    return slice1 + slice2


def generate_docstring(
    source: str, position: Tuple[int, int] = (1, 0), formatter: DocstringStyle = "google", autocomplete: bool = False
):
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
        num_remove = 3
        source = remove_characters_from_source(source, position, num_remove)

        # Shift the position to account for the removed quotes
        # ToDo: what happens if position[1] becomes negative?
        position = (position[0], position[1] - num_remove)

    structured_input = ingest_source.run(source, position)
    return format_docstring.run(structured_input, formatter)