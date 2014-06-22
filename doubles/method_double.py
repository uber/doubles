from doubles.exceptions import MockExpectationError, UnallowedMethodCallError
from doubles.message_allowance import MessageAllowance
from doubles.message_expectation import MessageExpectation


class MethodDouble(object):
    def __init__(self, method_name, obj):
        self._method_name = method_name
        self._obj = obj

        self._allowances = []

        self._define_proxy_method()

    def add_allowance(self):
        allowance = MessageAllowance()
        self._allowances.append(allowance)
        return allowance

    def add_expectation(self):
        expectation = MessageExpectation()
        self._allowances.append(expectation)
        return expectation

    def verify(self):
        for allowance in self._allowances:
            if not allowance.is_satisfied():
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
                allowance.record_call()
                return allowance

        for allowance in self._allowances:
            if allowance.allows_any_args():
                allowance.record_call()
                return allowance
