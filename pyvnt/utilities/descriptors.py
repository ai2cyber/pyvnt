from typing import Any, Dict, Tuple, Type, Union

from pyvnt.instance import EntityInstance, FieldInstance


def descriptors(class_or_instance: Union[EntityInstance, Type[EntityInstance]]) -> Tuple[FieldInstance[Any], ...]:
    try:
        fields: Dict[str, FieldInstance[Any]] = getattr(class_or_instance, "__dataclass_fields__")
    except AttributeError:
        raise TypeError("must be called with a dataclass type or instance")

    # Exclude pseudo-fields.  Note that fields is sorted by insertion
    # order, so the order of the tuple is as the fields were defined.
    return tuple(f for f in fields.values())
