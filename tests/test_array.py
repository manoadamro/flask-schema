import unittest
import flask_schema.types
import flask_schema.errors


class BasicSchema(flask_schema.types.Schema):
    thing = flask_schema.types.Bool()


class ArrayTest(unittest.TestCase):
    def test_min_only(self):
        prop = flask_schema.types.Array(flask_schema.types.Bool, min_length=0)
        self.assertEqual(prop([True, True]), [True, True])

    def test_min_only_out_of_range(self):
        prop = flask_schema.types.Array(flask_schema.types.Bool, min_length=1)
        self.assertRaises(flask_schema.errors.SchemaValidationError, prop, [])

    def test_max_only(self):
        prop = flask_schema.types.Array(flask_schema.types.Bool, max_length=3)
        self.assertEqual(prop([True, True]), [True, True])

    def test_max_only_out_of_range(self):
        prop = flask_schema.types.Array(flask_schema.types.Bool, max_length=3)
        self.assertRaises(
            flask_schema.errors.SchemaValidationError, prop, [True, True, True, True]
        )

    def test_min_and_max(self):
        prop = flask_schema.types.Array(
            flask_schema.types.Bool, min_length=0, max_length=3
        )
        self.assertEqual(prop([True, True]), [True, True])

    def test_min_and_max_out_of_range(self):
        prop = flask_schema.types.Array(
            flask_schema.types.Bool, min_length=0, max_length=3
        )
        self.assertRaises(
            flask_schema.errors.SchemaValidationError, prop, [True, True, True, True]
        )

    def test_no_range(self):
        prop = flask_schema.types.Array(flask_schema.types.Bool)
        self.assertEqual(prop([True, True, True, True]), [True, True, True, True])

    def test_array_of_property(self):
        prop = flask_schema.types.Array(flask_schema.types.Bool)
        self.assertEqual(prop([True, True]), [True, True])

    def test_array_of_property_fails(self):
        prop = flask_schema.types.Array(flask_schema.types.Bool)
        self.assertRaises(flask_schema.errors.SchemaValidationError, prop, [True, ""])

    def test_nullable_by_default(self):
        prop = flask_schema.types.Array(BasicSchema)
        self.assertIsNone(prop(None))

    def test_nullable_allows_null(self):
        prop = flask_schema.types.Array(BasicSchema, nullable=True)
        self.assertIsNone(prop(None))

    def test_nullable_raises_error(self):
        prop = flask_schema.types.Array(BasicSchema, nullable=False)
        self.assertRaises(flask_schema.errors.SchemaValidationError, prop, None)

    def test_wrong_type(self):
        prop = flask_schema.types.Array(BasicSchema, callback=None)
        self.assertRaises(flask_schema.errors.SchemaValidationError, prop, 12)

    def test_callback(self):
        prop = flask_schema.types.Array(
            BasicSchema, callback=lambda v: [{"thing": True}]
        )
        self.assertEqual(prop([{"thing": False}, {"thing": False}]), [{"thing": True}])

    def test_no_callback(self):
        prop = flask_schema.types.Array(BasicSchema, callback=None)
        self.assertEqual(prop([{"thing": False}]), [{"thing": False}])
