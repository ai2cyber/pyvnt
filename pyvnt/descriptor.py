from dataclasses import field
from typing import Any, Callable, Dict, List, Optional, TypeVar, overload, Union

from pyvnt.constants import TRANSFORMER_METADATA, VALIDATOR_METADATA
from pyvnt.transformer import Transformer
from pyvnt.transformers.common import self_transformer
from pyvnt.validator import Validator

_T = TypeVar("_T")

def descriptor(
    default: Union[_T,Optional[_T]] = None,
    default_factory: Union[Optional[Callable[[], _T]], Callable[[], _T]] = None,
    init: bool = True,
    repr: bool = True,
    hash: Optional[bool] = None,
    compare: bool = True,
    validations: Union[List[Validator[Union[_T,Any]]], List[Validator[_T]]] = [],
    transformations: List[Transformer[Union[_T,Any], Any]] = []
) -> Union[_T, Any]:
    args: Dict[str, Any] = {
        "init": init,
        "repr": repr,
        "hash": hash,
        "compare": compare,
        "metadata": {VALIDATOR_METADATA: validations, TRANSFORMER_METADATA: [self_transformer()] + transformations},
    }

    if default is not None:
        args["default"] = default
    elif default_factory is not None:
        args["default_factory"] = default_factory

    return field(**args)
