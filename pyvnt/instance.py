from dataclasses import MISSING
from typing import (
    Any,
    Callable,
    ClassVar,
    Dict,
    Literal,
    Mapping,
    Optional,
    Protocol,
    Tuple,
    Type,
    TypeVar,
    Union,
    overload,
    runtime_checkable,
)

from typing_extensions import Self

from pyvnt.exceptions import ValidationException

_TField = TypeVar("_TField")


@runtime_checkable
class FieldInstance(Protocol[_TField]):
    name: str
    type: Type[_TField]
    default: Union[_TField, Literal[MISSING]]
    default_factory: Union[Callable[[], _TField], Literal[MISSING]]
    init: bool
    repr: bool
    hash: bool
    compare: bool
    metadata: Mapping[Any, Any]


@runtime_checkable
class EntityInstance(Protocol):
    __entity__: ClassVar[bool]
    __dataclass_fields__: ClassVar[Dict[str, FieldInstance[Any]]]

    @overload
    def validate(self, throw: Literal[True] = True) -> Self: ...

    @overload
    def validate(self, throw: Literal[False] = False) -> Tuple[bool, Optional[ValidationException]]: ...

    def validate(self, throw: bool = True) -> Union[Self, Tuple[bool, Optional[ValidationException]]]: ...

    def serialize(self) -> Dict[str, Any]: ...

    @classmethod
    def deserialize(cls, values: Dict[str, Any], validate: bool = True) -> Self: ...
