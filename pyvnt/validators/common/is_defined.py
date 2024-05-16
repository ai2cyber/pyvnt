from typing import Any, List, Optional, Tuple

from pyvnt.exceptions import ValidationException
from pyvnt.utilities import MessageFactory
from pyvnt.validator import Validator


def is_defined(message: Optional[MessageFactory[Any]] = None) -> Validator[Any]:
    """Checks if the property is defined or not."""

    def predicate(value: Any, property_name: str) -> Tuple[bool, List[ValidationException]]:
        return value is not None, []

    def message_factory(value: Any, property_name: str, negate: bool):
        return f"Expected property \"{property_name}\" to{' not ' if negate else ' '}be defined."

    return Validator(name="is_defined", predicate=predicate, message_factory=message or message_factory)
