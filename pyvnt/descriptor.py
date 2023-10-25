from dataclasses import field
from typing import Any, Callable, Dict, List, Optional, TypeVar, overload

from pyvnt.constants import TRANSFORMER_METADATA, VALIDATOR_METADATA
from pyvnt.transformer import Transformer
from pyvnt.transformers.common import self_transformer
from pyvnt.validator import Validator

_T = TypeVar("_T")


@overload
def descriptor(
    *,
    default: _T,
    init: bool = True,
    repr: bool = True,
    hash: Optional[bool] = None,
    compare: bool = True,
    validations: List[Validator[_T]] = [],
    transformations: List[Transformer[_T, Any]] = []
) -> _T:
    ...


@overload
def descriptor(
    *,
    default_factory: Callable[[], _T],
    init: bool = True,
    repr: bool = True,
    hash: Optional[bool] = None,
    compare: bool = True,
    validations: List[Validator[_T]] = [],
    transformations: List[Transformer[_T, Any]] = []
) -> _T:
    ...


@overload
def descriptor(
    *,
    init: bool = True,
    repr: bool = True,
    hash: Optional[bool] = None,
    compare: bool = True,
    validations: List[Validator[Any]] = [],
    transformations: List[Transformer[Any, Any]] = []
) -> Any:
    ...


def descriptor(
    *,
    default: Optional[_T] = None,
    default_factory: Optional[Callable[[], _T]] = None,
    init: bool = True,
    repr: bool = True,
    hash: Optional[bool] = None,
    compare: bool = True,
    validations: List[Validator[_T]] = [],
    transformations: List[Transformer[_T, Any]] = []
) -> _T:
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
