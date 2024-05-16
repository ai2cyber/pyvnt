import unittest
from typing import List

from pyvnt import Entity, descriptor
from pyvnt.validators.sequence import contains, has_length, max_length, min_length


class Sample(Entity):
    property_one: List[int] = descriptor(default_factory=lambda: [0, 1, 2, 3], validations=[contains(0)])
    property_two: List[int] = descriptor(default_factory=lambda: [1, 2, 3, 4], validations=[contains(0).negate()])
    property_three: List[int] = descriptor(default_factory=lambda: [0, 1, 2, 3], validations=[has_length(4)])
    property_four: List[int] = descriptor(default_factory=lambda: [0, 1, 2, 3, 4], validations=[has_length(4).negate()])
    property_five: List[int] = descriptor(default_factory=lambda: [0, 1, 2, 3], validations=[max_length(4)])
    property_six: List[int] = descriptor(default_factory=lambda: [0, 1, 2, 3, 5], validations=[max_length(4).negate()])
    property_seven: List[int] = descriptor(default_factory=lambda: [0, 1, 2, 3], validations=[min_length(1)])
    property_eight: List[int] = descriptor(default_factory=lambda: [0, 1, 2, 3], validations=[min_length(5).negate()])


class TestSequenceValidators(unittest.TestCase):
    def test_contains(self):
        sample = Sample(property_one=[0, 1, 2, 3], property_two=[1, 2, 3, 4])
        result, error = sample.validate(False)

        self.assertTrue(result)
        self.assertIsNone(error)

        sample = Sample(property_one=[1, 2, 3, 4])
        result, error = sample.validate(False)

        self.assertFalse(result)
        assert error, "Expected error to be defined"
        self.assertIsNotNone(error.property_errors.get("property_one"))

        sample = Sample(property_two=[0, 1, 2, 3, 4])
        result, error = sample.validate(False)

        self.assertFalse(result)
        assert error, "Expected error to be defined"
        self.assertIsNotNone(error.property_errors.get("property_two"))

    def test_has_length(self):
        sample = Sample(property_three=[1, 2, 3, 4], property_four=[1, 2, 3, 4, 5])
        result, error = sample.validate(False)

        self.assertTrue(result)
        self.assertIsNone(error)

        sample = Sample(property_three=[1, 2, 3])
        result, error = sample.validate(False)

        self.assertFalse(result)
        assert error, "Expected error to be defined"
        self.assertIsNotNone(error.property_errors.get("property_three"))

        sample = Sample(property_four=[1, 2, 3, 4])
        result, error = sample.validate(False)

        self.assertFalse(result)
        assert error, "Expected error to be defined"
        self.assertIsNotNone(error.property_errors.get("property_four"))

    def test_max_length(self):
        sample = Sample(property_five=[1, 2, 3, 4], property_six=[1, 2, 3, 4, 5])
        result, error = sample.validate(False)

        self.assertTrue(result)
        self.assertIsNone(error)

        sample = Sample(property_five=[1, 2, 3, 4, 5])
        result, error = sample.validate(False)

        self.assertFalse(result)
        assert error, "Expected error to be defined"
        self.assertIsNotNone(error.property_errors.get("property_five"))

        sample = Sample(property_six=[1, 2, 3, 4])
        result, error = sample.validate(False)

        self.assertFalse(result)
        assert error, "Expected error to be defined"
        self.assertIsNotNone(error.property_errors.get("property_six"))

    def test_min_length(self):
        sample = Sample(property_seven=[1, 2, 3, 4], property_eight=[1, 2, 3, 4])
        result, error = sample.validate(False)

        self.assertTrue(result)
        self.assertIsNone(error)

        sample = Sample(property_seven=[])
        result, error = sample.validate(False)

        self.assertFalse(result)
        assert error, "Expected error to be defined"
        self.assertIsNotNone(error.property_errors.get("property_seven"))

        sample = Sample(property_eight=[1, 2, 3, 4, 5])
        result, error = sample.validate(False)

        self.assertFalse(result)
        assert error, "Expected error to be defined"
        self.assertIsNotNone(error.property_errors.get("property_eight"))


if __name__ == "__main__":
    unittest.main()
