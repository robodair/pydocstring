from parso.python.tree import (
    Class,
    Function,
    KeywordStatement,
    Module,
    Param,
    Scope,
    ReturnStmt,
    YieldExpr,
)
from typing import Optional, Type, Union

from pydocstring.data_structures import (
    AttrDetails,
    ClassDetails,
    FunctionDetails,
    ModuleDetails,
    ParamDetails,
    ReturnDetails
)
from pydocstring.ingest.ingest_utils import safe_determine_type


def unpack_param(parso_param: Param) -> ParamDetails:
    param_details = ParamDetails(name=parso_param.name.value)

    if parso_param.annotation:
        param_details.type = parso_param.annotation.value
    
    if parso_param.default:
        param_details.default = parso_param.default.get_code()
    
    if param_details.default and not parso_param.annotation:
        param_details.type = safe_determine_type(param_details.default)
    
    return param_details


def unpack_return(parso_return: Union[ReturnStmt, YieldExpr], annotation: Optional[str]) -> ReturnDetails:
    return_details = ReturnDetails()

    if annotation:
        return_details.type = annotation
    
    expression = "".join(x.get_code().strip() for x in parso_return.children[1:])
    return_details.expression = " ".join(expression.split())  # this replaces the newlines with spaces

    return return_details


def unpack_exception_name(parso_exception: KeywordStatement) -> str:
    """
    Find the name of an exception

    Args:
        node: Parso node containing the raises statement

    Returns:
        str: The exception name
    """
    name = parso_exception.children[1]

    while not name.type == "name":
        name = name.children[0]
    
    return name.value


def unpack_function(parso_function: Type[Scope]) -> FunctionDetails:
    assert isinstance(parso_function, Function)

    func_details = FunctionDetails()

    if parso_function.annotation:
        func_details.annotation = parso_function.annotation.value

    for param in parso_function.get_params():
        if param.star_count == 1:
            func_details.args = param.name.value
        elif param.star_count == 2:
            func_details.kwargs = param.name.value
        else:
            func_details.params.append(unpack_param(param))
    
    func_details.returns = list(map(lambda x: unpack_return(x, func_details.annotation), parso_function.iter_return_stmts()))
    func_details.yields = list(map(lambda x: unpack_return(x, func_details.annotation), parso_function.iter_yield_exprs()))
    func_details.raises = list(map(unpack_exception_name, parso_function.iter_raise_stmts()))

    return func_details


def unpack_attribute(node) -> AttrDetails:
    code = node.get_rhs().get_code().strip()
    return AttrDetails(
        name=node.children[0].value,
        code=code,
        type=safe_determine_type(code),
    )


def unpack_class(parso_class) -> ClassDetails:
    assert isinstance(parso_class, Class)

    class_details = ClassDetails()

    for child in parso_class.children:
        if child.type == "suite":
            for grand_child in child.children:
                if grand_child.type == "simple_stmt":
                    for great_grand_child in grand_child.children:
                        if great_grand_child.type == "expr_stmt":
                            class_details.attrs.append(unpack_attribute(great_grand_child))

    return class_details



def unpack_module(parso_module: Scope) -> ModuleDetails:
    assert isinstance(parso_module, Module)

    module_details = ModuleDetails()

    for child in parso_module.children:
        if child.type == "simple_stmt":
            for grand_child in child.children:
                if grand_child.type == "expr_stmt":
                    module_details.attrs.append(unpack_attribute(grand_child))
    
    return module_details
