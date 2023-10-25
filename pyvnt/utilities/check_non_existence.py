from dataclasses import MISSING
from typing import Any, Dict, Union, get_args, get_origin

from pyvnt.instance import FieldInstance


def check_non_existence(field: FieldInstance[Any], values: Dict[str, Any], class_name: str) -> None:
    def is_optional(field: FieldInstance[Any]):
        return get_origin(field.type) is Union and type(None) in get_args(field.type)

    def has_default(field: FieldInstance[Any]):
        return field.default is not MISSING or field.default_factory is not MISSING

    if field.name not in values and not is_optional(field) and not has_default(field):
        reason = (
            f'The property "{field.name}" of {class_name} is not optional'
            " is not specified in the dictionary and does not have a default."
        )
        raise ValueError(reason)
