# pyvnt: Python Validation and Transform

A class validation and transformation library highly influenced from `typestack` [class transformer](https://github.com/typestack/class-transformer) and [class validator](https://github.com/typestack/class-validator), that has fluent syntax to ensure secure data structures in Python. The library is based on the `dataclasses` library and utilizes it internally to store metadata on the fields.

- [pyvnt: Python Validation and Transform](#pyvnt-python-validation-and-transform)
  - [Installation](#installation)
  - [Motivation](#motivation)
  - [Validation](#validation)
    - [Predefined Validators](#predefined-validators)
    - [Defining you own Validators](#defining-you-own-validators)
  - [Transformation](#transformation)
    - [Predefined Transformers](#predefined-transformers)
    - [Defining you own Transformers](#defining-you-own-transformers)
  - [API Reference](#api-reference)
    - [Entity](#entity)
      - [Methods](#methods)
    - [Validator](#validator)
      - [Properties](#properties)
      - [Methods](#methods-1)
    - [Transformer](#transformer)
      - [Properties](#properties-1)
      - [Methods](#methods-2)
    - [descriptor | with default value](#descriptor--with-default-value)
    - [descriptor | with default factory](#descriptor--with-default-factory)
    - [descriptor | with no value initializer](#descriptor--with-no-value-initializer)
  - [Usage](#usage)
    - [Example](#example)

## Installation

- **pip**: To install using `pip` execute the following command where username and password are your git credentials.
  ```bash
  pip install pyvnt
  ```
- **poetry**: To install using poetry, you'll need to first add the source to your project by executing the following command. Then install normally as any other package.
  ```bash
  poetry add pyvnt
  ```

## Motivation

The motivation behind creating `pyvnt` is to provide developers with a versatile tool set that enhances code robustness, maintainability, and data integrity. This library aims to simplify the process of handling complex data structures by offering the following key features:

1. **Data Validation**: `pyvnt` enables developers to define validation rules and constraints for classes and their properties. This ensures that data input adheres to specific criteria, reducing the risk of processing incorrect or invalid data.
2. **Serialization and Deserialization**: The library facilitates the conversion of complex data objects into various formats, such as JSON or XML, and vice versa. This simplifies data persistence, transfer, and interchange between different systems and applications.

By combining these functionalities, `pyvnt` empowers developers to build more reliable, scalable, and maintainable applications. It simplifies data processing tasks and allows for better data validation, leading to fewer bugs and more robust software solutions.

## Validation

The `pyvnt` library empowers developers to enforce stringent validation rules on classes and their properties, ensuring the integrity of the data processed within the application. By defining validation constraints, developers can establish specific criteria that data must meet, preventing the ingestion of erroneous or inconsistent information. Whether it's validating user inputs, API data, or configuration settings, `pyvnt` simplifies the process of setting up validation checks. From basic type checks to complex custom validations, the library provides a flexible and intuitive way to verify data accuracy.

By catching validation errors early in the data processing pipeline, `pyvnt` helps maintain clean and consistent data, reducing the risk of downstream issues and enhancing the reliability of the application. Whether you're dealing with user forms, external data sources, or internal data manipulation, the validation feature in `pyvnt` is an essential tool for maintaining data quality and ensuring that your application operates with trustworthy information.

**Note**: Every validator exposes the method `negate()` that negates the defined predicate of the validation. For example, if we want a property to be anything but `1` the validator that should be used is `is_equal(1).negate()`. It is not always useful or meaningful to use the `negate()` method, but the functionality exists and can be used freely.

### Predefined Validators

| Validator            | Arguments                                                                                                                                         | Description                                                                                                            |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| `equals`             | `criteria`: The value you want to check against.                                                                                                  | Checks if the property is equal to the value of the specified criteria or not.                                         |
| `is_defined`         | -                                                                                                                                                 | Checks if the property is defined or not.                                                                              |
| `is_empty`           | -                                                                                                                                                 | Checks if the property has a falsy value or not. Falsy values are those that work like False when used in a condition. |
| `is_optional`        | -                                                                                                                                                 | Checks if the property is `None` and if it is skips the rest of the validations.                                       |
| `nested_validator`   | -                                                                                                                                                 | Validates a nested property which has its own validators.                                                              |
| `has_key`            | `criteria`: The value you want to check against.                                                                                                  | Checks if a mapping has the specified criteria as a key or not. Works only with `Mapping` types.                       |
| `has_value`          | `criteria`: The value you want to check against.                                                                                                  | Checks if a mapping has the specified criteria as a value or not. Works only with `Mapping` types.                     |
| `has_key_value_pair` | `criteria`: The key value pair in the form of a tuple you want to check against.                                                                  | Checks if a mapping has the specified criteria as a key value pair or not. Works only with `Mapping` types.            |
| `mapping_validator`  | `*validators`: A list of validators for every item.<br> `mode`: Specifies whether to apply the validations on the key or the value of the mapping | Applies all the specified validators for all the keys or values of the mapping.                                        |
| `sequence_validator` | `*validators`: A list of validators for every item.                                                                                               | Applies all the specified validators for all the items in the sequence.                                                |
| `at_least`           | `criteria`: The value you want to check against.                                                                                                  | Checks if the property is at least the specified criteria or not. Works only with numeric types.                       |
| `at_most`            | `criteria`: The value you want to check against.                                                                                                  | Checks if the property is at most the specified criteria or not. Works only with numeric types.                        |
| `is_divisible_by`    | `criteria`: The value you want to check against.                                                                                                  | Checks if the property is divisible by the specified criteria or not. Works only with numeric types.                   |
| `is_in_range`        | `min`: The smallest value in the range.<br> `max`: The biggest number in the range.                                                               | Checks if the property is within the specified range or not. Works only with numeric types.                            |
| `is_negative`        | -                                                                                                                                                 | Checks if the property is negative or not. Works only with numeric types.                                              |
| `is_positive`        | -                                                                                                                                                 | Checks if the property is positive or not. Works only with numeric types.                                              |
| `contains`           | `criteria`: The value you want to check against.                                                                                                  | Checks if the property contains the specified criteria. Works only with `Sequence` types.                              |
| `has_length`         | `length`: The length you want to check against.                                                                                                   | Checks if the property has exactly the specified length. Works only with `Sequence` types.                             |
| `max_length`         | `length`: The length you want to check against.                                                                                                   | Checks if the property has at most the specified length. Works only with `Sequence` types.                             |
| `min_length`         | `length`: The length you want to check against.                                                                                                   | Checks if the property has at least the specified length. Works only with `Sequence` types.                            |

### Defining you own Validators

A validator is essentially a function that returns a `Validator` object. So to define your own validator you define a function and its arguments like the following example.

```python
from typing import List, Optional, Tuple, TypeVar

from pyvnt import Validator, ValidationException


T = TypeVar("T")

def custom_validator(*args, **kwargs) -> Validator[T]:
  def predicate(value: T, property_name: str) -> Tuple[bool, List[ValidationException]]:
    ...

  def message_factory(value: T, property_name: str, negate: bool) -> str:
    ...

  return Validator(name="custom_validator", predicate=predicate, message_factory=message_factory)
```

## Transformation

In addition to its robust validation features, `pyvnt` offers powerful data transformation capabilities that streamline the handling of complex data structures. The library enables developers to define seamless transformation processes that convert data between different formats, such as JSON, XML, or custom data representations. This is particularly beneficial when working with APIs, databases, or external services that require specific data formats. With `pyvnt`, developers can effortlessly serialize data objects into desired formats for storage, transmission, or interoperability.

The library's deserialization functionality simplifies the reverse process, efficiently converting data from serialized formats back into native Python objects. By providing this seamless transformation layer, `pyvnt` alleviates the complexities of data conversion and allows developers to focus on building functionality without getting bogged down by intricate data handling tasks. Whether you're working with external data sources, integrating with various systems, or ensuring data persistence, `pyvnt` empowers developers to elegantly manage data transformation, promoting cleaner code and more efficient data exchange within the application.

**Note**: Every transformer exposes the method `chain()` that chains transformers in a type safe way. The chained transformer will take the output of the first transformer as its input and will output whatever you choose.

### Predefined Transformers

| Validator               | Arguments                                                                                                                                               | Description                                                           |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------- |
| `datetime_transformer`  | -                                                                                                                                                       | Transforms a `datetime` object to string and back.                    |
| `enum_transformer`      | `cls`: The enumeration type of the property.                                                                                                            | Transforms an `Enum` object to string and back.                       |
| `nested_transformer`    | `cls`: The type of the nested property.                                                                                                                 | Transforms a nested property with its own transformers.               |
| `optional_transformer`  | `transformer`: Transformation to apply if the value in defined (or not `None`).                                                                         | Optionally transforms an object if it's is not `None`.                |
| `self_transformer`      | -                                                                                                                                                       | Transforms a property to itself and back.                             |
| `uuid_transformer`      | -                                                                                                                                                       | Transforms a `UUID` object to string and back.                        |
| `dict_transformer`      | `key_transformer`: Optional transformer for the keys of the dictionary.<br> `value_transformer`: Optional transformer for the values of the dictionary. | Transforms a dictionary object to another dictionary object and back. |
| `mapping_transformer`   | `key_transformer`: Optional transformer for the keys of the dictionary.<br> `value_transformer`: Optional transformer for the values of the dictionary. | Transforms a mapping object to another dictionary object and back.    |
| `frozenset_transformer` | `transformer`: Transformation to apply to every item of the `frozenset`.                                                                                | Transforms a `frozenset` object to list and back.                     |
| `list_transformer`      | `transformer`: Transformation to apply to every item of the `list`.                                                                                     | Transforms a `list` object to list and back.                          |
| `sequence_transformer`  | `transformer`: Transformation to apply to every item of the `sequence`.                                                                                 | Transforms a `sequence` object to list and back.                      |
| `set_transformer`       | `transformer`: Transformation to apply to every item of the `set`.                                                                                      | Transforms a `set` object to list and back.                           |

### Defining you own Transformers

As was with the validators, a transformer is essentially a function that returns a `Transformer` object. So to define your own transformer you define a function and its arguments like the following example.

```python
from typing import List, Optional, Tuple, TypeVar

from pyvnt import Transformer

TIn = TypeVar("TIn")
TOut = TypeVar("TOut")

def custom_transformer(*args, **kwargs) -> Transformer[TIn, TOut]:
  def serializer(value: TIn, property_name: str) -> TOut:
    ...

  def deserializer(value: TOut, property_name: str) -> TIn:
    ...

  return Transformer(name="custom_transformer", serializer=serializer, deserializer=deserializer)
```

## API Reference

### Entity

The base class that creates a `pyvnt` Entity. This class exposes methods to make every class inheriting from it able to validate, serialize and deserialize itself with ease and predictability. The class is decorate with the `@dataclass_transform(field_specifiers=(descriptor,))` decorator which, as per [PEP-0681](https://peps.python.org/pep-0681/), makes it a `dataclass` generator using the `descriptor` function instead of the default `field`. It expose three basic methods, `validate`, `serialize` and `deserialize`, each of which offer self-explanatory functionality.

```python
@dataclass_transform(field_specifiers=(descriptor,))
class Entity(EntityInstance): ...
```

#### Methods

```python
def __init_subclass__(cls, *, init: bool = True, repr: bool = True, eq: bool = True, order: bool = False, unsafe_hash: bool = False, frozen: bool = False) -> None: ...
```

- **Description**: This method is where the magic happens. It alters every class that inherits from `Entity` and turns it into a `dataclass` (in general, check out how this method works in Python).
- **Properties**
  - `init: bool`: Same as `dataclass`. Specifies if it should create the `__init__` method automatically. Default: `True`
  - `repr: bool`: Same as `dataclass`. Specifies if it should create the `__repr__` method automatically. Default: `True`
  - `eq: bool`: Same as `dataclass`. Specifies if it should create the `__eq__` method automatically. Default: `True`
  - `order: bool`: Same as `dataclass`. Specifies if it should create the `__hash__` method automatically, but it's unsafe. Default: `False`
  - `unsafe_hash: bool`: Same as `dataclass`. Specifies if it should create the ``method automatically. Default:`False`
  - `frozen: bool`: Same as `dataclass`. Specifies whether the class is frozen or not (meaning it would have no property setters if `True`). Default: `False`

```python
def __post_init__(self) -> None: ...
```

- **Description**: Since dataclasses and therefore pyvnt overrides the default constructor of the class, users have no way to allow them to apply complex logic during the instantiation of the class. For this reason, the `__post_init__` method was created which is called internally right before the `__init__` method returns. When inside this function, you can be sure that all the parameters that you specified during the construction are present in their assigned properties and can be accessed freely.

```python
@overload
def validate(self, throw: Literal[True] = True) -> Self: ...
```

- **Description**: This method applies all the specified validations on the instance calling it and returns the same - now validated - instance. If errors occur during the validation it raises them.
- **Parameters**
  - `throw` `(bool)`: Determines wether the method should return the tuple or raise the exception. Default: `True`
- **Returns** `Self`: The validated instance.
- **Raises**
  - `ValidationException`: Describes which validator on which property failed to execute its predicate.

```python
@overload
def validate(self, throw: Literal[False] = False) -> Tuple[bool, Optional[ValidationException]]: ...
```

- **Description**: This method applies all the specified validations on the instance calling it and returns a boolean and an optional exception. If the boolean is set to `True` it means that the validation was successful and that the exception is `None`. Otherwise, the validation failed and the exception contains the reason that the validation failed.
- **Parameters**
  - `throw` `(bool)`: Determines wether the method should return the tuple or raise the exception. Default: `False`
- **Returns** `Tuple[bool, Optional[ValidationException]]`: The boolean that signifies the result of the validation and an optional exception which, if defined, describes why the validation failed.

```python
def serialize(self) -> Dict[str, Any]: ...
```

- **Description**: This method applies all the serialization transformations specified on the instance calling it and returns a fully serializable dictionary, which can then be converted to JSON, yml, toml, etc. If the transformation of any property fails, an exception is raised.
- **Returns** `Dict[str, Any]`: A fully serializable dictionary with string keys and recursively serializable objects.
- **Raises**
  - `TransformationException`: Describes which transformer on which property failed to execute its serializer.

```python
@classmethod
def deserialize(cls, values: Dict[str, Any], validate: bool = True) -> Self: ...
```

- **Description**: This method applies all the deserialization transformations specified on the instance calling it and returns a new instance of itself, after calling its `__post_init__` method (if present). If the transformation of any property fails, or if a required key is missing, an exception is raised.
- **Parameters**
  - `values` `(Dict[str, Any])`: The dictionary containing all the key value pairs necessary to deserialize an instance (presumably created by the `serialize` method). This dictionary, on the top level of every object can have the special key `__type__` were the user can specify the module path of an inherited class which will be used for the deserialization. In other words, if you need to deserialize class `B` which is located in the module `X` and inherits from class `A` , but you only have access to the parent class, you can deserialize an instance of `B` by calling `A.deserialize({'__type__': 'X.B', ...}, ...)`.
  - `validate` `(bool)`: Specifies wether the the instance should validated after its deserialization or not. Default: `True`
- **Returns** `Self`: A fresh, deserialized instance of the class or any of its subclasses.
- **Raises**
  - `Exception`: If a required property of the class is missing from the dictionary. A property's 'requiredness' is determined by two factors, if it is optional or if it has a default value or factory. If neither of those conditions are true, then the property is required.
  - `ValidationException`: If the validate flag is set to `True`. Describes which validator on which property failed to execute its predicate.
  - `TransformationException`: Describes which transformer on which property failed to execute its deserializer.

### Validator

A generic validator class for validating properties.

```python
T = TypeVar("T", contravariant=True)


class Validator(Generic[T]):
    name: str
    predicate: Predicate[T]
    message_factory: MessageFactory[T]
    mode: ValidationMode
    negated: bool
    property_name: Optional[str]
```

#### Properties

- `name: str`: The name of the validator. Useful for tracking where an error occurred.
- `mode: ValidationMode`: The validation mode flag specifies how the validation will happen for the validator. As of now there are two modes: `Default` and `Conditional`. When a validator is in default mode, if it fails the validation process stops and the error is returned. On the other hand if the validation fails and the validator is conditional, then it just skips the reset of the validators and considers itself to pass. Really useful when you want to apply a validation for optionally typed properties.
- `negated: bool`: Boolean flag to specify wether to check the given predicate or its negation.
- `predicate: Predicate[T]`: The predicate that the validator will check against the property.
- `property_name: Optional[str]`: The name of the property that is being validated. It is marked as optional not because it needs not be present, but because the information won't be accessible from the descriptor. It will be populated per property in the `Entity.validate` method.
- `message_factory: MessageFactory[T]`: A callable object that takes the value and the name of the property and the negation flag, and returns the error message that will be thrown if the validation fails.

#### Methods

```python
def __init__(self, name: str, predicate: Predicate[T], message_factory: MessageFactory[T], mode: ValidationMode = ValidationMode.Default property_name: Optional[str] = None) -> None: ...
```

- **Description**: Creates a new `Validator[T]` instance.
- **Parameters**
  - `name: str`: The name of the validator. Useful for tracking where an error occurred.
  - `predicate: Predicate[T]`: The predicate that the validator will check against the property.
  - `message_factory: MessageFactory[T]`: A callable object that takes the value and the name of the property and the negation flag, and returns the error message that will be thrown if the validation fails.
  - `mode: ValidationMode`: The validation mode flag specifies how the validation will happen for the validator. As of now there are two modes: `Default` and `Conditional`. When a validator is in default mode, if it fails the validation process stops and the error is returned. On the other hand if the validation fails and the validator is conditional, then it just skips the reset of the validators and considers itself to pass. Really useful when you want to apply a validation for optionally typed properties.
  - `property_name: Optional[str]`: The name of the property that is being validated. It is marked as optional not because it needs not be present, but because the information won't be accessible from the descriptor. It will be populated per property in the `Entity.validate` method.

```python
def validate(self, value: T) -> Optional[ValidationException]: ...
```

- **Description**: Validate a value using the validator's predicate function.
- **Parameters**
  - `value: T`: The value to be validated.
- **Returns** `Optional[ValidationException]`: A ValidationException if validation fails, or None if successful.
- **Raises**:
  - `Exception`: If the `property_name` does not have a value an exception is thrown stating as much.

```python
def negate(self) -> Self: ...
```

- **Description**: Negate the validator, making it check for the opposite condition.
- **Returns** `Self`: The negated validator.

```python
@classmethod
def compose(cls, *validators: Validator[T], property_name: str) -> Validator[T]: ...
```

- **Description**: This _classmethod_ composes an arbitrary number of validators into a single validator object. It is intended to be used in the `Entity.validate` method to gather all the validators into a single instance to batch perform validations on the properties.
- **Parameters**
  - `*validators: Validator[T]`: Variable-length arguments of validators to compose.
  - `property_name: str`: The name of the property the composed validator will be applied to.
- **Returns** `Validator[T]`: The composed validator.

### Transformer

A generic transformer class for serializing and deserializing data. This class allows you to create transformers that can convert data between different formats using custom serializer and deserializer functions.

```python
TIn = TypeVar("TIn")
TOut = TypeVar("TOut")


class Transformer(Generic[TIn, TOut]):
    name: str
    serializer: Serializer[TIn, TOut]
    deserializer: Deserializer[TIn, TOut]
    property_name: Optional[str]
```

#### Properties

- `name: str`: The name of the transformer. Useful for tracking where an error occurred.
- `serializer: Serializer[TIn, TOut]`: The serializer function that takes an object of type `TIn` and returns an object of type `TOut`.
- `deserializer: Deserializer[TIn, TOut]`: The deserializer function that takes an object of type `TOut` and returns an object of type `TIn`.
- `property_name: Optional[str]`: The name of the property that is being transformed. It is marked as optional not because it needs not be present, but because the information won't be accessible from the descriptor. It will be populated per property in the `Entity.serialize` and `Entity.deserialize` methods.

#### Methods

```python
def __init__(self, name: str, serializer: Serializer[TIn, TOut], deserializer: Deserializer[TIn, TOut], property_name: Optional[str] = None) -> None: ...
```

- **Description**: Creates a new `Transformer[TIn, TOut]` instance.
- **Parameters**
  - `name: str`: The name of the transformer. Useful for tracking where an error occurred.
  - `serializer: Serializer[TIn, TOut]`: The serializer function that takes an object of type `TIn` and returns an object of type `TOut`.
  - `deserializer: Deserializer[TIn, TOut]`: The deserializer function that takes an object of type `TOut` and returns an object of type `TIn`.
  - `property_name: Optional[str]`: The name of the property that is being transformed. It is marked as optional not because it needs not be present, but because the information won't be accessible from the descriptor. It will be populated per property in the `Entity.serialize` and `Entity.deserialize` methods. Defaults to `None`.

```python
def serialize(self, value: TIn) -> TOut: ...
```

- **Description**: Serializes the given value of type `TIn` and returns the serialized value of type `TOut`. In order to produce meaningful error messages, it is necessary for the `property_name` property to have been set at the point this method is called. Otherwise, it will throw an exception stating so.
- **Parameters**
  - `value: TIn`: The value that is going to be serialized.
- **Returns** `TOut`: The serialized value.
- **Raises**
  - `Exception`: If the `property_name` does not have a value an exception is thrown stating as much.
  - `TransformationException`: If the serialization process fails for some reason, this exception is thrown with detail on which property failed, why and optionally the exception that was thrown and caused the failure.

```python
def deserialize(self, value: TOut) -> TIn: ...
```

- **Description**: Deserializes the given value of type `TOut` and returns the deserialized value of type `TIn`. In order to produce meaningful error messages, it is necessary for the `property_name` property to have been set at the point this method is called. Otherwise, it will throw an exception stating so.
- **Parameters**
  - `value: TOut`: The value that is going to be deserialized.
- **Returns** `TIn`: The deserialized value.
- **Raises**
  - `Exception`: If the `property_name` does not have a value an exception is thrown stating as much.
  - `TransformationException`: If the deserialization process fails for some reason, this exception is thrown with detail on which property failed, why and optionally the exception that was thrown and caused the failure.

```python
TChainOut = TypeVar("TChainOut")

def chain(self, transformer: Transformer[TOut, TChainOut]) -> Transformer[TIn, TChainOut]: ...
```

- **Description**: Chains two transformer objects into a single transformer, while respecting their in and out types. In order for this method to work, you need to provide with a transformer instance that has as its input type the output type of the transformer from which the method is called. You could virtually chain an arbitrary number of transformers, essentially creating a transformation pipeline with various steps to reach the desired output (or input).
- **Parameters**
  - `transformer: Transformer[TOut, TChainOut]`: The transformer that is going to be chained. Notice how it expects the same `TOut` generic type of the calling transformer to be its input and an entirely arbitrary `TChainOut` generic type to be its output.
- **Returns** `Transformer[TIn, TChainOut]`: A new transformer instance with input type `TIn` (the same as the calling transformer) and output type `TChainOut` (the same as the provided transformer).

```python
@classmethod
def compose(cls, *transformers: Transformer[Any, Any], property_name: str) -> Transformer[Any, Any]: ...
```

- **Description**: This _classmethod_ composes an arbitrary number of transformers into a single transformer object. It differs from the `chain` method in its ignoring the input and output types of the provided transformers. It is intended to be used in the `Entity.serialize` and `Entity.deserialize` methods to gather all the transformers (included chained ones) into a single instance to batch perform serialization and deserialization on the properties.
- **Parameters**
  - `*transformers: Transformer[Any, Any]`: Variable-length arguments of transformers to compose.
  - `property_name: str`: The name of the property the composed transformer will be applied to.
- **Returns** `Transformer[Any, Any]`: The composed transformer.

### descriptor | with default value

```python
_T = TypeVar("_T")

def descriptor(*, default: _T, init: bool = True, repr: bool = True, hash: Optional[bool] = None, compare: bool = True, validations: List[Validator[_T]] = [], transformations: List[Transformer[_T, Any]] = []) -> _T: ...
```

- **Description**: A wrapper for `dataclass.field` with default value, that adds validators and transformers on the property offering type safety.
- **Parameters**
  - `default: _T`: If provided, this will be the default value for this field. This is needed because the `descriptor()` call itself replaces the normal position of the default value.
  - `init: bool`: If true, this field is included as a parameter to the generated `__init__()` method. Default `True`.
  - `repr: bool`: If true, this field is included in the string returned by the generated `__repr__()` method. Default `True`.
  - `hash: Optional[bool]`: This can be a bool or None. If true, this field is included in the generated `__hash__()` method. If `None`, use the value of compare: this would normally be the expected behavior. A field should be considered in the hash if it’s used for comparisons. Setting this value to anything other than `False` is discouraged. Default `None`.
  - `compare: bool`: If true, this field is included in the generated equality and comparison methods (`__eq__()`, `__gt__()`, et al.). Default `True`.
  - `validation: List[Validator[_T]]`: A list of validators to apply to this property. Internally it will use the metadata parameter of `field` to store the information on the property. Default `[]`.
  - `transformation: List[Transformer[_T, Any]]`: A list of transformers to apply to this property. Internally it will use the metadata parameter of `field` to store the information on the property. Default `[]`.

### descriptor | with default factory

```python
_T = TypeVar("_T")

def descriptor(*, default_factory: Callable[[], _T], init: bool = True, repr: bool = True, hash: Optional[bool] = None, compare: bool = True, validations: List[Validator[_T]] = [], transformations: List[Transformer[_T, Any]] = []) -> _T: ...
```

- **Description**: A wrapper for `dataclass.field` with default factory, that adds validators and transformers on the property offering type safety.
- **Parameters**
  - `default_factory`: If provided, it must be a zero-argument callable that will be called when a default value is needed for this field. Among other purposes, this can be used to specify fields with mutable default values, as discussed below. It is an error to specify both `default` and `default_factory`.
  - `init: bool`: If true, this field is included as a parameter to the generated `__init__()` method. Default `True`.
  - `repr: bool`: If true, this field is included in the string returned by the generated `__repr__()` method. Default `True`.
  - `hash: Optional[bool]`: This can be a bool or None. If true, this field is included in the generated `__hash__()` method. If `None`, use the value of compare: this would normally be the expected behavior. A field should be considered in the hash if it’s used for comparisons. Setting this value to anything other than `False` is discouraged. Default `None`.
  - `compare: bool`: If true, this field is included in the generated equality and comparison methods (`__eq__()`, `__gt__()`, et al.). Default `True`.
  - `validation: List[Validator[_T]]`: A list of validators to apply to this property. Internally it will use the metadata parameter of `field` to store the information on the property. Default `[]`.
  - `transformation: List[Transformer[_T, Any]]`: A list of transformers to apply to this property. Internally it will use the metadata parameter of `field` to store the information on the property. Default `[]`.

### descriptor | with no value initializer

```python
_T = TypeVar("_T")

def descriptor(*, init: bool = True, repr: bool = True, hash: Optional[bool] = None, compare: bool = True, validations: List[Validator[_T]] = [], transformations: List[Transformer[_T, Any]] = []) -> _T: ...
```

- **Description**: A wrapper for `dataclass.field` with no value initializer, that adds validators and transformers on the property offering type safety.
- **Parameters**
  - `init: bool`: If true, this field is included as a parameter to the generated `__init__()` method. Default `True`.
  - `repr: bool`: If true, this field is included in the string returned by the generated `__repr__()` method. Default `True`.
  - `hash: Optional[bool]`: This can be a bool or None. If true, this field is included in the generated `__hash__()` method. If `None`, use the value of compare: this would normally be the expected behavior. A field should be considered in the hash if it’s used for comparisons. Setting this value to anything other than `False` is discouraged. Default `None`.
  - `compare: bool`: If true, this field is included in the generated equality and comparison methods (`__eq__()`, `__gt__()`, et al.). Default `True`.
  - `validation: List[Validator[_T]]`: A list of validators to apply to this property. Internally it will use the metadata parameter of `field` to store the information on the property. Default `[]`.
  - `transformation: List[Transformer[_T, Any]]`: A list of transformers to apply to this property. Internally it will use the metadata parameter of `field` to store the information on the property. Default `[]`.

## Usage

`pyvnt` is extremely easy to use and heavily inspired from Python's `dataclasses.dataclass`. For every data schema you want to turn into a `pyvnt.Entity` you just make it inherit from this class, as simple as that. Then, following the pattern defined by `dataclasses.dataclass`, all the properties your class has need to be instantiated from `pyvnt.descriptor` which is essentially the same as `dataclasses.field` with the extra parameters to specify the _validators_ and the _transformers_ of the property.

### Example

```python
from typing import Any, Dict
from pyvnt import Entity, descriptor, equals, nested_validation, transform_nested


class Nested(Entity):
  property_one: int = descriptor(default=1, validations=[equals(1)])
  property_two: int = descriptor(default=2, validations=[equals(1).negate()])


class Sample(Entity):
  """The Sample class now has access to three methods: `validate`, `serialize` and `deserialize`."""
  property_one: int = descriptor(default=1, validations=[equals(1)])
  property_two: int = descriptor(default=2, validations=[equals(1).negate()])
  property_three: Nested = descriptor(
    default_factory=NestedSample,
    validations=[nested_validation()],
    transformations=[transform_nested(Nested)]
  )


sample = Sample()
success, error = sample.validate()
print(success, error)  # Prints: True, None

serialized: Dict[str, Any] = sample.serialize()
print(serialized)  # Prints: {'__type__': 'main.Sample', 'property_one': 1, 'property_two': 2, 'property_three': {'__type__': 'main.Nested', 'property_one': 1, 'property_two': 2}}

deserialized_sample: Sample = Sample.deserialize(serialized)  # Returns an actual instance of the class Sample
success, error = deserialized_sample.validate()  # Can use all the methods defined in Sample
print(success, error)  # Prints: True, None

assert sample == deserialized_sample
```
