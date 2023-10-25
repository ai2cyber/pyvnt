import unittest
from typing import Any, Dict, List, Optional

from pyvnt import Entity, descriptor
from pyvnt.transformers import dict_transformer, list_transformer, nested_transformer
from pyvnt.validators.common import equals, is_defined, is_empty, is_optional, nested_validator
from pyvnt.validators.nested import mapping_validator, sequence_validator


class NestedSample(Entity):
    property_one: int = descriptor(default=1, validations=[equals(1)])


class Sample(Entity):
    property_one: int = descriptor(default=1, validations=[equals(1)])
    property_two: int = descriptor(default=2, validations=[equals(1).negate()])
    property_three: Optional[int] = descriptor(default=1, validations=[is_defined()])
    property_four: Optional[int] = descriptor(default_factory=lambda: None, validations=[is_defined().negate()])
    property_five: Any = descriptor(default=0, validations=[is_empty()])
    property_six: Any = descriptor(default=1, validations=[is_empty().negate()])
    property_seven: Optional[int] = descriptor(default_factory=lambda: None, validations=[is_optional(), equals(1)])
    property_eight: NestedSample = descriptor(
        default_factory=NestedSample,
        validations=[nested_validator()],
        transformations=[nested_transformer(NestedSample)],
    )
    property_nine: List[NestedSample] = descriptor(
        default_factory=lambda: [NestedSample(), NestedSample()],
        validations=[sequence_validator(nested_validator())],
        transformations=[list_transformer(nested_transformer(NestedSample))],
    )
    property_ten: Dict[str, NestedSample] = descriptor(
        default_factory=lambda: {"test": NestedSample()},
        validations=[mapping_validator(nested_validator(), mode="value")],
        transformations=[dict_transformer(value_transformer=nested_transformer(NestedSample))],
    )


class TestSerialization(unittest.TestCase):
    def test(self):
        sample = Sample()
        serialized_sample = sample.serialize()
        deserialized_sample = Sample.deserialize(serialized_sample)

        self.assertEqual(sample, deserialized_sample)


if __name__ == "__main__":
    unittest.main()
