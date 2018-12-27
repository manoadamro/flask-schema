import unittest
import flask_schema.types
import flask_schema.errors


class BoolTest(unittest.TestCase):
    def test_nullable_by_default(self):
        prop = flask_schema.types.Bool()
        self.assertIsNone(prop(None))

    def test_nullable_allows_null(self):
        prop = flask_schema.types.Bool(nullable=True)
        self.assertIsNone(prop(None))

    def test_nullable_raises_error(self):
        prop = flask_schema.types.Bool(nullable=False)
        self.assertRaises(flask_schema.errors.SchemaValidationError, prop, None)

    def test_default_is_none(self):
        prop = flask_schema.types.Bool(default=None)
        self.assertIsNone(prop(None))

    def test_default_value(self):
        prop = flask_schema.types.Bool(default=True)
        self.assertEqual(prop(None), True)

    def test_default_passive_when_value_not_none(self):
        prop = flask_schema.types.Bool(default=False)
        self.assertEqual(prop(True), True)

    def test_default_callable(self):
        prop = flask_schema.types.Bool(default=lambda: True)
        self.assertEqual(prop(None), True)

    def test_wrong_type(self):
        prop = flask_schema.types.Bool(callback=None)
        self.assertRaises(flask_schema.errors.SchemaValidationError, prop, 12)

    def test_callback(self):
        prop = flask_schema.types.Bool(callback=lambda v: False)
        self.assertEqual(prop(True), False)

    def test_no_callback(self):
        prop = flask_schema.types.Bool(callback=None)
        self.assertEqual(prop(True), True)
