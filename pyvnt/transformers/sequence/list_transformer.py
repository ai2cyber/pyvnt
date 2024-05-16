from typing import List, TypeVar

from pyvnt.transformer import Transformer

_TIn = TypeVar("_TIn")
_TOut = TypeVar("_TOut")


def list_transformer(transformer: Transformer[_TIn, _TOut]) -> Transformer[List[_TIn], List[_TOut]]:
    """Transforms a `list` object to list and back.

    Args:
        transformer (Transformer[T, Any]): Transformation to apply to every item of the `list`.
    """

    def serializer(value: List[_TIn], property_name: str) -> List[_TOut]:
        transformer.property_name = property_name
        transformed: List[_TOut] = []

        for item in value:
            transformed.append(transformer.serialize(item))

        return transformed

    def deserializer(value: List[_TOut], property_name: str) -> List[_TIn]:
        transformer.property_name = property_name
        transformed: List[_TIn] = []

        for item in value:
            transformed.append(transformer.deserialize(item))

        return transformed

    return Transformer(name="list_transformer", serializer=serializer, deserializer=deserializer)
