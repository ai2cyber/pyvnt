from typing import List, Sequence, TypeVar

from pyvnt.transformer import Transformer

_TIn = TypeVar("_TIn")
_TOut = TypeVar("_TOut")


def sequence_transformer(transformer: Transformer[_TIn, _TOut]) -> Transformer[Sequence[_TIn], List[_TOut]]:
    """Transforms a `sequence` object to list and back.

    Args:
        transformer (Transformer[T, Any]): Transformation to apply to every item of the `sequence`.
    """

    def serializer(value: Sequence[_TIn], property_name: str) -> List[_TOut]:
        transformer.property_name = property_name
        transformed: List[_TOut] = []

        for item in value:
            transformed.append(transformer.serialize(item))

        return transformed

    def deserializer(value: List[_TOut], property_name: str) -> Sequence[_TIn]:
        transformer.property_name = property_name
        transformed: List[_TIn] = []

        for item in value:
            transformed.append(transformer.deserialize(item))

        return transformed

    return Transformer(name="sequence_transformer", serializer=serializer, deserializer=deserializer)
