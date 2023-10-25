from dataclasses import dataclass
from typing import Any, ClassVar, Dict, List, Literal, Optional, Tuple, Type, Union, overload

from typing_extensions import Self, dataclass_transform

from pyvnt.constants import TRANSFORMER_METADATA, VALIDATOR_METADATA
from pyvnt.descriptor import descriptor
from pyvnt.exceptions import ValidationException
from pyvnt.instance import EntityInstance, FieldInstance
from pyvnt.transformer import Transformer
from pyvnt.utilities import check_non_existence, descriptors, get_field_default, to_type
from pyvnt.validator import Validator


@dataclass_transform(field_specifiers=(descriptor,))
class Entity(EntityInstance):
    __entity__: ClassVar[bool] = True
    __dataclass_fields__: ClassVar[Dict[str, FieldInstance[Any]]]
    __dataclass_params__: ClassVar[Any]

    def __init_subclass__(
        cls,
        *,
        init: bool = True,
        repr: bool = True,
        eq: bool = True,
        order: bool = False,
        unsafe_hash: bool = False,
        frozen: bool = False,
    ) -> None:
        dataclass(init=init, repr=repr, eq=eq, order=order, unsafe_hash=unsafe_hash, frozen=frozen)(cls)

    def __post_init__(self) -> None:
        pass

    @overload
    def validate(self, throw: Literal[True] = True) -> Self:
        ...

    @overload
    def validate(self, throw: Literal[False] = False) -> Tuple[bool, Optional[ValidationException]]:
        ...

    def validate(self, throw: bool = True) -> Union[Self, Tuple[bool, Optional[ValidationException]]]:
        property_errors: Dict[str, List[ValidationException]] = {}

        for field in descriptors(self):
            validators: List[Validator[Any]] = field.metadata.get(VALIDATOR_METADATA, [])
            if not validators:
                continue

            value = getattr(self, field.name)

            composed_validator = Validator.compose(*validators, property_name=field.name)
            error = composed_validator.validate(value)

            if error:
                property_errors[field.name] = error.property_errors.get(field.name) or []

        exception = ValidationException(self.__class__.__name__, property_errors) if property_errors else None

        if not throw:
            return not exception, exception

        if exception:
            raise exception

        return self

    def serialize(self) -> Dict[str, Any]:
        dictionary: Dict[str, Any] = {"__type__": ".".join([self.__class__.__module__, self.__class__.__name__])}

        for field in descriptors(self):
            transformers: List[Transformer[Any, Any]] = field.metadata.get(TRANSFORMER_METADATA, [])
            if not transformers:
                raise Exception(f"No transformers found for {self.__class__.__name__}s property {field.name}")

            composed_transformer = Transformer.compose(*transformers, property_name=field.name)
            dictionary[field.name] = composed_transformer.serialize(getattr(self, field.name))

        return {k: v for k, v in dictionary.items() if v is not None}

    @classmethod
    def deserialize(cls, values: Dict[str, Any], validate: bool = True) -> Self:
        target_class: Type[Self] = cls
        if "__type__" in values:
            target_class = to_type(values["__type__"], cls)

        target_instance = object.__new__(target_class)

        for field in descriptors(target_class):
            check_non_existence(field, values, target_class.__name__)

            transformers: List[Transformer[Any, Any]] = field.metadata.get(TRANSFORMER_METADATA, [])
            transformers.reverse()
            if not transformers:
                raise Exception(f"No transformers found for {target_class.__name__}s property {field.name}")

            value = values.get(field.name)
            if value is not None:
                composed_transformer = Transformer.compose(*transformers, property_name=field.name)
                setattr(target_instance, field.name, composed_transformer.deserialize(value))
            else:
                setattr(target_instance, field.name, get_field_default(field))

        # Handle post initialization
        target_instance.__post_init__()  # type: ignore

        if validate:
            return target_instance.validate()

        return target_instance
