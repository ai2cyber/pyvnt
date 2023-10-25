import unittest
from typing import Dict, Mapping

from pyvnt import Entity, descriptor
from pyvnt.validators.mappings import has_key, has_key_value_pair, has_value


class Sample(Entity):
    property_one: Mapping[int, str] = descriptor(default_factory=lambda: {1: "2"}, validations=[has_key(1)])
    property_two: Mapping[int, str] = descriptor(default_factory=lambda: {2: "3"}, validations=[has_key(1).negate()])
    property_three: Mapping[int, str] = descriptor(default_factory=lambda: {3: "5"}, validations=[has_value("5")])
    property_four: Mapping[int, str] = descriptor(
        default_factory=lambda: {4: "6"}, validations=[has_value("5").negate()]
    )
    property_five: Dict[int, str] = descriptor(
        default_factory=lambda: {3: "5"},
        validations=[has_key_value_pair((3, "5"))],
    )
    property_six: Dict[int, str] = descriptor(
        default_factory=lambda: {4: "6"},
        validations=[has_key_value_pair((3, "5")).negate()],
    )


class TestMappingValidators(unittest.TestCase):
    def test_has_key(self):
        sample = Sample(property_one={1: "2"}, property_two={2: "3"})
        result, error = sample.validate(False)

        self.assertTrue(result)
        self.assertIsNone(error)

        sample = Sample(property_one={2: "3"}, property_two={2: "3"})
        result, error = sample.validate(False)

        self.assertFalse(result)
        assert error, "Expected error to be defined"
        self.assertIsNotNone(error.property_errors.get("property_one"))

        sample = Sample(property_one={1: "2"}, property_two={1: "2"})
        result, error = sample.validate(False)

        self.assertFalse(result)
        assert error, "Expected error to be defined"
        self.assertIsNotNone(error.property_errors.get("property_two"))

    def test_has_value(self):
        sample = Sample(property_three={3: "5"}, property_four={4: "6"})
        result, error = sample.validate(False)

        self.assertTrue(result)
        self.assertIsNone(error)

        sample = Sample(property_three={4: "6"}, property_four={4: "6"})
        result, error = sample.validate(False)

        self.assertFalse(result)
        assert error, "Expected error to be defined"
        self.assertIsNotNone(error.property_errors.get("property_three"))

        sample = Sample(property_three={3: "5"}, property_four={1: "5"})
        result, error = sample.validate(False)

        self.assertFalse(result)
        assert error, "Expected error to be defined"
        self.assertIsNotNone(error.property_errors.get("property_four"))

    def test_has_key_value_pair(self):
        sample = Sample(property_five={3: "5"}, property_six={4: "6"})
        result, error = sample.validate(False)

        self.assertTrue(result)
        self.assertIsNone(error)

        sample = Sample(property_five={4: "6"}, property_six={4: "6"})
        result, error = sample.validate(False)

        self.assertFalse(result)
        assert error, "Expected error to be defined"
        self.assertIsNotNone(error.property_errors.get("property_five"))

        sample = Sample(property_five={3: "5"}, property_six={3: "5"})
        result, error = sample.validate(False)

        self.assertFalse(result)
        assert error, "Expected error to be defined"
        self.assertIsNotNone(error.property_errors.get("property_six"))


if __name__ == "__main__":
    unittest.main()
