import unittest
import flask_schema.types
import flask_schema.errors


class PropertyTest(unittest.TestCase):
    def test_nullable_by_default(self):
        prop = flask_schema.types.Property(int)
        self.assertIsNone(prop(None))

    def test_nullable_allows_null(self):
        prop = flask_schema.types.Property(int, nullable=True)
        self.assertIsNone(prop(None))

    def test_nullable_raises_error(self):
        prop = flask_schema.types.Property(int, nullable=False)
        self.assertRaises(flask_schema.errors.SchemaValidationError, prop, None)

    def test_default_is_none(self):
        prop = flask_schema.types.Property(int, default=None)
        self.assertIsNone(prop(None))

    def test_default_value(self):
        prop = flask_schema.types.Property(int, default=12)
        self.assertEqual(prop(None), 12)

    def test_default_passive_when_value_not_none(self):
        prop = flask_schema.types.Property(int, default=12)
        self.assertEqual(prop(21), 21)

    def test_default_callable(self):
        prop = flask_schema.types.Property(int, default=lambda: 12)
        self.assertEqual(prop(None), 12)

    def test_wrong_type(self):
        prop = flask_schema.types.Property(str, callback=None)
        self.assertRaises(flask_schema.errors.SchemaValidationError, prop, 12)

    def test_callback(self):
        prop = flask_schema.types.Property(int, callback=lambda v: v * 2)
        self.assertEqual(prop(12), 24)

    def test_no_callback(self):
        prop = flask_schema.types.Property(int, callback=None)
        self.assertEqual(prop(12), 12)
