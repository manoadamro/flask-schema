import functools
from typing import Any, Callable, Union
import flask
from . import types, errors


class SchemaProtect:
    def __init__(self, rule: Union[bool, types.Property, None]):
        self.rule = rule

    @property
    def request_body(self):
        if self.rule is True:
            if not flask.request.is_json:
                raise errors.SchemaValidationError()  # TODO expected json
            return flask.request.json
        elif self.rule is False:
            if flask.request.is_json:
                raise errors.SchemaValidationError()  # TODO unexpected json
            return None
        elif isinstance(self.rule, types.Property):
            return self.rule(flask.request.json)
        elif self.rule is None:
            return None
        raise errors.SchemaValidationError()  # TODO unknown rule type

    def __call__(self, func: Callable) -> Callable:
        @functools.wraps(func)
        def _call(*args: Any, **kwargs: Any) -> Any:
            return func(self.request_body, *args, **kwargs)

        return _call
