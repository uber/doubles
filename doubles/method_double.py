from inspect import isclass

from doubles.allowance import Allowance
from doubles.expectation import Expectation
from doubles.proxy_method import ProxyMethod
from doubles.verification import verify_method


class MethodDouble(object):
    def __init__(self, method_name, obj):
        self._method_name = method_name
        self._obj = obj

        self._verify_method_name()

        self._expectations = []

        self._proxy_method = ProxyMethod(
            obj,
            method_name,
            lambda args, kwargs: self._find_matching_expectation(args, kwargs)
        )

    def add_allowance(self):
        allowance = Allowance(self._obj, self._method_name)
        self._expectations.append(allowance)
        return allowance

    def add_expectation(self):
        expectation = Expectation(self._obj, self._method_name)
        self._expectations.append(expectation)
        return expectation

    def restore_original_method(self):
        self._proxy_method.restore_original_method()

    def verify(self):
        for expectation in self._expectations:
            if not expectation.is_satisfied():
                expectation.raise_failure_exception()

    def _find_matching_expectation(self, args, kwargs):
        for expectation in self._expectations:
            if expectation.satisfy_exact_match(args, kwargs):
                return expectation

        for expectation in self._expectations:
            if expectation.satisfy_any_args_match():
                return expectation

    def _verify_method_name(self):
        if hasattr(self._obj, '_doubles_verify_method_name'):
            self._obj._doubles_verify_method_name(self._method_name)
        elif isclass(self._obj):
            verify_method(self._obj, self._method_name, class_level=True)
        else:
            verify_method(self._obj, self._method_name)
