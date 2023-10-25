from typing import Any

from pyvnt.transformer import Transformer


def self_transformer() -> Transformer[Any, Any]:
    """Transforms a property to itself and back."""

    def serializer(value: Any, property_name: str):
        return value

    def deserializer(value: Any, property_name: str):
        return value

    return Transformer(name="self_transformer", serializer=serializer, deserializer=deserializer)
