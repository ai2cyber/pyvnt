from enum import Enum
from typing import Generic, List, Optional, Tuple, TypeVar

from typing_extensions import Self

from pyvnt.exceptions import ValidationException
from pyvnt.utilities import MessageFactory, Predicate

T = TypeVar("T", contravariant=True)


def negate_predicate(predicate: Predicate[T]) -> Predicate[T]:
    def negated(value: T, property_name: str) -> Tuple[bool, List[ValidationException]]:
        result, error = predicate(value, property_name)
        return not result, error

    return negated


class ValidationMode(Enum):
    """Specifies how the validation will happen for a property."""

    Default = "default"
    """The validation will happen normally one after the other."""

    Conditional = "conditional"
    """If a conditional validation fails, the rest of the validations won't happen."""


class Validator(Generic[T]):
    def __init__(
        self,
        name: str,
        predicate: Predicate[T],
        message_factory: MessageFactory[T],
        mode: ValidationMode = ValidationMode.Default,
        property_name: Optional[str] = None,
    ) -> None:
        self.name: str = name
        self.predicate: Predicate[T] = predicate
        self.message_factory: MessageFactory[T] = message_factory

        self.mode: ValidationMode = mode
        self.negated: bool = False
        self.property_name: Optional[str] = property_name

    def validate(self, value: T) -> Optional[ValidationException]:
        if not self.property_name:
            raise Exception(f'Validator "{self.name}" called without a property name.')

        result, errors = self.predicate(value, self.property_name)
        if not result:
            message = self.message_factory(value, self.property_name, self.negated)
            property_errors = {self.property_name: errors}
            return ValidationException(message, property_errors)

        return None

    def negate(self) -> Self:
        self.negated = True
        self.predicate = negate_predicate(self.predicate)
        return self

    @classmethod
    def compose(cls, *validators: "Validator[T]", property_name: str) -> "Validator[T]":
        def predicate(value: T, property_name: str) -> Tuple[bool, List[ValidationException]]:
            errors: List[ValidationException] = []

            for validator in validators:
                validator.property_name = property_name

                error = validator.validate(value)
                continue_validation = error is None if validator.mode == ValidationMode.Default else error is not None

                if error and not validator.mode == ValidationMode.Conditional:
                    errors.append(error)

                if not continue_validation:
                    break

            return not errors, errors

        def message_factory(value: T, property_name: str, negate: bool) -> str:
            return f'Validation failed for property "{property_name}": {value}.'

        return Validator(
            name="composed",
            predicate=predicate,
            message_factory=message_factory,
            property_name=property_name,
        )
