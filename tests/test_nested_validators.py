import unittest
from typing import Dict, List

from pyvnt import Entity, descriptor
from pyvnt.validators.nested import mapping_validator, sequence_validator
from pyvnt.validators.numeric import at_least, at_most


class Sample(Entity):
    property_one: Dict[int, str] = descriptor(
        default_factory=lambda: {1: "2"},
        validations=[mapping_validator(at_least(1), at_most(5), mode="key")],
    )
    property_two: List[int] = descriptor(
        default_factory=lambda: [1, 2],
        validations=[sequence_validator(at_least(1), at_most(5))],
    )


class TestNestedValidators(unittest.TestCase):
    def test_mapping_validator(self):
        sample = Sample(property_one={1: "2"})
        result, error = sample.validate(False)

        self.assertTrue(result)
        self.assertIsNone(error)

        sample = Sample(property_one={6: "3"})
        result, error = sample.validate(False)

        self.assertFalse(result)
        assert error, "Expected error to be defined"
        self.assertIsNotNone(error.property_errors.get("property_one"))

    def test_sequence_validator(self):
        sample = Sample(property_two=[1, 2, 3])
        result, error = sample.validate(False)

        self.assertTrue(result)
        self.assertIsNone(error)

        sample = Sample(property_two=[5, 6, 7])
        result, error = sample.validate(False)

        self.assertFalse(result)
        assert error, "Expected error to be defined"
        self.assertIsNotNone(error.property_errors.get("property_two"))


if __name__ == "__main__":
    unittest.main()
