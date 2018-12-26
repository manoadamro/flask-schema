import re
import datetime
from typing import Any, Callable, Dict, List, Pattern, Tuple, Type, Union

from . import errors


class _Range:
    def __init__(
        self,
        minimum: Union[
            List, Tuple, str, int, float, datetime.datetime, datetime.date, None
        ],
        maximum: Union[
            List, Tuple, str, int, float, datetime.datetime, datetime.date, None
        ],
    ):
        self.min = minimum
        self.max = maximum

    def __call__(
        self,
        value: Union[
            List, Tuple, str, int, float, datetime.datetime, datetime.date, None
        ],
    ) -> bool:

        if value is None:
            return True
        if isinstance(value, (list, tuple, str)):
            value = len(value)

        minimum = self.min() if callable(self.min) else self.min
        maximum = self.max() if callable(self.max) else self.max

        if minimum is None and maximum is None:
            return True
        if minimum is None:
            return value <= maximum
        if maximum is None:
            return value >= minimum
        return minimum <= value <= maximum


class Schema:
    def __init__(self):
        self.object = Object(
            self.__class__,
            strict=self._is_strict,
            nullable=False,
            default=None,
            callback=None,
        )

    @property
    def _is_strict(self) -> bool:
        return getattr(self, "__strict__", False)

    def __call__(self, value: Dict) -> Dict:
        return self.object(value)


class Property:
    def __init__(
        self,
        *types: Type[Any],
        nullable: bool = True,
        default: Any = None,
        callback: Callable = None,
    ):
        self.types = types
        self.nullable = nullable
        self.default = default
        self.callback = callback

    def _get_value(self, value: Any) -> Any:
        if value is not None:
            return value
        if not self.nullable:
            raise errors.SchemaValidationError()  # TODO not nullable
        if callable(self.default):
            return self.default()
        return self.default

    def __call__(self, value: Any) -> Any:
        value = self._get_value(value)
        if value is not None and not isinstance(value, self.types):
            raise errors.SchemaValidationError()  # TODO wrong type
        if self.callback is not None:
            return self.callback(value)
        return value


class Object(Property):
    def __init__(self, schema: Type[Schema], strict: bool = False, **kwargs):
        super(Object, self).__init__(dict, **kwargs)
        self.strict = strict
        self.schema = self._load(schema)

    @classmethod
    def _load(cls, schema: Type[Schema]) -> Dict:
        return {f: getattr(schema, f) for f in dir(schema) if not f.startswith("_")}

    def _valid_fields(self, obj: Dict) -> bool:
        return all(key in self.schema for key in obj)

    def _valid_values(self, obj: Dict) -> Dict:
        return {key: func(obj.get(key, None)) for key, func in self.schema.items()}

    def __call__(self, value: Union[Dict, None]) -> Union[Dict, None]:
        value = super(Object, self).__call__(value)
        if value is None:
            return None
        if self.strict and not self._valid_fields(value):
            raise errors.SchemaValidationError()  # TODO invalid fields
        return self._valid_values(value)


class Array(Property):
    def __init__(
        self,
        schema: Type[Property],
        min_length: Union[int, float] = None,
        max_length: Union[int, float] = None,
        **kwargs,
    ):
        super(Array, self).__init__(list, **kwargs)
        self.schema = schema() if isinstance(schema, type) else schema
        self.range = _Range(min_length, max_length)

    def __call__(self, value: Union[List[Any], None]) -> Union[List[Any], None]:
        value = super(Array, self).__call__(value)
        if not self.range(value):
            raise errors.SchemaValidationError()  # TODO out of range
        if value is None:
            return None
        for i in range(len(value)):
            value[i] = self.schema(value[i])
        return value


class Number(Property):
    def __init__(
        self,
        types: Tuple = (int, float),
        min_value: Union[int, float] = None,
        max_value: Union[int, float] = None,
        **kwargs,
    ):
        super(Number, self).__init__(*types, **kwargs)
        self.range = _Range(min_value, max_value)

    def __call__(self, value: Union[int, float, None]) -> Union[int, float, None]:
        value = super(Number, self).__call__(value)
        if not self.range(value):
            raise errors.SchemaValidationError()  # TODO out of range
        return value


class Int(Number):
    def __init__(self, **kwargs):
        super(Int, self).__init__((int,), **kwargs)


class Float(Number):
    def __init__(self, **kwargs):
        super(Float, self).__init__((int, float), **kwargs)


