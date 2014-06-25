from doubles.verifying_doubles.verifying_double import VerifyingDouble

_any = object()


class MessageAllowance(object):
    def __init__(self, obj, method_name):
        self._obj = obj
        self._method_name = method_name
        self.args = _any
        self.kwargs = _any
        self._is_satisfied = True

        self.and_return(None)

    def and_raise(self, exception):
        def proxy_exception():
            raise exception

        self._return_value = proxy_exception
        return self

    def and_return(self, return_value):
        self._return_value = lambda: return_value
        return self

    def and_return_result_of(self, return_value):
        self._return_value = return_value
        return self

    def is_satisfied(self):
        return self._is_satisfied

    def with_args(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self._verify_arguments()
        return self

    def with_no_args(self):
        self.args = ()
        self.kwargs = {}
        self._verify_arguments()
        return self

    def satisfy_any_args_match(self):
        return self.args is _any and self.kwargs is _any

    def satisfy_exact_match(self, args, kwargs):
        return self.args == args and self.kwargs == kwargs

    @property
    def return_value(self):
        return self._return_value()

    def _verify_arguments(self):
        if not isinstance(self._obj, VerifyingDouble):
            return

        self._obj._doubles_verify_arguments(self._method_name, self.args, self.kwargs)
