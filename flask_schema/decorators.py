import functools
import os
from typing import Any, Callable, ClassVar, Dict, Type, Union

import flask

from . import errors, types


class SchemaProtect:
    validate_output = os.environ.get("FLASK_SCHEMA_VALIDATE_OUTPUT", True)

    def __init__(
        self,
        schema: Union[
            bool,
            Type[types.Schema],
            types.Schema,
            Type[types.Property],
            types.Property,
            None,
        ],
        output: Union[
            bool,
            Type[types.Schema],
            types.Schema,
            Type[types.Property],
            types.Property,
            None,
        ] = None,
    ):
        self.schema = self._resolve(schema)
        self.output = self._resolve(output)

    @staticmethod
    def _resolve(value: Any) -> Any:
        if isinstance(value, type) and issubclass(
            value, (types.Property, types.Schema)
        ):
            return value()
        return value

    def request_body(self):
        if self.schema is True:
            if not flask.request.is_json:
                raise errors.SchemaValidationError()  # TODO expected json
            return flask.request.json
        if self.schema is False:
            if flask.request.is_json:
                raise errors.SchemaValidationError()  # TODO unexpected json
            return None
        if self.schema is None:
            if flask.request.is_json:
                return flask.request.json
            return None
        if isinstance(self.schema, (types.Property, types.Schema)):
            return self.schema(flask.request.json)
        raise errors.SchemaValidationError()  # TODO unknown rule type

    def response_body(self, response: Union[Dict, types.Property, types.Schema, None]):
        if not self.validate_output or self.output is None:
            return response
        if self.output is False:
            raise errors.SchemaValidationError()  # TODO response should be None
        if self.output is True:
            if not isinstance(response, dict):
                raise errors.SchemaValidationError()
            return response
        if isinstance(self.output, (types.Property, types.Schema)):
            return self.output(response)
        raise errors.SchemaValidationError()  # TODO unknown rule type

    def __call__(self, func: Callable) -> Callable:
        @functools.wraps(func)
        def _call(*args: Any, **kwargs: Any) -> Any:
            response = func(self.request_body(), *args, **kwargs)
            return self.response_body(response)

        return _call


class CustomProperty:
    def __init__(self, *args: Type, **kwargs: Any):
        self.prop = types.Property(*args, **kwargs)

    def __call__(self, func: ClassVar) -> Callable:
        @functools.wraps(func)
        def _wrapped(value: Any):
            value: Any = self.prop(value)
            return func(func.__class__, value)

        return _wrapped
