from typing import List, Optional, Tuple

from pyvnt.exceptions import ValidationException
from pyvnt.utilities import MessageFactory
from pyvnt.validator import T, Validator


def equals(criteria: T, message: Optional[MessageFactory[T]] = None) -> Validator[T]:
    """Checks if the property is equal to the value of the specified criteria or not.

    Args:
        `criteria`: The value you want to check against."""

    def predicate(value: T, property_name: str) -> Tuple[bool, List[ValidationException]]:
        return value == criteria, []

    def message_factory(value: T, property_name: str, negate: bool) -> str:
        return (
            f"Expected property \"{property_name}\" to{' not ' if negate else ' '}be equal to \"{criteria}\", but"
            f' it\'s "{value}".'
        )

    return Validator(name="equals", predicate=predicate, message_factory=message or message_factory)
