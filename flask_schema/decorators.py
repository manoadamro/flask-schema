import functools
from typing import Any, Callable, ClassVar, Union, Type
import flask
from . import types, errors


class SchemaProtect:
    def __init__(
        self,
        rule: Union[
            bool,
            Type[types.Schema],
            types.Schema,
            Type[types.Property],
            types.Property,
            None,
        ],
    ):
        if isinstance(rule, type) and issubclass(rule, (types.Property, types.Schema)):
            rule = rule()
        self.rule = rule

    @property
    def request_body(self):
        if self.rule is True:
            if not flask.request.is_json:
                raise errors.SchemaValidationError()  # TODO expected json
            return flask.request.json
        if self.rule is False:
            if flask.request.is_json:
                raise errors.SchemaValidationError()  # TODO unexpected json
            return None
        if self.rule is None:
            if flask.request.is_json:
                return flask.request.json
            return None
        if isinstance(self.rule, (types.Property, types.Schema)):
            return self.rule(flask.request.json)
        raise errors.SchemaValidationError()  # TODO unknown rule type

    def __call__(self, func: Callable) -> Callable:
        @functools.wraps(func)
        def _call(*args: Any, **kwargs: Any) -> Any:
            return func(self.request_body, *args, **kwargs)

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
