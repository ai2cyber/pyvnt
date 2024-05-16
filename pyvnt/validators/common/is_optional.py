from typing import Any, List, Optional, Tuple

from pyvnt.exceptions import ValidationException
from pyvnt.utilities import MessageFactory
from pyvnt.validator import ValidationMode, Validator


def is_optional(message: Optional[MessageFactory[Any]] = None) -> Validator[Any]:
    """Checks if the property is `None` and if it is skips the rest of the validations."""

    def predicate(value: Any, property_name: str) -> Tuple[bool, List[ValidationException]]:
        return value is None, []

    def message_factory(value: Any, property_name: str, negate: bool) -> str:
        return ""

    return Validator(
        name="is_optional",
        predicate=predicate,
        message_factory=message or message_factory,
        mode=ValidationMode.Conditional,
    )
