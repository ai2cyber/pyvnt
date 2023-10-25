import unittest
from typing import Any, Optional

from pyvnt import Entity, descriptor
from pyvnt.validators.common import equals, is_defined, is_empty, is_optional, nested_validator


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
    property_eight: NestedSample = descriptor(default_factory=NestedSample, validations=[nested_validator()])


class TestCommonValidators(unittest.TestCase):
    def test_equals(self):
        sample = Sample(property_one=1, property_two=2)
        result, error = sample.validate(False)

        self.assertTrue(result)
        self.assertIsNone(error)

        sample = Sample(property_one=1, property_two=1)
        result, error = sample.validate(False)

        self.assertFalse(result)
        assert error, "Expected error to be defined"
        self.assertIsNotNone(error.property_errors.get("property_two"))

        sample = Sample(property_one=2, property_two=0)
        result, error = sample.validate(False)

        self.assertFalse(result)
        assert error, "Expected error to be defined"
        self.assertIsNotNone(error.property_errors.get("property_one"))

    def test_is_defined(self):
        sample = Sample(property_three=1, property_four=None)
        result, error = sample.validate(False)

        self.assertTrue(result)
        self.assertIsNone(error)

        sample = Sample(property_three=None, property_four=None)
        result, error = sample.validate(False)

        self.assertFalse(result)
        assert error, "Expected error to be defined"
        self.assertIsNotNone(error.property_errors.get("property_three"))

        sample = Sample(property_three=1, property_four=1)
        result, error = sample.validate(False)

        self.assertFalse(result)
        assert error, "Expected error to be defined"
        self.assertIsNotNone(error.property_errors.get("property_four"))

    def test_is_empty(self):
        samples = [
            Sample(property_five=[], property_six=[1]),
            Sample(property_five=(), property_six=(1,)),
            Sample(property_five=set(), property_six={1}),
            Sample(property_five="", property_six="1"),
            Sample(property_five=range(0), property_six=range(1)),
            Sample(property_five=0, property_six=1),
            Sample(property_five=0.0, property_six=3.14),
            Sample(property_five=0j, property_six=1j),
        ]

        for sample in samples:
            result, error = sample.validate(False)
            self.assertTrue(result)
            self.assertIsNone(error)

        samples = [
            Sample(property_five=[1], property_six=[1]),
            Sample(property_five=(1), property_six=(1)),
            Sample(property_five=set([1]), property_six=set([1])),
            Sample(property_five="1", property_six="1"),
            Sample(property_five=range(1), property_six=range(1)),
            Sample(property_five=1, property_six=1),
            Sample(property_five=3.14, property_six=3.14),
            Sample(property_five=1j, property_six=1j),
        ]

        for sample in samples:
            result, error = sample.validate(False)

            self.assertFalse(result)
            assert error, "Expected error to be defined"
            self.assertIsNotNone(error.property_errors.get("property_five"))

        samples = [
            Sample(property_five=[], property_six=[]),
            Sample(property_five=(), property_six=()),
            Sample(property_five=set(), property_six=set()),
            Sample(property_five="", property_six=""),
            Sample(property_five=range(0), property_six=range(0)),
            Sample(property_five=0, property_six=0),
            Sample(property_five=0.0, property_six=0.0),
            Sample(property_five=0j, property_six=0j),
        ]

        for sample in samples:
            result, error = sample.validate(False)

            self.assertFalse(result)
            assert error, "Expected error to be defined"
            self.assertIsNotNone(error.property_errors.get("property_six"))

    def test_is_optional(self):
        sample = Sample(property_seven=None)
        result, error = sample.validate(False)

        self.assertTrue(result)
        self.assertIsNone(error)

        sample = Sample(property_seven=1)
        result, error = sample.validate(False)

        self.assertTrue(result)
        self.assertIsNone(error)

        sample = Sample(property_seven=2)
        result, error = sample.validate(False)

        self.assertFalse(result)
        assert error, "Expected error to be defined"
        self.assertIsNotNone(error.property_errors.get("property_seven"))

    def test_validate_nested(self):
        sample = Sample(property_eight=NestedSample(property_one=1))
        result, error = sample.validate(False)

        self.assertTrue(result)
        self.assertIsNone(error)

        sample = Sample(property_eight=NestedSample(property_one=2))
        result, error = sample.validate(False)

        self.assertFalse(result)
        assert error, "Expected error to be defined"
        self.assertIsNotNone(error.property_errors.get("property_eight"))


if __name__ == "__main__":
    unittest.main()
