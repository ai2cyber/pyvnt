from typing import List, Optional, Tuple, Union

from pyvnt.exceptions import ValidationException
from pyvnt.utilities import MessageFactory
from pyvnt.validator import Validator


def is_positive(message: Optional[MessageFactory[Union[int, float]]] = None) -> Validator[Union[int, float]]:
    """Checks if the property is positive or not. Works only with numeric types."""

    def predicate(value: Union[int, float], property_name: str) -> Tuple[bool, List[ValidationException]]:
        return value > 0, []

    def message_factory(value: Union[int, float], property_name: str, negate: bool) -> str:
        return f"Expected property \"{property_name}\" to{' not ' if negate else ' '}be positive."

    return Validator(name="is_positive", predicate=predicate, message_factory=message or message_factory)
