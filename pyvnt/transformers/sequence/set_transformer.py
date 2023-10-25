from typing import List, Set, TypeVar

from pyvnt.transformer import Transformer

_TIn = TypeVar("_TIn")
_TOut = TypeVar("_TOut")


def set_transformer(transformer: Transformer[_TIn, _TOut]) -> Transformer[Set[_TIn], List[_TOut]]:
    """Transforms a `set` object to list and back.

    Args:
        transformer (Transformer[T, Any]): Transformation to apply to every item of the `set`.
    """

    def serializer(value: Set[_TIn], property_name: str) -> List[_TOut]:
        transformer.property_name = property_name
        transformed: List[_TOut] = []

        for item in value:
            transformed.append(transformer.serialize(item))

        return transformed

    def deserializer(value: List[_TOut], property_name: str) -> Set[_TIn]:
        transformer.property_name = property_name
        transformed: List[_TIn] = []

        for item in value:
            transformed.append(transformer.deserialize(item))

        return set(transformed)

    return Transformer(name="set_transformer", serializer=serializer, deserializer=deserializer)
