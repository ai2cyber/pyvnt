import unittest

from pyvnt import Entity, descriptor
from pyvnt.validators.numeric import at_least, at_most, is_divisible_by, is_in_range, is_negative, is_positive


class Sample(Entity):
    property_one: int = descriptor(default=0, validations=[at_least(0)])
    property_two: int = descriptor(default=-1, validations=[at_least(0).negate()])
    property_three: int = descriptor(default=0, validations=[at_most(10)])
    property_four: int = descriptor(default=11, validations=[at_most(10).negate()])
    property_five: int = descriptor(default=2, validations=[is_divisible_by(2)])
    property_six: int = descriptor(default=3, validations=[is_divisible_by(2).negate()])
    property_seven: int = descriptor(default=0, validations=[is_in_range(0, 5)])
    property_eight: int = descriptor(default=6, validations=[is_in_range(0, 5).negate()])
    property_nine: int = descriptor(default=-1, validations=[is_negative()])
    property_ten: int = descriptor(default=1, validations=[is_negative().negate()])
    property_eleven: int = descriptor(default=1, validations=[is_positive()])
    property_twelve: int = descriptor(default=-1, validations=[is_positive().negate()])


class TestNumericValidators(unittest.TestCase):
    def test_at_least(self):
        sample = Sample(property_one=0, property_two=-1)
        result, error = sample.validate(False)

        self.assertTrue(result)
        self.assertIsNone(error)

        sample = Sample(property_one=-1)
        result, error = sample.validate(False)

        self.assertFalse(result)
        assert error, "Expected error to be defined"
        self.assertIsNotNone(error.property_errors.get("property_one"))

        sample = Sample(property_two=1)
        result, error = sample.validate(False)

        self.assertFalse(result)
        assert error, "Expected error to be defined"
        self.assertIsNotNone(error.property_errors.get("property_two"))

    def test_at_most(self):
        sample = Sample(property_three=0, property_four=11)
        result, error = sample.validate(False)

        self.assertTrue(result)
        self.assertIsNone(error)

        sample = Sample(property_three=11)
        result, error = sample.validate(False)

        self.assertFalse(result)
        assert error, "Expected error to be defined"
        self.assertIsNotNone(error.property_errors.get("property_three"))

        sample = Sample(property_four=9)
        result, error = sample.validate(False)

        self.assertFalse(result)
        assert error, "Expected error to be defined"
        self.assertIsNotNone(error.property_errors.get("property_four"))

    def test_is_divisible_by(self):
        sample = Sample(property_five=2, property_six=3)
        result, error = sample.validate(False)

        self.assertTrue(result)
        self.assertIsNone(error)

        sample = Sample(property_five=3)
        result, error = sample.validate(False)

        self.assertFalse(result)
        assert error, "Expected error to be defined"
        self.assertIsNotNone(error.property_errors.get("property_five"))

        sample = Sample(property_six=2)
        result, error = sample.validate(False)

        self.assertFalse(result)
        assert error, "Expected error to be defined"
        self.assertIsNotNone(error.property_errors.get("property_six"))

    def test_is_in_range(self):
        sample = Sample(property_seven=0, property_eight=6)
        result, error = sample.validate(False)

        self.assertTrue(result)
        self.assertIsNone(error)

        sample = Sample(property_seven=6)
        result, error = sample.validate(False)

        self.assertFalse(result)
        assert error, "Expected error to be defined"
        self.assertIsNotNone(error.property_errors.get("property_seven"))

        sample = Sample(property_eight=4)
        result, error = sample.validate(False)

        self.assertFalse(result)
        assert error, "Expected error to be defined"
        self.assertIsNotNone(error.property_errors.get("property_eight"))

    def test_is_negative(self):
        sample = Sample(property_nine=-1, property_ten=1)
        result, error = sample.validate(False)

        self.assertTrue(result)
        self.assertIsNone(error)

        sample = Sample(property_nine=1)
        result, error = sample.validate(False)

        self.assertFalse(result)
        assert error, "Expected error to be defined"
        self.assertIsNotNone(error.property_errors.get("property_nine"))

        sample = Sample(property_ten=-1)
        result, error = sample.validate(False)

        self.assertFalse(result)
        assert error, "Expected error to be defined"
        self.assertIsNotNone(error.property_errors.get("property_ten"))

    def test_is_positive(self):
        sample = Sample(property_eleven=1, property_twelve=-1)
        result, error = sample.validate(False)

        self.assertTrue(result)
        self.assertIsNone(error)

        sample = Sample(property_eleven=-1)
        result, error = sample.validate(False)

        self.assertFalse(result)
        assert error, "Expected error to be defined"
        self.assertIsNotNone(error.property_errors.get("property_eleven"))

        sample = Sample(property_twelve=1)
        result, error = sample.validate(False)

        self.assertFalse(result)
        assert error, "Expected error to be defined"
        self.assertIsNotNone(error.property_errors.get("property_twelve"))


if __name__ == "__main__":
    unittest.main()
