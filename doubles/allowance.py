from functools import wraps
from inspect import getargspec

from doubles.exceptions import MockExpectationError, VerifyingBuiltinDoubleArgumentError
from doubles.verification import verify_arguments
from doubles.call_count_accumulator import CallCountAccumulator
import doubles.lifecycle

_any = object()


def _get_future():
    try:
        from concurrent.futures import Future
    except ImportError:
        try:
            from tornado.concurrent import Future
        except ImportError:
            raise ImportError(
                'Error Importing Future, Could not find concurrent.futures or tornado.concurrent',
            )
    return Future()


def verify_count_is_non_negative(func):
    @wraps(func)
    def inner(self, arg):
        if arg < 0:
            raise TypeError(func.__name__ + ' requires one positive integer argument')
        return func(self, arg)
    return inner


def check_func_takes_args(func):
    arg_spec = getargspec(func)
    return arg_spec.args or arg_spec.varargs or arg_spec.keywords or arg_spec.defaults


def build_argument_repr_string(args, kwargs):
    args = [repr(x) for x in args]
    kwargs = ['{}={!r}'.format(k, v) for k, v in kwargs.items()]
    return '({})'.format(', '.join(args + kwargs))


class Allowance(object):
    """An individual method allowance (stub)."""

    def __init__(self, target, method_name, caller):
        """
        :param Target target: The object owning the method to stub.
        :param str method_name: The name of the method to stub.
        """

        self._target = target
        self._method_name = method_name
        self._caller = caller
        self.args = _any
        self.kwargs = _any
        self._custom_matcher = None
        self._is_satisfied = True
        self._call_counter = CallCountAccumulator()

        self._return_value = lambda *args, **kwargs: None

    def and_raise(self, exception):
        """Causes the double to raise the provided exception when called.

        :param Exception exception: The exception to raise.
        """
        def proxy_exception(*args, **kwargs):
            raise exception

        self._return_value = proxy_exception
        return self

    def and_raise_future(self, exception):
        """Similar to `and_raise` but the doubled method returns a future.

        :param Exception exception: The exception to raise.
        """
        future = _get_future()
        future.set_exception(exception)
        return self.and_return(future)

    def and_return_future(self, *return_values):
        """Similar to `and_return` but the doubled method returns a future.

        :param object return_values: The values the double will return when called,
        """
        futures = []
        for value in return_values:
            future = _get_future()
            future.set_result(value)
            futures.append(future)
        return self.and_return(*futures)

    def and_return(self, *return_values):
        """Set a return value for an allowance

        Causes the double to return the provided values in order.  If multiple
        values are provided, they are returned one at a time in sequence as the double is called.
        If the double is called more times than there are return values, it should continue to
        return the last value in the list.


        :param object return_values: The values the double will return when called,
        """

        if not return_values:
            raise TypeError('and_return() expected at least 1 return value')

        return_values = list(return_values)
        final_value = return_values.pop()

        self.and_return_result_of(
            lambda: return_values.pop(0) if return_values else final_value
        )
        return self

    def and_return_result_of(self, return_value):
        """ Causes the double to return the result of calling the provided value.

        :param return_value: A callable that will be invoked to determine the double's return value.
        :type return_value: any callable object
        """
        if not check_func_takes_args(return_value):
            self._return_value = lambda *args, **kwargs: return_value()
        else:
            self._return_value = return_value

        return self

    def is_satisfied(self):
        """Returns a boolean indicating whether or not the double has been satisfied.

        Stubs are always satisfied, but mocks are only satisifed if they've been
        called as was declared.

        :return: Whether or not the double is satisfied.
        :rtype: bool
        """
        return self._is_satisfied

    def with_args(self, *args, **kwargs):
        """Declares that the double can only be called with the provided arguments.

        :param args: Any positional arguments required for invocation.
        :param kwargs: Any keyword arguments required for invocation.
        """

        self.args = args
        self.kwargs = kwargs
        self.verify_arguments()
        return self

    def with_args_validator(self, matching_function):
        """Define a custom function for testing arguments

        :param func matching_function:  The function used to test arguments passed to the stub.
        """
        self.args = None
        self.kwargs = None
        self._custom_matcher = matching_function
        return self

    def __call__(self, *args, **kwargs):
        """A short hand syntax for with_args

        Allows callers to do:
            allow(module).foo.with_args(1, 2)
        With:
            allow(module).foo(1, 2)

        :param args: Any positional arguments required for invocation.
        :param kwargs: Any keyword arguments required for invocation.
        """
        return self.with_args(*args, **kwargs)

    def with_no_args(self):
        """Declares that the double can only be called with no arguments."""

        self.args = ()
        self.kwargs = {}
        self.verify_arguments()
        return self

    def satisfy_any_args_match(self):
        """Returns a boolean indicating whether or not the stub will accept arbitrary arguments.

        This will be true unless the user has specified otherwise using ``with_args`` or
        ``with_no_args``.

        :return: Whether or not the stub accepts arbitrary arguments.
        :rtype: bool
        """

        return self.args is _any and self.kwargs is _any

    def satisfy_exact_match(self, args, kwargs):
        """Returns a boolean indicating whether or not the stub will accept the provided arguments.

        :return: Whether or not the stub accepts the provided arguments.
        :rtype: bool
        """

        if self.args is None and self.kwargs is None:
            return False
        elif self.args is _any and self.kwargs is _any:
            return True
        elif args == self.args and kwargs == self.kwargs:
            return True
        elif len(args) != len(self.args) or len(kwargs) != len(self.kwargs):
            return False

        if not all(x == y or y == x for x, y in zip(args, self.args)):
            return False

        for key, value in self.kwargs.items():
            if key not in kwargs:
                return False
            elif not (kwargs[key] == value or value == kwargs[key]):
                return False

        return True

    def satisfy_custom_matcher(self, args, kwargs):
        """Return a boolean indicating if the args satisify the stub

        :return: Whether or not the stub accepts the provided arguments.
        :rtype: bool
        """
        if not self._custom_matcher:
            return False
        try:
            return self._custom_matcher(*args, **kwargs)
        except Exception:
            return False

    def return_value(self, *args, **kwargs):
        """Extracts the real value to be returned from the wrapping callable.

        :return: The value the double should return when called.
        """

        self._called()
        return self._return_value(*args, **kwargs)

    def verify_arguments(self, args=None, kwargs=None):
        """Ensures that the arguments specified match the signature of the real method.

        :raise: ``VerifyingDoubleError`` if the arguments do not match.
        """

        args = self.args if args is None else args
        kwargs = self.kwargs if kwargs is None else kwargs

        try:
            verify_arguments(self._target, self._method_name, args, kwargs)
        except VerifyingBuiltinDoubleArgumentError:
            if doubles.lifecycle.ignore_builtin_verification():
                raise

    @verify_count_is_non_negative
    def exactly(self, n):
        """Set an exact call count allowance

        :param integer n:
        """

        self._call_counter.set_exact(n)
        return self

    @verify_count_is_non_negative
    def at_least(self, n):
        """Set a minimum call count allowance

        :param integer n:
        """

        self._call_counter.set_minimum(n)
        return self

    @verify_count_is_non_negative
    def at_most(self, n):
        """Set a maximum call count allowance

        :param integer n:
        """

        self._call_counter.set_maximum(n)
        return self

    def never(self):
        """Set an expected call count allowance of 0"""

        self.exactly(0)
        return self

    def once(self):
        """Set an expected call count allowance of 1"""

        self.exactly(1)
        return self

    def twice(self):
        """Set an expected call count allowance of 2"""

        self.exactly(2)
        return self

    @property
    def times(self):
        return self
    time = times

    def _called(self):
        """Indicate that the allowance was called

        :raise MockExpectationError if the allowance has been called too many times
        """

        if self._call_counter.called().has_too_many_calls():
            self.raise_failure_exception()

    def raise_failure_exception(self, expect_or_allow='Allowed'):
        """Raises a ``MockExpectationError`` with a useful message.

        :raise: ``MockExpectationError``
        """

        raise MockExpectationError(
            "{} '{}' to be called {}on {!r} with {}, but was not. ({}:{})".format(
                expect_or_allow,
                self._method_name,
                self._call_counter.error_string(),
                self._target.obj,
                self._expected_argument_string(),
                self._caller.filename,
                self._caller.lineno,
            )
        )

    def _expected_argument_string(self):
        """Generates a string describing what arguments the double expected.

        :return: A string describing expected arguments.
        :rtype: str
        """

        if self.args is _any and self.kwargs is _any:
            return 'any args'
        else:
            return build_argument_repr_string(self.args, self.kwargs)