class Bool(Property):
    def __init__(self, **kwargs):
        super(Bool, self).__init__(bool, **kwargs)

    def __call__(self, value: Union[bool, None]) -> bool:
        return super(Bool, self).__call__(value)


class String(Property):
    def __init__(
        self,
        min_length: Union[int, float] = None,
        max_length: Union[int, float] = None,
        **kwargs,
    ):
        super(String, self).__init__(str, **kwargs)
        self.range = _Range(min_length, max_length)

    def __call__(self, value: Union[str, None]) -> Union[str, None]:
        value = super(String, self).__call__(value)
        if not self.range(value):
            raise errors.SchemaValidationError()  # TODO out of range
        return value


class Regex(String):
    def __init__(self, matcher: Union[Pattern, str], **kwargs):
        super(Regex, self).__init__(**kwargs)
        self.matcher = re.compile(matcher) if isinstance(matcher, str) else matcher

    def _match(self, value: str):
        return re.match(self.matcher, value) is not None

    def __call__(self, value: Union[str, None]) -> Union[str, None]:
        value = super(Regex, self).__call__(value)
        if value is not None and not self._match(value):
            raise errors.SchemaValidationError()  # TODO no match
        return value


class Email(Regex):
    matcher = re.compile(".+@[^@]+.[^@]{2,}$")

    def __init__(self, **kwargs):
        super(Email, self).__init__(self.matcher, **kwargs)


class Uuid(Regex):
    matcher = re.compile(
        "^[a-fA-F0-9]{8}-?[a-fA-F0-9]{4}-?[a-fA-F0-9]{4}-?[a-fA-F0-9]{4}-?[a-fA-F0-9]{12}$"
    )

    def __init__(self, strip_hyphens=False, **kwargs):
        super(Uuid, self).__init__(self.matcher, **kwargs)
        self.strip_hyphens = strip_hyphens

    def __call__(self, value: Union[str, None]) -> Union[str, None]:
        value = super(Uuid, self).__call__(value)
        if value is not None and self.strip_hyphens:
            return value.replace("-", "")
        return value


class Date(Property):
    def __init__(
        self, min_value: datetime.date = None, max_value: datetime.date = None, **kwargs
    ):
        super(Date, self).__init__(datetime.date, **kwargs)
        self.range = _Range(min_value, max_value)

    @staticmethod
    def _get_date(
        value: Union[str, datetime.datetime, None]
    ) -> Union[datetime.date, None]:
        try:
            if value is None:
                return
            if isinstance(value, (float, int)):
                return datetime.date.fromtimestamp(value)
            if isinstance(value, str):
                return datetime.datetime.fromisoformat(value).date()
            if isinstance(value, datetime.datetime):
                return value.date()
            if isinstance(value, datetime.date):
                return value
            raise ValueError()  # TODO wrong type
        except ValueError as ex:
            raise errors.SchemaValidationError(str(ex))  # TODO

    def __call__(
        self, value: Union[str, datetime.date, None]
    ) -> Union[str, datetime.date, None]:
        value = self._get_date(value)
        value = super(Date, self).__call__(value)
        if not self.range(value):
            raise errors.SchemaValidationError()  # TODO out of range
        return value


class DateTime(Property):
    def __init__(
        self,
        min_value: datetime.datetime = None,
        max_value: datetime.datetime = None,
        **kwargs,
    ):
        super(DateTime, self).__init__(datetime.datetime, **kwargs)
        self.range = _Range(min_value, max_value)

    @staticmethod
    def _get_datetime(
        value: Union[str, datetime.datetime, None]
    ) -> Union[datetime.datetime, None]:
        try:
            if value is None:
                return
            if isinstance(value, (float, int)):
                return datetime.datetime.fromtimestamp(value)
            if isinstance(value, str):
                if value.endswith("Z"):
                    value = f"{value[:-1]}+00:00"
                return datetime.datetime.fromisoformat(value)
            if isinstance(value, datetime.datetime):
                return value
            raise ValueError()  # TODO wrong type
        except ValueError as ex:
            raise errors.SchemaValidationError(str(ex))  # TODO

    def __call__(
        self, value: Union[str, datetime.datetime, None]
    ) -> Union[str, datetime.datetime, None]:
        value = self._get_datetime(value)
        value = super(DateTime, self).__call__(value)
        if not self.range(value):
            raise errors.SchemaValidationError()  # TODO out of range
        return value
