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

    def verify(self):
        for expectation in self._expectations:
            if not expectation.is_satisfied():
                raise MockExpectationError

    def _define_proxy_method(self):
        def proxy_method(*args, **kwargs):
            expectation = self._find_matching_expectation(args, kwargs)

            if not expectation:
                raise UnallowedMethodCallError

            return expectation.return_value

        setattr(self._obj, self._method_name, proxy_method)

    def _find_matching_expectation(self, args, kwargs):
        for expectation in self._expectations:
            if expectation.satisfy_exact_match(args, kwargs):
                return expectation

        for expectation in self._expectations:
            if expectation.satisfy_any_args_match():
                return expectation
