from typing import List, Optional, Tuple, TypeVar

from pyvnt.exceptions import ValidationException
from pyvnt.utilities import MessageFactory
from pyvnt.validator import Validator

T = TypeVar("T", int, float)


def is_in_range(min: T, max: T, message: Optional[MessageFactory[T]] = None) -> Validator[T]:
    """Checks if the property is within the specified range or not. Works only with numeric types.

    Args:
        min (int): The smallest value in the range.
        max (int): The biggest number in the range."""

    def predicate(value: T, property_name: str) -> Tuple[bool, List[ValidationException]]:
        return min <= value <= max, []

    def message_factory(value: T, property_name: str, negate: bool) -> str:
        return f"Expected property \"{property_name}\" to{' not ' if negate else ' '}be in the range [{min}, {max}]."

    return Validator(name="is_in_range", predicate=predicate, message_factory=message or message_factory)
