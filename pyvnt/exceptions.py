from typing import Dict, List


class ValidationException(Exception):
    def __init__(
        self,
        message: str,
        property_errors: "Dict[str, List[ValidationException]]" = {},
    ) -> None:
        super().__init__(message, property_errors)

        self.message: str = message
        self.property_errors: Dict[str, List[ValidationException]] = property_errors


class TransformationException(Exception):
    def __init__(self, name: str, message: str, exception: Exception) -> None:
        super().__init__(name, message, exception)

        self.name: str = name
        self.message: str = message
        self.exception: Exception = exception
