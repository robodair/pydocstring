"""
Google Docstring Formatter
"""

from more_itertools.more import first
from parso.python.tree import Class, Function, Module

from pydocstring.format_utils import (get_exception_name, get_param_info,
                                      get_return_info, parse_params,
                                      safe_determine_type)


class Param:
    def __init__(self, name="", type="", default="", description=""):
        self.name = name
        self.type = type
        self.default = default
        self.description = description

    @classmethod
    def from_parso(cls, parso_param):
        name, type, default = get_param_info(parso_param)
        name = parso_param.star_count * "*" + name
        return cls(name, type, default)

    @classmethod
    def from_raw_doc(cls, param_paragraph):
        pass


class DocString:
    def __init__(
        self, header="", params={}, returns="", yields="", raises="", footer=""
    ):
        self.header = header
        self.params = params
        self.returns = returns
        self.yields = yields
        self.raises = raises
        self.footer = footer

    @classmethod
    def from_parso_function(cls, parso_function):
        return cls(
            params={
                param.name.value: Param.from_parso(param)
                for param in parso_function.get_params()
            },
            returns=list(parso_function.iter_return_stmts()),
            yields=list(parso_function.iter_yield_exprs()),
            raises=list(parso_function.iter_raise_stmts()),
        )

    @classmethod
    def from_raw_doc(cls, doc):
        paragraphs = doc.split("\n\n")
        param_paragraph_index = first(
            [
                index
                for index, paragraph in enumerate(paragraphs)
                if paragraph.lstrip().startswith("Args:")
            ],
            default=None,
        )

        if param_paragraph_index:
            for item in parse_params(paragraphs[param_paragraph_index]).items():
                print(item)

            params = [Param.frow_raw_doc(paragraphs[param_paragraph_index])]
            footer = paragraphs[param_paragraph_index + 1 :]
        else:
            header = doc[3:-3]
            params = []
            footer = ""
        return cls(header=header, params=params, footer=footer)

    def merge(self, other):
        self.header = self.header or other.header
        self.params = self.params or other.params
        self.returns = self.returns or other.returns
        self.yields = self.yields or other.yields
        self.raises = self.raises or other.raises
        self.footer = self.footer or other.footer


def function_docstring(parso_function: Function, formatter):
    """
    Format a docstring for a function

    Args:
        parso_function (Function): The function tree node

    Returns:
        str: The formatted docstring
    """
    assert isinstance(parso_function, Function)

    input_doc = parso_function.get_doc_node()
    if input_doc:
        doc = DocString.from_raw_doc(input_doc.value)
        doc.merge(DocString.from_parso_function(parso_function))
    else:
        doc = DocString.from_parso_function(parso_function)

    docstring = f"{doc.header}\n"

    if doc.params:
        docstring += formatter["start_args_block"]
        for param in doc.params.values():
            # if param.star_count == 1:
            #     docstring += formatter["param_placeholder_args"].format(
            #         param.name.value, "Variable length argument list."
            #     )
            # elif param.star_count == 2:
            #     docstring += formatter["param_placeholder_kwargs"].format(
            #         param.name.value, "Arbitrary keyword arguments."
            #     )
            # else:
            docstring += formatter["param_placeholder"].format(
                param.name, param.type, param.default
            )

    if doc.returns:
        docstring += formatter["start_return_block"]
        for ret in doc.returns:
            docstring += formatter["return_placeholder"].format(
                *get_return_info(ret, parso_function.annotation)
            )
    # TODO: how to handle this with merge
    elif parso_function.annotation:
        docstring += formatter["start_return_block"]
        docstring += formatter["return_annotation_placeholder"].format(
            parso_function.annotation.value
        )

    if doc.yields:
        docstring += formatter["start_yield_block"]
        for yie in doc.yields:
            docstring += formatter["yield_placeholder"].format(
                *get_return_info(yie, parso_function.annotation)
            )

    if doc.raises:
        docstring += formatter["start_raise_block"]
        for exception in doc.raises:
            docstring += formatter["raise_placeholder"].format(
                get_exception_name(exception)
            )

    docstring += "\n"
    return docstring


def class_docstring(parso_class, formatter):
    """
    Format a docstring for a class

    Only documents attributes, ``__init__`` method args can be documented on the ``__init__``
        method

    Args:
        parso_class (Class): The class tree node

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
        docstring += formatter["start_attributes"]
        for attribute in attribute_expressions:
            name = attribute.children[0].value
            code = attribute.get_rhs().get_code().strip()
            attr_type = safe_determine_type(code)
            attr_str = formatter["attribute_placeholder"].format(name, attr_type, code)
            docstring += attr_str

    docstring += "\n"
    return docstring


def module_docstring(parso_module, formatter):
    """
    Format a docstring for a module

    Only documents attributes, ``__init__`` method args can be documented on the ``__init__``
        method

    Args:
        parso_module (Module): The module tree node

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
        docstring += formatter["start_attributes"]
        for attribute in attribute_expressions:
            name = attribute.children[0].value
            code = attribute.get_rhs().get_code().strip()
            attr_type = safe_determine_type(code)
            attr_str = formatter["attribute_placeholder"].format(name, attr_type, code)
            docstring += attr_str

    docstring += "\n"
    if not docstring.strip():
        docstring = "\n\nEmpty Module\n\n"
    return docstring
