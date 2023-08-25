import ast
from typing import Optional


def safe_determine_type(string: str) -> Optional[str]:
    """
    Determine the python type of the given literal, for use in docstrings

    Args:
        string (str): The string to evaluate

    Returns:
        ``str``: The type, or "TYPE" if the type could not be determined
    """
    try:
        return ast.literal_eval(string).__class__.__name__
    except ValueError:
        try:
            if string.startswith("set(") or isinstance(
                ast.literal_eval(string.replace("{", "[").replace("}", "]")), list
            ):
                return "set"
        except ValueError:
            return "TYPE"
