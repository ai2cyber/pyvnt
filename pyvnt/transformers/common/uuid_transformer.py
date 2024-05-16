from uuid import UUID

from pyvnt.transformer import Transformer


def uuid_transformer() -> Transformer[UUID, str]:
    """Transforms a `UUID` object to string and back."""

    def serializer(value: UUID, property_name: str):
        return str(value)

    def deserializer(value: str, property_name: str):
        return UUID(value)

    return Transformer(name="uuid_transformer", serializer=serializer, deserializer=deserializer)
