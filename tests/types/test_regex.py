import unittest
import flask_schema.types
import flask_schema.errors


class RegexTest(unittest.TestCase):

    # REGEX TESTS

    def test_regex(self):
        prop = flask_schema.types.Regex(r"HELL")
        self.assertEqual(prop("HELLO"), "HELLO")

    def test_regex_fail(self):
        prop = flask_schema.types.Regex("ELL")
        self.assertRaises(flask_schema.errors.SchemaValidationError, prop, "nope")

    # TODO test regex fail

    # PROPERTY TESTS

    def test_nullable_by_default(self):
        prop = flask_schema.types.Regex("")
        self.assertIsNone(prop(None))

    def test_nullable_allows_null(self):
        prop = flask_schema.types.Regex("", nullable=True)
        self.assertIsNone(prop(None))

    def test_nullable_raises_error(self):
        prop = flask_schema.types.Regex("", nullable=False)
        self.assertRaises(flask_schema.errors.SchemaValidationError, prop, None)

    def test_default_is_none(self):
        prop = flask_schema.types.Regex("", default=None)
        self.assertIsNone(prop(None))

    def test_default_value(self):
        prop = flask_schema.types.Regex("", default="yep")
        self.assertEqual(prop(None), "yep")

    def test_default_passive_when_value_not_none(self):
        prop = flask_schema.types.Regex("", default="pey")
        self.assertEqual(prop("yep"), "yep")

    def test_default_callable(self):
        prop = flask_schema.types.Regex("", default=lambda: "yep")
        self.assertEqual(prop(None), "yep")

    def test_wrong_type(self):
        prop = flask_schema.types.Regex("", callback=None)
        self.assertRaises(flask_schema.errors.SchemaValidationError, prop, 12)

    def test_callback(self):
        prop = flask_schema.types.Regex("", callback=lambda v: f"{v}{v}")
        self.assertEqual(prop("yep"), "yepyep")

    def test_no_callback(self):
        prop = flask_schema.types.Regex("", callback=None)
        self.assertEqual(prop("yep"), "yep")
