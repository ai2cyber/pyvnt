from typing import List, Mapping, Optional, Tuple, TypeVar

from pyvnt.exceptions import ValidationException
from pyvnt.utilities import MessageFactory
from pyvnt.validator import Validator

_TKey = TypeVar("_TKey")
_TValue = TypeVar("_TValue")


def has_key_value_pair(
    criteria: Tuple[_TKey, _TValue],
    message: Optional[MessageFactory[Mapping[_TKey, _TValue]]] = None,
) -> Validator[Mapping[_TKey, _TValue]]:
    """Checks if a mapping has the specified criteria as a (key, value) pair or not. Works only with `Mapping` types.

    Args:
        criteria (T): The kay, value pair you want to check against."""

    def predicate(value: Mapping[_TKey, _TValue], property_name: str) -> Tuple[bool, List[ValidationException]]:
        if val := value.get(criteria[0]):
            return val == criteria[1], []

        return False, []

    def message_factory(value: Mapping[_TKey, _TValue], property_name: str, negate: bool) -> str:
        message = f'Expected property "{property_name}" to'
        message += " not " if negate else " "
        message += f'contain the (key, value): "{criteria}".'
        return message

    return Validator(name="has_key_value_pair", predicate=predicate, message_factory=message or message_factory)
