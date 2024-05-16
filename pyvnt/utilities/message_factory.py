from typing import Protocol, TypeVar

T = TypeVar("T", contravariant=True)


class MessageFactory(Protocol[T]):
    def __call__(self, value: T, property_name: str, negate: bool) -> str:
        """Returns a message describing the failed validation."""
        ...
