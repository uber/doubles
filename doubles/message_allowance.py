_any = object()


class MessageAllowance(object):
    def __init__(self, verify=False):
        self.return_value = None
        self.args = _any
        self.kwargs = _any

    def allows_any_args(self):
        return self.args is _any and self.kwargs is _any

    def and_return(self, return_value):
        self.return_value = return_value

    def with_args(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        return self

    def matches_exactly(self, args, kwargs):
        return self._property_matches('args', args) and self._property_matches('kwargs', kwargs)

    def _property_matches(self, name, value):
        return getattr(self, name) == value
