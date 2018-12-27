import unittest
import flask_schema.types
import flask_schema.errors


class BasicSchema(flask_schema.types.Schema):
    thing = flask_schema.types.Bool()


class ObjectTest(unittest.TestCase):
    def test_strict(self):
        prop = flask_schema.types.Object(BasicSchema, strict=True)
        self.assertRaises(
            flask_schema.errors.SchemaValidationError,
            prop,
            {"thing": False, "other": 12},
        )

    def test_nullable_by_default(self):
        prop = flask_schema.types.Object(BasicSchema)
        self.assertIsNone(prop(None))

    def test_nullable_allows_null(self):
        prop = flask_schema.types.Object(BasicSchema, nullable=True)
        self.assertIsNone(prop(None))

    def test_nullable_raises_error(self):
        prop = flask_schema.types.Object(BasicSchema, nullable=False)
        self.assertRaises(flask_schema.errors.SchemaValidationError, prop, None)

    def test_wrong_type(self):
        prop = flask_schema.types.Object(BasicSchema, callback=None)
        self.assertRaises(flask_schema.errors.SchemaValidationError, prop, 12)

    def test_callback(self):
        prop = flask_schema.types.Object(
            BasicSchema, callback=lambda v: {"thing": True}
        )
        self.assertEqual(prop({"thing": False}), {"thing": True})

    def test_no_callback(self):
        prop = flask_schema.types.Object(BasicSchema, callback=None)
        self.assertEqual(prop({"thing": False}), {"thing": False})
