import unittest
import datetime
import flask_schema.types
import flask_schema.errors


class DateTimeTest(unittest.TestCase):

    epoc = datetime.datetime(year=1970, month=1, day=1)
    millenium = datetime.datetime(year=2000, month=1, day=1)
    millenium05 = datetime.datetime(year=2005, month=1, day=1)

    # TODO from timestamp

    # TODO from string

    # TODO from string with time zone

    # TODO from string with Z

    # TODO wrong type

    def test_min_only(self):
        prop = flask_schema.types.DateTime(min_value=self.epoc)
        self.assertEqual(prop(self.millenium), self.millenium)

    def test_min_only_out_of_range(self):
        prop = flask_schema.types.DateTime(min_value=self.millenium)
        self.assertRaises(flask_schema.errors.SchemaValidationError, prop, self.epoc)

    def test_max_only(self):
        prop = flask_schema.types.DateTime(max_value=self.millenium05)
        self.assertEqual(prop(self.millenium), self.millenium)

    def test_max_only_out_of_range(self):
        prop = flask_schema.types.DateTime(max_value=self.millenium)
        self.assertRaises(
            flask_schema.errors.SchemaValidationError, prop, self.millenium05
        )

    def test_min_and_max(self):
        prop = flask_schema.types.DateTime(
            min_value=self.epoc, max_value=self.millenium05
        )
        self.assertEqual(prop(self.millenium), self.millenium)

    def test_min_and_max_out_of_range(self):
        prop = flask_schema.types.DateTime(
            min_value=self.epoc, max_value=self.millenium
        )
        self.assertRaises(
            flask_schema.errors.SchemaValidationError, prop, self.millenium05
        )

    def test_no_range(self):
        prop = flask_schema.types.DateTime()
        self.assertEqual(prop(self.epoc), self.epoc)

    # PROPERTY TESTS

    def test_nullable_by_default(self):
        prop = flask_schema.types.DateTime()
        self.assertIsNone(prop(None))

    def test_nullable_allows_null(self):
        prop = flask_schema.types.DateTime(nullable=True)
        self.assertIsNone(prop(None))

    def test_nullable_raises_error(self):
        prop = flask_schema.types.DateTime(nullable=False)
        self.assertRaises(flask_schema.errors.SchemaValidationError, prop, None)

    def test_default_is_none(self):
        prop = flask_schema.types.DateTime(default=None)
        self.assertIsNone(prop(None))

    def test_default_value(self):
        prop = flask_schema.types.DateTime(default=self.epoc)
        self.assertEqual(prop(None), self.epoc)

    def test_default_passive_when_value_not_none(self):
        prop = flask_schema.types.DateTime(default=self.epoc)
        self.assertEqual(prop(self.millenium), self.millenium)

    def test_default_callable(self):
        prop = flask_schema.types.DateTime(default=lambda: self.millenium)
        self.assertEqual(prop(None), self.millenium)

    def test_wrong_type(self):
        prop = flask_schema.types.DateTime(callback=None)
        self.assertRaises(flask_schema.errors.SchemaValidationError, prop, "nope")

    def test_callback(self):
        prop = flask_schema.types.DateTime(
            callback=lambda v: v + datetime.timedelta(days=5)
        )
        self.assertEqual(prop(self.epoc), datetime.datetime(year=1970, month=1, day=6))

    def test_no_callback(self):
        prop = flask_schema.types.DateTime(callback=None)
        self.assertEqual(prop(self.epoc), self.epoc)
