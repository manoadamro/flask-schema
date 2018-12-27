import unittest
import flask_schema.types
import flask_schema.errors


class NumberTest(unittest.TestCase):
    def test_property_choice(self):
        prop = flask_schema.types.Choice(
            [flask_schema.types.Bool(), flask_schema.types.Int()]
        )
        self.assertEqual(prop(12), 12)
        self.assertEqual(prop(True), True)
        self.assertRaises(flask_schema.errors.SchemaValidationError, prop, 4.5)

    def test_invalid_choice(self):
        prop = flask_schema.types.Choice([1, 2, 3])
        self.assertRaises(flask_schema.errors.SchemaValidationError, prop, 4)

    def test_nullable_by_default(self):
        prop = flask_schema.types.Choice([1, 2, 3])
        self.assertIsNone(prop(None))

    def test_nullable_allows_null(self):
        prop = flask_schema.types.Choice([1, 2, 3], nullable=True)
        self.assertIsNone(prop(None))

    def test_nullable_raises_error(self):
        prop = flask_schema.types.Choice([1, 2, 3], nullable=False)
        self.assertRaises(flask_schema.errors.SchemaValidationError, prop, None)

    def test_default_is_none(self):
        prop = flask_schema.types.Choice([1, 2, 3], default=None)
        self.assertIsNone(prop(None))

    def test_default_value(self):
        prop = flask_schema.types.Choice([1, 2, 3], default=2)
        self.assertEqual(prop(None), 2)

    def test_default_passive_when_value_not_none(self):
        prop = flask_schema.types.Choice([1, 2, 3], default=2)
        self.assertEqual(prop(1), 1)

    def test_default_callable(self):
        prop = flask_schema.types.Choice([1, 2, 3], default=lambda: 1)
        self.assertEqual(prop(None), 1)

    def test_wrong_type(self):
        prop = flask_schema.types.Choice([1, 2, 3], callback=None)
        self.assertRaises(flask_schema.errors.SchemaValidationError, prop, "nope")

    def test_callback(self):
        prop = flask_schema.types.Choice([1, 2, 3], callback=lambda v: v * 2)
        self.assertEqual(prop(1), 2)

    def test_no_callback(self):
        prop = flask_schema.types.Choice([1, 2, 3], callback=None)
        self.assertEqual(prop(1), 1)
