from doubles.exceptions import MockExpectationError, UnallowedMethodCallError
from doubles.message_allowance import MessageAllowance
from doubles.message_expectation import MessageExpectation


class MethodDouble(object):
    def __init__(self, method_name, obj):
        self._method_name = method_name
        self._obj = obj

        self._allowances = []
        self._expectations = []

    def add_allowance(self):
        self._define_proxy_method()
        allowance = MessageAllowance()
        self._allowances.append(allowance)
        return allowance

    def add_expectation(self):
        self._expectations.append(MessageExpectation())

    def verify(self):
        for expectation in self._expectations:
            if not expectation.is_satisfied():
                raise MockExpectationError

    def _define_proxy_method(self):
        def proxy_method(*args, **kwargs):
            allowance = self._find_matching_allowance(args, kwargs)

            if not allowance:
                raise UnallowedMethodCallError

            return allowance.return_value

        setattr(self._obj, self._method_name, proxy_method)

    def _find_matching_allowance(self, args, kwargs):
        for allowance in self._allowances:
            if allowance.matches_exactly(args, kwargs):
                return allowance

        for allowance in self._allowances:
            if allowance.allows_any_args():
                return allowance
