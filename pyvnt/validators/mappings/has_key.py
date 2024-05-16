from typing import Any, List, Mapping, Optional, Tuple

from pyvnt.exceptions import ValidationException
from pyvnt.utilities import MessageFactory
from pyvnt.validator import T, Validator


def has_key(criteria: T, message: Optional[MessageFactory[Mapping[T, Any]]] = None) -> Validator[Mapping[T, Any]]:
    """Checks if a mapping has the specified criteria as a key or not. Works only with `Mapping` types.

    Args:
        criteria (T): The value you want to check against."""

    def predicate(value: Mapping[T, Any], property_name: str) -> Tuple[bool, List[ValidationException]]:
        return criteria in value, []

    def message_factory(value: Mapping[T, Any], property_name: str, negate: bool) -> str:
        return f"Expected property \"{property_name}\" to{' not ' if negate else ' '}contain the key \"{criteria}\"."

    return Validator(name="has_key", predicate=predicate, message_factory=message or message_factory)

#comments