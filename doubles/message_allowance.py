_any = object()


class MessageAllowance(object):
    def __init__(self):
        self._return_value = None
        self.args = _any
        self.kwargs = _any
        self._is_callable_return = False
        self._is_satisfied = True

    def and_return(self, return_value):
        self._return_value = return_value
        self._is_callable_return = False
        return self

    def and_return_result_of(self, return_value):
        self._return_value = return_value
        self._is_callable_return = True
        return self

    def is_satisfied(self):
        return self._is_satisfied

    def with_args(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        return self

    def with_no_args(self):
        self.args = ()
        self.kwargs = {}
        return self

    def satisfy_any_args_match(self):
        return self.args is _any and self.kwargs is _any

    def satisfy_exact_match(self, args, kwargs):
        return self.args == args and self.kwargs == kwargs

    @property
    def return_value(self):
        if self._is_callable_return:
            return self._return_value()
        else:
            return self._return_value
