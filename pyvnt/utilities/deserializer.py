from typing import Protocol, TypeVar

_TIn = TypeVar("_TIn", covariant=True)
_TOut = TypeVar("_TOut", contravariant=True)


class Deserializer(Protocol[_TIn, _TOut]):
    def __call__(self, value: _TOut, property_name: str) -> _TIn:
        ...
