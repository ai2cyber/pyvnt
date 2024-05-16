from typing import Any, Dict, Mapping, overload

from pyvnt.transformer import TIn, TOut, Transformer
from pyvnt.transformers.common import self_transformer


@overload
def mapping_transformer() -> Transformer[Mapping[Any, Any], Mapping[str, Any]]:
    ...


@overload
def mapping_transformer(*, key_transformer: Transformer[TIn, str]) -> Transformer[Mapping[TIn, Any], Mapping[str, Any]]:
    ...


@overload
def mapping_transformer(
    *, value_transformer: Transformer[TOut, Any]
) -> Transformer[Mapping[Any, TOut], Mapping[str, Any]]:
    ...


@overload
def mapping_transformer(
    *,
    key_transformer: Transformer[TIn, str],
    value_transformer: Transformer[TOut, Any],
) -> Transformer[Mapping[TIn, TOut], Mapping[str, Any]]:
    ...


def mapping_transformer(
    *,
    key_transformer: Transformer[TIn, str] = self_transformer(),
    value_transformer: Transformer[TOut, Any] = self_transformer(),
) -> Transformer[Mapping[TIn, TOut], Mapping[str, Any]]:
    """Transforms a mapping object to another dictionary object and back.

    Args:
        key_transformer (Transformer[TIn, str], optional): Optional transformer for the keys of the mapping. Defaults to self_transformer().
        value_transformer (Transformer[TOut, Any], optional): Optional transformer for the values of the mapping. Defaults to self_transformer().
    """  # noqa

    def serializer(value: Mapping[TIn, TOut], property_name: str) -> Dict[str, Any]:
        key_transformer.property_name = property_name
        value_transformer.property_name = property_name
        transformed: Dict[str, Any] = {}

        for item in value:
            transformed[key_transformer.serialize(item)] = value_transformer.serialize(value[item])

        return transformed

    def deserializer(value: Mapping[str, Any], property_name: str) -> Mapping[TIn, TOut]:
        key_transformer.property_name = property_name
        value_transformer.property_name = property_name
        transformed: Dict[TIn, TOut] = {}

        for item in value:
            transformed[key_transformer.deserialize(item)] = value_transformer.deserialize(value[item])

        return transformed

    return Transformer(name="mapping_transformer", serializer=serializer, deserializer=deserializer)
