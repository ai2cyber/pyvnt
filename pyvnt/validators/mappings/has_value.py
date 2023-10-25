from typing import Any, List, Mapping, Optional, Tuple

from pyvnt.exceptions import ValidationException
from pyvnt.utilities import MessageFactory
from pyvnt.validator import T, Validator


def has_value(criteria: T, message: Optional[MessageFactory[Mapping[Any, T]]] = None) -> Validator[Mapping[Any, T]]:
    """Checks if a mapping has the specified criteria as a value or not. Works only with `Mapping` types.

    Args:
        criteria (T): The value you want to check against."""

    def predicate(value: Mapping[Any, T], property_name: str) -> Tuple[bool, List[ValidationException]]:
        return criteria in value.values(), []

    def message_factory(value: Mapping[Any, T], property_name: str, negate: bool) -> str:
        return f"Expected property \"{property_name}\" to{' not ' if negate else ' '}contain the value \"{criteria}\"."

    return Validator(name="has_value", predicate=predicate, message_factory=message or message_factory)
