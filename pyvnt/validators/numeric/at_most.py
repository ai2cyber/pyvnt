from typing import List, Optional, Tuple, TypeVar

from pyvnt.exceptions import ValidationException
from pyvnt.utilities import MessageFactory
from pyvnt.validator import Validator

T = TypeVar("T", int, float)


def at_most(criteria: T, message: Optional[MessageFactory[T]] = None) -> Validator[T]:
    """Checks if the property is at most the specified criteria or not. Works only with numeric types.

    Args:
        criteria (T): The value you want to check against."""

    def predicate(value: T, property_name: str) -> Tuple[bool, List[ValidationException]]:
        return value <= criteria, []

    def message_factory(value: T, property_name: str, negate: bool) -> str:
        return f"Expected property \"{property_name}\" to{' not ' if negate else ' '}be at most \"{criteria}\"."

    return Validator(name="at_most", predicate=predicate, message_factory=message or message_factory)
