from doubles.exceptions import MockExpectationError, UnallowedMethodCallError
from doubles.message_expectation import MessageAllowance
from doubles.message_expectation import MessageExpectation


class MethodDouble(object):
    def __init__(self, method_name, obj):
        self._method_name = method_name
        self._obj = obj

        self._expectations = []

        self._define_proxy_method()

    def add_allowance(self):
        allowance = MessageAllowance()
        self._expectations.append(allowance)
        return allowance

    def add_expectation(self):
        expectation = MessageExpectation()
        self._expectations.append(expectation)
        return expectation

    def restore_original_method(self):
        try:
            setattr(self._obj, self._method_name, self._original_method)
        except AttributeError:
            pass

    def verify(self):
        for expectation in self._expectations:
            if not expectation.is_satisfied():
                raise MockExpectationError

    def _define_proxy_method(self):
        _self = self

        def proxy_method(self, *args, **kwargs):
            expectation = _self._find_matching_expectation(args, kwargs)

            if not expectation:
                raise UnallowedMethodCallError

            return expectation.return_value

        try:
            self._original_method = getattr(self._obj, self._method_name)
        except AttributeError:
            pass

        bound_proxy_method = proxy_method.__get__(self._obj)
        setattr(self._obj, self._method_name, bound_proxy_method)

    def _find_matching_expectation(self, args, kwargs):
        for expectation in self._expectations:
            if expectation.satisfy_exact_match(args, kwargs):
                return expectation

        for expectation in self._expectations:
            if expectation.satisfy_any_args_match():
                return expectation
