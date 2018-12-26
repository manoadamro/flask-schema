import unittest
import flask_schema.types
import flask_schema.errors


class StringTest(unittest.TestCase):

    # STRING TESTS

    def test_min_only(self):
        prop = flask_schema.types.String(min_length=0)
        self.assertEqual(prop("12345"), "12345")

    def test_min_only_out_of_range(self):
        prop = flask_schema.types.String(min_length=1)
        self.assertRaises(flask_schema.errors.SchemaValidationError, prop, "")

    def test_max_only(self):
        prop = flask_schema.types.String(max_length=10)
        self.assertEqual(prop("12345"), "12345")

    def test_max_only_out_of_range(self):
        prop = flask_schema.types.String(max_length=10)
        self.assertRaises(
            flask_schema.errors.SchemaValidationError, prop, "12345123451234512345"
        )

    def test_min_and_max(self):
        prop = flask_schema.types.String(min_length=0, max_length=10)
        self.assertEqual(prop("12345"), "12345")

    def test_min_and_max_out_of_range(self):
        prop = flask_schema.types.String(min_length=0, max_length=10)
        self.assertRaises(
            flask_schema.errors.SchemaValidationError, prop, "12345123451234512345"
        )

    def test_no_range(self):
        prop = flask_schema.types.String()
        self.assertEqual(prop("12345123451234512345"), "12345123451234512345")

    # PROPERTY TESTS

    def test_nullable_by_default(self):
        prop = flask_schema.types.String()
        self.assertIsNone(prop(None))

    def test_nullable_allows_null(self):
        prop = flask_schema.types.String(nullable=True)
        self.assertIsNone(prop(None))

    def test_nullable_raises_error(self):
        prop = flask_schema.types.String(nullable=False)
        self.assertRaises(flask_schema.errors.SchemaValidationError, prop, None)

    def test_default_is_none(self):
        prop = flask_schema.types.String(default=None)
        self.assertIsNone(prop(None))

    def test_default_value(self):
        prop = flask_schema.types.String(default="yep")
        self.assertEqual(prop(None), "yep")

    def test_default_passive_when_value_not_none(self):
        prop = flask_schema.types.String(default="pey")
        self.assertEqual(prop("yep"), "yep")

    def test_default_callable(self):
        prop = flask_schema.types.String(default=lambda: "yep")
        self.assertEqual(prop(None), "yep")

    def test_wrong_type(self):
        prop = flask_schema.types.String(callback=None)
        self.assertRaises(flask_schema.errors.SchemaValidationError, prop, 12)

    def test_callback(self):
        prop = flask_schema.types.String(callback=lambda v: f"{v}{v}")
        self.assertEqual(prop("yep"), "yepyep")

    def test_no_callback(self):
        prop = flask_schema.types.String(callback=None)
        self.assertEqual(prop("yep"), "yep")
