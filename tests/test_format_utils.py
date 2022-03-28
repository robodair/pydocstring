from pathlib import Path

import pydocstring.format_utils as tested

DATA = Path(__file__).parent / "data"


def test_parse_footer():
    footer = """\
       Returns:
           TYPE: an existing returns description
    """
    returns, raises, yields, footer = tested.parse_footer(footer)
    assert (
        returns
        == "       Returns:\n           TYPE: an existing returns description\n    "
    )

    assert raises is None
    assert yields is None
    assert footer is None
