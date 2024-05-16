from enum import Enum
from typing import Any, Type, TypeVar

from pyvnt.transformer import Transformer

_T = TypeVar("_T", bound=Enum)


def enum_transformer(cls: Type[_T]) -> Transformer[_T, Any]:
    """Transforms an `Enum` object to string and back.

    Args:
        cls (Type[_T]): The enumeration type of the property.
    """

    def serializer(value: _T, property_name: str):
        return value.value

    def deserializer(value: Any, property_name: str):
        return cls(value)

    return Transformer(name="enum_transfer", serializer=serializer, deserializer=deserializer)
