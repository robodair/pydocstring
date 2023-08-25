from dataclasses import dataclass, field
from typing import List, Optional, Union


@dataclass
class ParamDetails:
    name: str
    type: str = "TYPE"
    default: Optional[str] = None


@dataclass
class ReturnDetails:
    type: str = "TYPE"
    expression: str = ""


@dataclass
class FunctionDetails:
    params: List[ParamDetails] = field(default_factory=list)
    args: Optional[str] = None
    kwargs: Optional[str] = None
    returns: List[ReturnDetails] = field(default_factory=list)
    yields: List[ReturnDetails] = field(default_factory=list)
    raises: List[str] = field(default_factory=list)
    annotation: Optional[str] = None

    def has_parameters(self) -> bool:
        return self.params or self.args or self.kwargs
    

@dataclass
class AttrDetails:
    name: str
    code: str
    type: str


@dataclass
class ClassDetails:
    attrs: List[AttrDetails] = field(default_factory=list)


@dataclass
class ModuleDetails:
    attrs: List[AttrDetails] = field(default_factory=list)


IngestedDetails = Union[FunctionDetails, ClassDetails, ModuleDetails]