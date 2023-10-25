from typing import Any, Dict, Type, TypeVar

from pyvnt.instance import EntityInstance
from pyvnt.transformer import Transformer

T = TypeVar("T", bound=EntityInstance)


def nested_transformer(cls: Type[T]) -> Transformer[T, Dict[str, Any]]:
    """Transforms a nested property with its own transformers.

    Args:
        cls (Type[T]): The type of the nested property.
    """

    def serializer(value: T, property_name: str) -> Dict[str, Any]:
        return value.serialize()

    def deserializer(value: Dict[str, Any], property_name: str) -> T:
        return cls.deserialize(value, False)

    return Transformer(name="nested_transformer", serializer=serializer, deserializer=deserializer)
