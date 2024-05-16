from typing import List, Optional, Tuple

from pyvnt.exceptions import ValidationException
from pyvnt.instance import EntityInstance
from pyvnt.utilities import MessageFactory
from pyvnt.validator import Validator


def nested_validator(message: Optional[MessageFactory[EntityInstance]] = None) -> Validator[EntityInstance]:
    """Validates a nested property which has its own validators."""

    def predicate(value: EntityInstance, property_name: str) -> Tuple[bool, List[ValidationException]]:
        result, error = value.validate(False)

        errors: List[ValidationException] = []
        if error:
            errors.append(error)

        return result, errors

    def message_factory(value: EntityInstance, property_name: str, negate: bool):
        return f'Validation failed for property "{property_name}".'

    return Validator(name="validate_nested", predicate=predicate, message_factory=message or message_factory)
