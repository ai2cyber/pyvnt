from typing import Protocol, TypeVar

_TIn = TypeVar("_TIn", contravariant=True)
_TOut = TypeVar("_TOut", covariant=True)


class Serializer(Protocol[_TIn, _TOut]):
    def __call__(self, value: _TIn, property_name: str) -> _TOut:
        ...
