from typing import List, Optional, Sequence, Tuple

from pyvnt.exceptions import ValidationException
from pyvnt.utilities import MessageFactory
from pyvnt.validator import T, Validator


def contains(criteria: T, message: Optional[MessageFactory[Sequence[T]]] = None) -> Validator[Sequence[T]]:
    """Checks if the property contains the specified criteria. Works only with `Sequence` types.

    Args:
        criteria (T): The value you want to check against."""

    def predicate(value: Sequence[T], property_name: str) -> Tuple[bool, List[ValidationException]]:
        return criteria in value, []

    def message_factory(value: Sequence[T], property_name: str, negate: bool) -> str:
        return f"Expected property \"{property_name}\" to{' not ' if negate else ' '}contain \"{criteria}\"."

    return Validator(name="contains", predicate=predicate, message_factory=message or message_factory)
