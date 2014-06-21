_any = object()


class MessageAllowance(object):
    def __init__(self, verify=False):
        self._return_value = None
        self.args = _any
        self.kwargs = _any
        self._is_callable_return = False

    def allows_any_args(self):
        return self.args is _any and self.kwargs is _any

    def and_return(self, return_value):
        self._return_value = return_value
        self._is_callable_return = False

    def and_return_result_of(self, return_value):
        self._return_value = return_value
        self._is_callable_return = True

    def with_args(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        return self

    def matches_exactly(self, args, kwargs):
        return self._property_matches('args', args) and self._property_matches('kwargs', kwargs)

    @property
    def return_value(self):
        if self._is_callable_return:
            return self._return_value()
        else:
            return self._return_value

    def _property_matches(self, name, value):
        return getattr(self, name) == value
