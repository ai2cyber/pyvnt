from typing import FrozenSet, List, TypeVar

from pyvnt.transformer import Transformer

_TIn = TypeVar("_TIn")
_TOut = TypeVar("_TOut")


def frozenset_transformer(transformer: Transformer[_TIn, _TOut]) -> Transformer[FrozenSet[_TIn], List[_TOut]]:
    """Transforms a `frozenset` object to list and back.

    Args:
        transformer (Transformer[T, Any]): Transformation to apply to every item of the `frozenset`.
    """

    def serializer(value: FrozenSet[_TIn], property_name: str) -> List[_TOut]:
        transformer.property_name = property_name
        transformed: List[_TOut] = []

        for item in value:
            transformed.append(transformer.serialize(item))

        return transformed

    def deserializer(value: List[_TOut], property_name: str) -> FrozenSet[_TIn]:
        transformer.property_name = property_name
        transformed: List[_TIn] = []

        for item in value:
            transformed.append(transformer.deserialize(item))

        return frozenset(transformed)

    return Transformer(name="frozenset_transformer", serializer=serializer, deserializer=deserializer)
