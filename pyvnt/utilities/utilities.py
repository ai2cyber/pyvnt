from dataclasses import MISSING, is_dataclass
from typing import Any, Dict, Union, get_args, get_origin, Tuple, Type, Protocol, TypeVar, Optional, List
import importlib

from pyvnt.instance import EntityInstance, FieldInstance
from pyvnt.constants import ENTITY
from pyvnt.exceptions import ValidationException

T = TypeVar("T", contravariant=True)
_T = TypeVar("_T", contravariant=True)
_TIn = TypeVar("_TIn", covariant=True)
_TOut = TypeVar("_TOut", contravariant=True)


class MessageFactory(Protocol[T]):
    def __call__(self, value: T, property_name: str, negate: bool) -> str:
        """Returns a message describing the failed validation."""
        ...


class Predicate(Protocol[T]):
    def __call__(self, value: T, property_name: str) -> Tuple[bool, List[ValidationException]]:
        """A predicate that checks whether a value passes or not a validation."""
        ...


class Serializer(Protocol[_TIn, _TOut]):
    def __call__(self, value: _TIn, property_name: str) -> _TOut: ...


class Deserializer(Protocol[_TIn, _TOut]):
    def __call__(self, value: _TOut, property_name: str) -> _TIn: ...


def check_non_existence(field: FieldInstance[Any], values: Dict[str, Any], class_name: str) -> None:
    def is_optional(field: FieldInstance[Any]):
        return get_origin(field.type) is Union and type(None) in get_args(field.type)

    def has_default(field: FieldInstance[Any]):
        return field.default is not MISSING or field.default_factory is not MISSING

    if field.name not in values and not is_optional(field) and not has_default(field):
        reason = f'The property "{field.name}" of {class_name} is not optional' " is not specified in the dictionary and does not have a default."
        raise ValueError(reason)


def descriptors(class_or_instance: Union[EntityInstance, Type[EntityInstance]]) -> Tuple[FieldInstance[Any], ...]:
    try:
        fields: Dict[str, FieldInstance[Any]] = getattr(class_or_instance, "__dataclass_fields__")
    except AttributeError:
        raise TypeError("must be called with a dataclass type or instance")

    # Exclude pseudo-fields.  Note that fields is sorted by insertion
    # order, so the order of the tuple is as the fields were defined.
    return tuple(f for f in fields.values())


def get_field_default(field: FieldInstance[_T]) -> Optional[_T]:
    return field.default if field.default is not MISSING else field.default_factory() if field.default_factory is not MISSING else None


def is_entity(cls_or_instance: Union[Any, Type[Any]]) -> bool:
    return is_dataclass(cls_or_instance) and hasattr(cls_or_instance, ENTITY)


def to_type(module_path: str, type: Type[_T]) -> Type[_T]:
    splitted = module_path.split(".")
    class_name = splitted.pop()
    module_name = ".".join(splitted)

    try:
        module = importlib.import_module(module_name)
        cls: Type[Any] = getattr(module, class_name)

        if not issubclass(cls, type):
            raise Exception(f"Loaded type '{cls.__name__}' is not a subclass of '{type.__name__}'.")

        return cls
    except Exception:
        raise
