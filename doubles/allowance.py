from doubles.exceptions import MockExpectationError
from doubles.verification import verify_arguments

_any = object()


class Allowance(object):
    def __init__(self, target, method_name):
        self._target = target
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

    def raise_failure_exception(self):
        raise MockExpectationError(
            "Expected '{}' to be called on {!r} with {}, but was not.".format(
                self._method_name,
                self._target.obj,
                self._expected_argument_string()
            )
        )

    def satisfy_any_args_match(self):
        return self.args is _any and self.kwargs is _any

    def satisfy_exact_match(self, args, kwargs):
        return self.args == args and self.kwargs == kwargs

    @property
    def return_value(self):
        return self._return_value()

    def _expected_argument_string(self):
        if self.args is _any and self.kwargs is _any:
            return 'any args'
        else:
            return '(args={!r}, kwargs={!r})'.format(self.args, self.kwargs)

    def _verify_arguments(self):
        verify_arguments(self._target, self._method_name, self.args, self.kwargs)
