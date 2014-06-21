_any = object()


class MessageAllowance(object):
    def __init__(self, verify=False):
        self.return_value = None
        self.args = _any
        self.kwargs = _any

    def and_return(self, return_value):
        self.return_value = return_value

    def with_args(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def matches(self, args, kwargs):
        return self._property_matches('args', args) and self._property_matches('kwargs', kwargs)

    def _property_matches(self, name, arg):
        value = getattr(self, name)

        return value is _any or value == arg
