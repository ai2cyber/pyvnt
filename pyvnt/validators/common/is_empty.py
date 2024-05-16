from typing import Any, List, Optional, Tuple

from pyvnt.exceptions import ValidationException
from pyvnt.utilities import MessageFactory
from pyvnt.validator import Validator


def is_empty(message: Optional[MessageFactory[Any]] = None) -> Validator[Any]:
    """Checks if the property has a falsy value or not. Falsy values are those that work like False when used in a
    condition."""

    def predicate(value: Any, property_name: str) -> Tuple[bool, List[ValidationException]]:
        return value is not None and not value, []

    def message_factory(value: Any, property_name: str, negate: bool) -> str:
        return f"Expected property \"{property_name}\" to{' not ' if negate else ' '}be empty."

    return Validator(name="is_empty", predicate=predicate, message_factory=message or message_factory)
