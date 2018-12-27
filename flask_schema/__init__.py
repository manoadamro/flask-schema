from . import types, errors, decorators

schema_protect = decorators.SchemaProtect
custom_property = decorators.CustomProperty

# types
schema = types

# errors
SchemaValidationError = errors.SchemaValidationError
