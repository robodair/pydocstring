"""
Google Docstring Formatter
"""

from collections import OrderedDict
from textwrap import dedent

from more_itertools.more import first
from parso.python.tree import Class, Function, Module

from pydocstring.format_utils import (get_exception_name, get_param_info,
                                      get_return_info, parse_footer,
                                      parse_params, safe_determine_type)


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

    def __str__(self):
        return dedent(
            f"""\
Param(name={self.name},
      type={self.type},
      default={self.default},
      description={self.description})"""
        )


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
            params=OrderedDict(
                [
                    (param.name.value, Param.from_parso(param))
                    for param in parso_function.get_params()
                ]
            ),
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
            header = "\n\n".join(paragraphs[:param_paragraph_index])[3:]
            params = [
                Param(name=name, type=type_, description=description)
                for name, type_, description in parse_params(
                    paragraphs[param_paragraph_index]
                )
            ]
            params = OrderedDict([param.name, param] for param in params)
            footer = "\n\n".join(paragraphs[param_paragraph_index + 1 :])[:-3]
        else:
            header = doc[3:-3]
            params = []
            footer = ""

        returns, raises, yields, footer = parse_footer(footer)
        return cls(
            header=header,
            params=params,
            returns=returns,
            raises=raises,
            yields=yields,
            footer=footer,
        )

    def merge(self, other):
        """Merge both docstring objects.

        If a param exists in the second docstring, it will override the one from the first one.
        """
        self.header = self.header or other.header

        for key in self.params.keys():
            if key in other.params:
                self.params[key].description = other.params[key].description
                self.params[key].type = other.params[key].type
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
        doc = DocString.from_parso_function(parso_function)
        doc.merge(DocString.from_raw_doc(input_doc.value))
    else:
        doc = DocString.from_parso_function(parso_function)

    docstring = f"{doc.header}\n"

    if doc.params:
        docstring += formatter["start_args_block"]
        for param in doc.params.values():
            if param.name.startswith("*"):
                docstring += formatter["param_placeholder_args"].format(
                    param.name,
                    "Arbitrary keyword arguments."
                    if param.name.startswith("**")
                    else "Variable length argument list.",
                )
            else:
                docstring += formatter["param_placeholder"](
                    param.name, param.type, param.default, param.description
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
