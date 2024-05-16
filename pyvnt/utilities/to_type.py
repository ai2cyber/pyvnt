import importlib
from typing import Any, Type, TypeVar

_T = TypeVar("_T")


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
