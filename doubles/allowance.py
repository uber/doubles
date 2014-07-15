from doubles.verification import verify_arguments

_any = object()


class Allowance(object):
    """An individual method allowance (stub)."""

    def __init__(self, target, method_name):
        self._target = target
        self._method_name = method_name
        self.args = _any
        self.kwargs = _any
        self._is_satisfied = True

        self.and_return(None)

    def and_raise(self, exception):
        """
        Causes the stub to raise the provided exception when called.

        :param Exception exception: The exception to raise.
        """
        def proxy_exception():
            raise exception

        self._return_value = proxy_exception
        return self

    def and_return(self, return_value):
        """
        Causes the stub to return the provided value.

        :param return_value: The value the stub will return when called.
        :type return_value: any object
        """

        self._return_value = lambda: return_value
        return self

    def and_return_result_of(self, return_value):
        """
        Causes the stub to return the result of calling the provided value.

        :param return_value: A callable that will be invoked to determine the stub's return value.
        :type return_value: any callable object
        """

        self._return_value = return_value
        return self

    def is_satisfied(self):
        return self._is_satisfied

    def with_args(self, *args, **kwargs):
        """
        Declares that the stub can only be called with the provided arguments.

        :param args: Any positional arguments required for invocation.
        :param kwargs: Any keyword arguments required for invocation.
        """

        self.args = args
        self.kwargs = kwargs
        self._verify_arguments()
        return self

    def with_no_args(self):
        """
        Declares that the stub can only be called with no arguments.
        """

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

    def _expected_argument_string(self):
        if self.args is _any and self.kwargs is _any:
            return 'any args'
        else:
            return '(args={!r}, kwargs={!r})'.format(self.args, self.kwargs)

    def _verify_arguments(self):
        verify_arguments(self._target, self._method_name, self.args, self.kwargs)
