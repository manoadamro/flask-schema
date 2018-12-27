import unittest
import unittest.mock
import flask
import flask_schema.types
import flask_schema.decorators
import flask_schema.errors


class TestSchema(flask_schema.types.Schema):
    __strict__ = True
    test = flask_schema.types.Bool()


def route(json_body):
    return json_body


class SchemaProtectTest(unittest.TestCase):
    def setUp(self):
        self.app = flask.Flask("TestFlask")

    @unittest.mock.patch.object(
        flask, "request", unittest.mock.Mock(json={"test": True})
    )
    def test_expects_specific_json(self):
        func = flask_schema.decorators.SchemaProtect(TestSchema)(route)
        self.assertEqual(func(), {"test": True})

    @unittest.mock.patch.object(
        flask, "request", unittest.mock.Mock(json={"nope": True})
    )
    def test_fails_when_expecting_specific_json(self):
        func = flask_schema.decorators.SchemaProtect(TestSchema)(route)
        self.assertRaises(flask_schema.errors.SchemaValidationError, func)

    @unittest.mock.patch.object(
        flask, "request", unittest.mock.Mock(json={"anything": 123})
    )
    def test_expects_any_json(self):
        func = flask_schema.decorators.SchemaProtect(True)(route)
        self.assertEqual(func(), {"anything": 123})

    @unittest.mock.patch.object(flask, "request", unittest.mock.Mock(is_json=False))
    def test_fails_when_expecting_any_json(self):
        func = flask_schema.decorators.SchemaProtect(True)(route)
        self.assertRaises(flask_schema.errors.SchemaValidationError, func)

    @unittest.mock.patch.object(flask, "request", unittest.mock.Mock(is_json=False))
    def test_expects_no_json(self):
        func = flask_schema.decorators.SchemaProtect(False)(route)
        self.assertEqual(func(), None)

    @unittest.mock.patch.object(flask, "request", unittest.mock.Mock(is_json=True))
    def test_fails_when_expecting_no_json(self):
        func = flask_schema.decorators.SchemaProtect(False)(route)
        self.assertRaises(flask_schema.errors.SchemaValidationError, func)

    @unittest.mock.patch.object(flask, "request", unittest.mock.Mock(is_json=False))
    def test_expects_any_or_no_json_gets_none(self):
        func = flask_schema.decorators.SchemaProtect(None)(route)
        self.assertEqual(func(), None)

    @unittest.mock.patch.object(
        flask, "request", unittest.mock.Mock(is_json=True, json={"yep": 123})
    )
    def test_expects_any_or_no_json_gets_json(self):
        func = flask_schema.decorators.SchemaProtect(None)(route)
        self.assertEqual(func(), {"yep": 123})

    @unittest.mock.patch.object(flask, "request", unittest.mock.Mock())
    def test_wrong_type(self):
        func = flask_schema.decorators.SchemaProtect(123)(route)
        self.assertRaises(flask_schema.errors.SchemaValidationError, func)
