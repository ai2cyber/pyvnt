from typing import Any, List, Literal, Mapping, Optional, Tuple, overload

from pyvnt.exceptions import ValidationException
from pyvnt.utilities import MessageFactory
from pyvnt.validator import T, Validator


@overload
def mapping_validator(
    *validators: Validator[T],
    mode: Literal["key"],
    message: Optional[MessageFactory[Mapping[T, Any]]] = None,
) -> Validator[Mapping[T, Any]]:
    """Applies all the specified validators for all the keys or values of the mapping.

    Args:
        *validators (Validator[T]): A list of validators for every item.
        mode (Literal['key']): Specifies whether to apply the validations on the key or the value of the mapping
    """
    ...


@overload
def mapping_validator(
    *validators: Validator[T],
    mode: Literal["value"],
    message: Optional[MessageFactory[Mapping[Any, T]]] = None,
) -> Validator[Mapping[Any, T]]:
    """Applies all the specified validators for all the keys or values of the mapping.

    Args:
        *validators (Validator[T]): A list of validators for every item.
        mode (Literal['value']): Specifies whether to apply the validations on the key or the value of the mapping
    """
    ...


def mapping_validator(
    *validators: Validator[Any],
    mode: Literal["key", "value"],
    message: Optional[MessageFactory[Mapping[Any, Any]]] = None,
) -> Validator[Mapping[Any, Any]]:
    """Applies all the specified validators for all the keys or values of the mapping.

    Args:
        *validators (Validator[Any]): A list of validators for every item.
        mode (Literal['key', 'value']): Specifies whether to apply the validations on the key or the value of the mapping
    """  # noqa

    def predicate(value: Mapping[Any, Any], property_name: str) -> Tuple[bool, List[ValidationException]]:
        errors: List[ValidationException] = []
        for key, value in value.items():
            for validator in validators:
                validator.property_name = f"{property_name}.{key}"
                if error := validator.validate(key if mode == "key" else value):
                    errors.append(error)
        return not errors, errors

    def message_factory(value: Mapping[Any, Any], property_name: str, negate: bool) -> str:
        return f'Expected every {mode} of "{property_name}" to satisfy the conditions.'

    return Validator(name="mapping_validator", predicate=predicate, message_factory=message or message_factory)
