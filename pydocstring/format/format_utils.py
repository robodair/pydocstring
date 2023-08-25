"""Provides helper utilities for formatting"""

from typing import List
from data_structures import AttrDetails, FunctionDetails, ReturnDetails

from pydocstring.format.docstring_styles import FormatTemplate


def format_params(function_details: FunctionDetails, format_template: FormatTemplate) -> str:
    docstring = format_template.start_args_block

    if function_details.args:
        docstring += format_template.param_placeholder_args.format(function_details.args, "Variable length argument list.")
    
    if function_details.kwargs:
        docstring += format_template.param_placeholder_kwargs.format(function_details.kwargs, "Arbitrary keyword arguments.")

    for param in function_details.params:
        default = " default: ``{0}``".format(param.default) if param.default else ""
        docstring += format_template.param_placeholder.format(param.name, param.type, default)
    
    return docstring


def format_returns(returns: List[ReturnDetails], format_template: FormatTemplate) -> str:
    docstring = format_template.start_return_block

    for ret in returns:
        docstring += format_template.return_placeholder.format(ret.type, ret.expression)

    return docstring


def format_annotation(annotation: str, format_template: FormatTemplate) -> str:
    docstring = format_template.start_return_block

    docstring += format_template.return_annotation_placeholder.format(annotation)

    return docstring


def format_yields(yields: List[ReturnDetails], format_template: FormatTemplate) -> str:
    docstring = format_template.start_yield_block

    for yie in yields:
        docstring += format_template.yield_placeholder.format(yie.type, yie.expression)
    
    return docstring


def format_raises(raises: List[str], format_template: FormatTemplate) -> str:
    docstring = format_template.start_raise_block

    for exception in raises:
        docstring += format_template.raise_placeholder.format(exception)
    
    return docstring


def format_attributes(attributes: List[AttrDetails], format_template: FormatTemplate) -> str:
    docstring = format_template.start_attributes

    for attr in attributes:
        docstring += format_template.attribute_placeholder.format(attr.name, attr.type, attr.code)
    
    return docstring
