from typing import Any, Dict, overload

from pyvnt.transformer import TIn, TOut, Transformer
from pyvnt.transformers.common import self_transformer


@overload
def dict_transformer() -> Transformer[Dict[Any, Any], Dict[str, Any]]:
    ...


@overload
def dict_transformer(*, key_transformer: Transformer[TIn, str]) -> Transformer[Dict[TIn, Any], Dict[str, Any]]:
    ...


@overload
def dict_transformer(*, value_transformer: Transformer[TOut, Any]) -> Transformer[Dict[Any, TOut], Dict[str, Any]]:
    ...


@overload
def dict_transformer(
    *,
    key_transformer: Transformer[TIn, str],
    value_transformer: Transformer[TOut, Any],
) -> Transformer[Dict[TIn, TOut], Dict[str, Any]]:
    ...


def dict_transformer(
    *,
    key_transformer: Transformer[TIn, str] = self_transformer(),
    value_transformer: Transformer[TOut, Any] = self_transformer(),
) -> Transformer[Dict[TIn, TOut], Dict[str, Any]]:
    """Transforms a dictionary object to another dictionary object and back.

    Args:
        key_transformer (Transformer[TIn, str], optional): Optional transformer for the keys of the dictionary. Defaults to self_transformer().
        value_transformer (Transformer[TOut, Any], optional): Optional transformer for the values of the dictionary. Defaults to self_transformer().
    """  # noqa

    def serializer(value: Dict[TIn, TOut], property_name: str) -> Dict[str, Any]:
        key_transformer.property_name = property_name
        value_transformer.property_name = property_name
        transformed: Dict[str, Any] = {}

        for item in value:
            transformed[key_transformer.serialize(item)] = value_transformer.serialize(value[item])

        return transformed

    def deserializer(value: Dict[str, Any], property_name: str) -> Dict[TIn, TOut]:
        key_transformer.property_name = property_name
        value_transformer.property_name = property_name
        transformed: Dict[TIn, TOut] = {}

        for item in value:
            transformed[key_transformer.deserialize(item)] = value_transformer.deserialize(value[item])

        return transformed

    return Transformer(name="dict_transformer", serializer=serializer, deserializer=deserializer)
