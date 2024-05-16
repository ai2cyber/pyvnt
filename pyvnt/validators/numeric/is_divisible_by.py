from typing import List, Optional, Tuple, TypeVar

from pyvnt.exceptions import ValidationException
from pyvnt.utilities import MessageFactory
from pyvnt.validator import Validator

T = TypeVar("T", int, float)


def is_divisible_by(criteria: T, message: Optional[MessageFactory[T]] = None) -> Validator[T]:
    """Checks if the property is divisible by the specified criteria or not. Works only with numeric types.

    Args:
        criteria (T): The value you want to check against."""

    def predicate(value: T, property_name: str) -> Tuple[bool, List[ValidationException]]:
        return value % criteria == 0, []

    def message_factory(value: T, property_name: str, negate: bool) -> str:
        return f"Expected property \"{property_name}\" to{' not ' if negate else ' '}be divisible by {criteria}"

    return Validator(name="is_divisible_by", predicate=predicate, message_factory=message or message_factory)
