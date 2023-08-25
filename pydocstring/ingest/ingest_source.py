import parso
from parso.python.tree import BaseNode, search_ancestor
from typing import Iterable, Optional, Tuple

from pydocstring import exc
from pydocstring.data_structures import IngestedDetails
from pydocstring.ingest.unpack_parso import unpack_class, unpack_function, unpack_module


def select_node_at_position(tree: BaseNode, position: Tuple[int, int]) -> BaseNode:
    try:
        leaf = tree.get_leaf_for_position(position, include_prefixes=True)
    except ValueError as e:
        leaf = tree
    
    if not leaf:  # pragma: no cover
        raise exc.FailedToIngestError(
            "Could not find leaf at cursor position {}".format(position)
        )

    return leaf


def select_target_node(tree: BaseNode, scopes: Iterable[str]) -> str:
    target = search_ancestor(tree, *scopes)

    if not target:
        if tree.type == "file_input":
            target = tree
        else:  # pragma: no cover
            raise exc.FailedToGenerateDocstringError(
                "Could not find scope of leaf {} ".format(tree)
            )

    return target


def run(source: str, position: Tuple[int, int]) -> Optional[IngestedDetails]:
    """
    Ingests the source text and returns it as structured data with all key components

    Args:
        source (str): the text of the source
        position (tuple): the position of the cursor in the source, row, column. Rows start at 1
            Columns start at 0

    Returns:
       IngestedDetails or None: the source text as structured data, or none if ingestion wasn't possible
    """
    tree = parso.parse(source)
    assert isinstance(tree, BaseNode)

    leaf = select_node_at_position(tree, position)

    unpack_map = {"funcdef": unpack_function, "classdef": unpack_class, "file_input": unpack_module}
    target = select_target_node(leaf, unpack_map.keys())
    return unpack_map[target.type](target)
