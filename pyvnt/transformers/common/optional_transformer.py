from typing import Optional, TypeVar

from pyvnt.transformer import Transformer

TIn = TypeVar("TIn")
TOut = TypeVar("TOut")


def optional_transformer(transformer: Transformer[TIn, TOut]) -> Transformer[Optional[TIn], Optional[TOut]]:
    def serializer(value: Optional[TIn], property_name: str) -> Optional[TOut]:
        transformer.property_name = property_name
        return transformer.serialize(value) if value is not None else None

    def deserializer(value: Optional[TOut], property_name: str) -> Optional[TIn]:
        transformer.property_name = property_name
        return transformer.deserialize(value) if value is not None else None

    return Transformer("optional_transformer", serializer, deserializer)
