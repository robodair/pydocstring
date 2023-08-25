from dataclasses import dataclass
from strenum import StrEnum

from pydocstring import exc

class DocstringStyle(StrEnum):
    GOOGLE = "google"
    NUMPY = "numpy"
    REST = "reST"

    @classmethod
    def list_values(cls):
        return [x.value for x in cls]


@dataclass
class FormatTemplate:
    start_args_block: str
    param_placeholder: str
    param_placeholder_args: str
    param_placeholder_kwargs: str
    start_return_block: str
    return_placeholder: str
    return_annotation_placeholder: str
    start_yield_block: str
    yield_placeholder: str
    start_raise_block: str
    raise_placeholder: str
    start_attributes: str
    attribute_placeholder: str


TEMPLATE_MAP = {
    DocstringStyle.GOOGLE: FormatTemplate(
        start_args_block="\n\nArgs:\n",
        param_placeholder="    {0} ({1}): {2}\n",
        param_placeholder_args="    *{0}: {1}\n",
        param_placeholder_kwargs="    **{0}: {1}\n",
        start_return_block="\n\nReturns:\n",
        return_placeholder="    {0}: {1}\n",
        return_annotation_placeholder="    {0}: \n",
        start_yield_block="\n\nYields:\n",
        yield_placeholder="    {0}: {1}\n",
        start_raise_block="\n\nRaises:\n",
        raise_placeholder="    {0}: \n",
        start_attributes="\n\nAttributes:\n",
        attribute_placeholder="    {0} ({1}): {2}\n",
    ),
    DocstringStyle.NUMPY: FormatTemplate(
        start_args_block="\n\n    Parameters\n    ----------\n",
        param_placeholder="    {0} : {1}\n        {2}\n",
        param_placeholder_args="    *{0}\n        {1}\n",
        param_placeholder_kwargs="    **{0}\n        {1}\n",
        start_return_block="\n\n    Returns\n    -------\n",
        return_placeholder="    {0}\n        {1}\n",
        return_annotation_placeholder="    {0}\n        \n",
        start_yield_block="\n\n    Yields\n    ------\n",
        yield_placeholder="    {0}\n        {1}\n",
        start_raise_block="\n\n    Raises\n    ------\n",
        raise_placeholder="    {0}\n        \n",
        start_attributes="\n\n    Attributes\n    ----------\n",
        attribute_placeholder="    {0} : {1}\n        {2}\n",
    ),
    DocstringStyle.REST: FormatTemplate(
        start_args_block="\n\n",
        param_placeholder=":param {0}: {2}\n:type {0}: {1}\n",
        param_placeholder_args=":param *{0}: {1}\n",
        param_placeholder_kwargs=":param **{0}: {1}\n",
        start_return_block="\n\n",
        return_placeholder=":return: {1}\n:rtype: {0}\n",
        return_annotation_placeholder=":return: \n:rtype: {0}\n",
        start_yield_block="\n\n",
        yield_placeholder=":yields: {1}\n:ytype: {0}\n",
        start_raise_block="\n\n",
        raise_placeholder=":raises {0}: \n",
        start_attributes="\n\n",
        attribute_placeholder=":var {0}: {2}\n:type {0}: {1}\n",
    ),
}


def get_style_template(style: DocstringStyle) -> FormatTemplate:
    """
    Args:
        style (DocstringStyle): the format of the docstring choose from google, numpy, reST.

    Raises:
        exc.InvalidFormatter: If the value provided to `formatter` is not a supported
            formatter name
    
    Returns:
       FormatTemplate: the template for generating a docstring in a chosen style
    """

    if style not in TEMPLATE_MAP:
        raise exc.InvalidFormatterError("Failed to find template for: {}".format(style))
    
    return TEMPLATE_MAP[style]
