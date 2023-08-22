"""
Docstring Formatter
"""

from typing import Dict
from parso.python.tree import (
    Class,
    Function,
    Module,
)

from pydocstring.format_utils import (
    get_exception_name,
    get_param_info,
    get_return_info,
    safe_determine_type,
)   


def function_docstring(parso_function, format_template: Dict[str, str]) -> str:
    """
    Format a docstring for a function

    Args:
        parso_function (Function): The function tree node
        format_template (Dict): The specific templates used to construct the docstring

    Returns:
        str: The formatted docstring
    """
    assert isinstance(parso_function, Function)

    docstring = "\n"

    params = parso_function.get_params()
    if params:
        docstring += format_template["start_args_block"]
        for param in params:
            if param.star_count == 1:
                docstring += format_template["param_placeholder_args"].format(
                    param.name.value, "Variable length argument list."
                )
            elif param.star_count == 2:
                docstring += format_template["param_placeholder_kwargs"].format(
                    param.name.value, "Arbitrary keyword arguments."
                )
            else:
                docstring += format_template["param_placeholder"].format(
                    *get_param_info(param)
                )

    returns = list(parso_function.iter_return_stmts())
    if returns:
        docstring += format_template["start_return_block"]
        for ret in returns:
            docstring += format_template["return_placeholder"].format(
                *get_return_info(ret, parso_function.annotation)
            )
    elif parso_function.annotation:
        docstring += format_template["start_return_block"]
        docstring += format_template["return_annotation_placeholder"].format(
            parso_function.annotation.value
        )

    yields = list(parso_function.iter_yield_exprs())
    if yields:
        docstring += format_template["start_yield_block"]
        for yie in yields:
            docstring += format_template["yield_placeholder"].format(
                *get_return_info(yie, parso_function.annotation)
            )

    raises = list(parso_function.iter_raise_stmts())
    if raises:
        docstring += format_template["start_raise_block"]
        for exception in raises:
            docstring += format_template["raise_placeholder"].format(
                get_exception_name(exception)
            )

    docstring += "\n"
    return docstring


def class_docstring(parso_class, format_template: Dict[str, str]) -> str:
    """
    Format a docstring for a class

    Only documents attributes, ``__init__`` method args can be documented on the ``__init__`` method

    Args:
        parso_class (Class): The class tree node
        format_template (Dict): The specific templates used to construct the docstring

    Returns:
        str: The formatted docstring

    """
    assert isinstance(parso_class, Class)
    docstring = "\n"
    attribute_expressions = []

    for child in parso_class.children:
        if child.type == "suite":
            for child2 in child.children:
                if child2.type == "simple_stmt":
                    for child3 in child2.children:
                        if child3.type == "expr_stmt":
                            attribute_expressions.append(child3)

    if attribute_expressions:
        docstring += format_template["start_attributes"]
        for attribute in attribute_expressions:
            name = attribute.children[0].value
            code = attribute.get_rhs().get_code().strip()
            attr_type = safe_determine_type(code)
            attr_str = format_template["attribute_placeholder"].format(name, attr_type, code)
            docstring += attr_str

    docstring += "\n"
    return docstring


def module_docstring(parso_module, format_template: Dict[str, str]) -> str:
    """
    Format a docstring for a module

    Only documents attributes, ``__init__`` method args can be documented on the ``__init__`` method

    Args:
        parso_module (Module): The module tree node
        format_template (Dict): The specific templates used to construct the docstring

    Returns:
        str: The formatted docstring

    """
    assert isinstance(parso_module, Module)
    docstring = "\n"
    attribute_expressions = []

    for child in parso_module.children:
        if child.type == "simple_stmt":
            for child2 in child.children:
                if child2.type == "expr_stmt":
                    attribute_expressions.append(child2)

    if attribute_expressions:
        docstring += format_template["start_attributes"]
        for attribute in attribute_expressions:
            name = attribute.children[0].value
            code = attribute.get_rhs().get_code().strip()
            attr_type = safe_determine_type(code)
            attr_str = format_template["attribute_placeholder"].format(name, attr_type, code)
            docstring += attr_str

    docstring += "\n"
    if not docstring.strip():
        docstring = "\n\nEmpty Module\n\n"
    return docstring
