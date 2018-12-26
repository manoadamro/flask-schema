

class SchemaProtect:

    def __init__(self, *rules, **kwrules):
        self.rules = rules

    def __call__(self, func):
        def _call(*args, **kwargs):
            pass
        return _call
