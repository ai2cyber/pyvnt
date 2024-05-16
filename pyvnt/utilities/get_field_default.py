from dataclasses import MISSING
from typing import Optional, TypeVar

from pyvnt.instance import FieldInstance

_T = TypeVar("_T", contravariant=True)


def get_field_default(field: FieldInstance[_T]) -> Optional[_T]:
    return (
        field.default
        if field.default is not MISSING
        else field.default_factory()
        if field.default_factory is not MISSING
        else None
    )
