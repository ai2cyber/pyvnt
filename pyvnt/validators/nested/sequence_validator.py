from typing import List, Optional, Sequence, Tuple

from pyvnt.exceptions import ValidationException
from pyvnt.utilities import MessageFactory
from pyvnt.validator import T, Validator


def sequence_validator(
    *validators: Validator[T],
    message: Optional[MessageFactory[Sequence[T]]] = None,
) -> Validator[Sequence[T]]:
    """Applies all the specified validators for all the items in the sequence.

    Args:
        *validators (Validator[T]): A list of validators for every item."""

    def predicate(value: Sequence[T], property_name: str) -> Tuple[bool, List[ValidationException]]:
        errors: List[ValidationException] = []

        for index, item in enumerate(value):
            for validator in validators:
                validator.property_name = f"{property_name}.{index}"
                if error := validator.validate(item):
                    errors.append(error)
        return not errors, errors

    def message_factory(value: Sequence[T], property_name: str, negate: bool) -> str:
        return f'Expected every item of "{property_name}" to satisfy the conditions.'

    return Validator(name="sequence_validator", predicate=predicate, message_factory=message or message_factory)
