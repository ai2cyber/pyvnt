from typing import Any, Generic, Optional, TypeVar

from pyvnt.exceptions import TransformationException
from pyvnt.utilities import Deserializer, Serializer

TIn = TypeVar("TIn")
TOut = TypeVar("TOut")
TChainOut = TypeVar("TChainOut")


class Transformer(Generic[TIn, TOut]):
    def __init__(
        self,
        name: str,
        serializer: Serializer[TIn, TOut],
        deserializer: Deserializer[TIn, TOut],
        property_name: Optional[str] = None,
    ) -> None:
        self.name: str = name
        self.serializer: Serializer[TIn, TOut] = serializer
        self.deserializer: Deserializer[TIn, TOut] = deserializer

        self.property_name: Optional[str] = property_name

    def serialize(self, value: TIn) -> TOut:
        if not self.property_name:
            raise Exception("Transformer called without a property name. Something went wrong in the initialization.")

        try:
            return self.serializer(value, self.property_name)
        except Exception as e:
            raise TransformationException(self.name, f'Failed to serialize property "{self.property_name}".', e)

    def deserialize(self, value: TOut) -> TIn:
        if not self.property_name:
            raise Exception("Transformer called without a property name. Something went wrong in the initialization.")

        try:
            return self.deserializer(value, self.property_name)
        except Exception as e:
            raise TransformationException(self.name, f'Failed to deserialize property "{self.property_name}".', e)

    def chain(self, transformer: "Transformer[TOut, TChainOut]") -> "Transformer[TIn, TChainOut]":
        def serializer(value: TIn, property_name: str) -> TChainOut:
            return transformer.serializer(self.serializer(value, property_name), property_name)

        def deserializer(value: TChainOut, property_name: str) -> TIn:
            return self.deserializer(transformer.deserializer(value, property_name), property_name)

        return Transformer(f"{self.name}->{transformer.name}", serializer, deserializer)

    @classmethod
    def compose(cls, *transformers: "Transformer[Any, Any]", property_name: str) -> "Transformer[Any, Any]":
        def serializer(value: Any, property_name: str):
            input_value = value

            for transformer in transformers:
                transformer.property_name = property_name
                input_value = transformer.serialize(input_value)

            return input_value

        def deserializer(value: Any, property_name: str):
            input_value = value

            for transformer in transformers:
                transformer.property_name = property_name
                input_value = transformer.deserialize(input_value)

            return input_value

        return Transformer(
            name="composed",
            serializer=serializer,
            deserializer=deserializer,
            property_name=property_name,
        )
