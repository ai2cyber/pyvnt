from typing import List, Protocol, Tuple, TypeVar

from pyvnt.exceptions import ValidationException

T = TypeVar("T", contravariant=True)


class Predicate(Protocol[T]):
    def __call__(self, value: T, property_name: str) -> Tuple[bool, List[ValidationException]]:
        """A predicate that checks whether a value passes or not a validation."""
        ...
