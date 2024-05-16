from dataclasses import is_dataclass
from typing import Any, Type, Union

from pyvnt.constants import ENTITY


def is_entity(cls_or_instance: Union[Any, Type[Any]]) -> bool:
    return is_dataclass(cls_or_instance) and hasattr(cls_or_instance, ENTITY)
