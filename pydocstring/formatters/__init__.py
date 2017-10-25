"""
pydocstring formatters, use :py:func:get() to get the formatter you want
"""
from pydocstring.formatters import google, numpy, reST
from pydocstring.exc import InvalidFormatterError
_formatter_map = {
    "google": google,
    "numpy": numpy,
    "rest": reST
}

def get(formatter_type):
    """Return the requested formatter"""
    formatter_type = formatter_type.lower()
    if formatter_type not in _formatter_map: #pragma: no cover
        raise InvalidFormatterError(formatter_type)
    return _formatter_map[formatter_type]
