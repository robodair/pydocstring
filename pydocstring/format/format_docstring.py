"""
Docstring Formatter
"""

from pydocstring import exc
from pydocstring.data_structures import (
    ClassDetails,
    FunctionDetails,
    IngestedDetails,
    ModuleDetails
)
from pydocstring.format.docstring_styles import (
    DocstringStyle,
    FormatTemplate,
    get_style_template
)
from pydocstring.format.format_utils import (
    format_annotation,
    format_attributes,
    format_params,
    format_raises,
    format_returns,
    format_yields,
)


def format_function(function_details: FunctionDetails, format_template: FormatTemplate) -> str:
    docstring = "\n"

    if function_details.has_parameters():
        docstring += format_params(function_details, format_template)

    if function_details.returns:
        docstring += format_returns(function_details.returns, format_template)
    elif function_details.annotation:
        docstring += format_annotation(function_details.annotation, format_template)

    if function_details.yields:
        docstring += format_yields(function_details.yields, format_template)

    if function_details.raises:
        docstring += format_raises(function_details.raises, format_template)

    docstring += "\n"
    return docstring


def format_class(class_details: ClassDetails, format_template: FormatTemplate) -> str:
    docstring = "\n"

    if class_details.attrs:
        docstring += format_attributes(class_details.attrs, format_template)
    
    docstring += "\n"
    return docstring


def format_module(module_details: ModuleDetails, format_template: FormatTemplate) -> str:
    docstring = "\n"

    if module_details.attrs:
        docstring += format_attributes(module_details.attrs, format_template)
    
    docstring += "\n"

    if not docstring.strip():
        return "\n\nEmpty Module\n\n"

    return docstring


def run(structured_data: IngestedDetails, style: DocstringStyle) -> str:
    template = get_style_template(style)

    if isinstance(structured_data, FunctionDetails):
        return format_function(structured_data, template)

    elif isinstance(structured_data, ClassDetails):
        return format_class(structured_data, template)

    elif isinstance(structured_data, ModuleDetails):
        return format_module(structured_data, template)

    raise exc.FailedToGenerateDocstringError(
        "Failed to generate Docstring for: {}".format(structured_data)
    )  # pragma: no cover
