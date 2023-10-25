from datetime import datetime

from pyvnt.transformer import Transformer


def datetime_transformer() -> Transformer[datetime, str]:
    """Transforms a `datetime` object to string and back."""

    def serializer(value: datetime, property_name: str) -> str:
        return value.isoformat()

    def deserializer(value: str, property_name: str) -> datetime:
        return datetime.fromisoformat(value)

    return Transformer(name="datetime_transformer", serializer=serializer, deserializer=deserializer)
