import unittest
import flask_schema.types
import flask_schema.errors


class IntTest(unittest.TestCase):

    # INT TESTS

    def test_fails_if_float(self):
        prop = flask_schema.types.Int()
        self.assertRaises(flask_schema.errors.SchemaValidationError, prop, 1.5)

    # NUMBER TESTS

    def test_min_only(self):
        prop = flask_schema.types.Int(min_value=0)
        self.assertEqual(prop(5), 5)

    def test_min_only_out_of_range(self):
        prop = flask_schema.types.Int(min_value=0)
        self.assertRaises(flask_schema.errors.SchemaValidationError, prop, -1)

    def test_max_only(self):
        prop = flask_schema.types.Int(max_value=10)
        self.assertEqual(prop(5), 5)

    def test_max_only_out_of_range(self):
        prop = flask_schema.types.Int(max_value=10)
        self.assertRaises(flask_schema.errors.SchemaValidationError, prop, 20)

    def test_min_and_max(self):
        prop = flask_schema.types.Int(min_value=0, max_value=10)
        self.assertEqual(prop(5), 5)

    def test_min_and_max_out_of_range(self):
        prop = flask_schema.types.Int(min_value=0, max_value=10)
        self.assertRaises(flask_schema.errors.SchemaValidationError, prop, 20)

    def test_no_range(self):
        prop = flask_schema.types.Int()
        self.assertEqual(prop(20), 20)

    # PROPERTY TESTS

    def test_nullable_by_default(self):
        prop = flask_schema.types.Int()
        self.assertIsNone(prop(None))

    def test_nullable_allows_null(self):
        prop = flask_schema.types.Int(nullable=True)
        self.assertIsNone(prop(None))

    def test_nullable_raises_error(self):
        prop = flask_schema.types.Int(nullable=False)
        self.assertRaises(flask_schema.errors.SchemaValidationError, prop, None)

    def test_default_is_none(self):
        prop = flask_schema.types.Int(default=None)
        self.assertIsNone(prop(None))

    def test_default_value(self):
        prop = flask_schema.types.Int(default=12)
        self.assertEqual(prop(None), 12)

    def test_default_passive_when_value_not_none(self):
        prop = flask_schema.types.Int(default=12)
        self.assertEqual(prop(21), 21)

    def test_default_callable(self):
        prop = flask_schema.types.Int(default=lambda: 12)
        self.assertEqual(prop(None), 12)

    def test_wrong_type(self):
        prop = flask_schema.types.Int(callback=None)
        self.assertRaises(flask_schema.errors.SchemaValidationError, prop, "nope")

    def test_callback(self):
        prop = flask_schema.types.Int(callback=lambda v: v * 2)
        self.assertEqual(prop(12), 24)

    def test_no_callback(self):
        prop = flask_schema.types.Int(callback=None)
        self.assertEqual(prop(12), 12)
