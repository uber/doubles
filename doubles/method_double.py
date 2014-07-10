from doubles.allowance import Allowance
from doubles.class_double import ClassDouble
from doubles.expectation import Expectation
from doubles.instance_double import InstanceDouble
from doubles.proxy_method import ProxyMethod
from doubles.verification import verify_method


class MethodDouble(object):
    def __init__(self, method_name, target):
        self._method_name = method_name
        self._target = target

        self._verify_method()

        self._expectations = []

        self._proxy_method = ProxyMethod(
            target,
            method_name,
            lambda args, kwargs: self._find_matching_expectation(args, kwargs)
        )

    def add_allowance(self):
        allowance = Allowance(self._target, self._method_name)
        self._expectations.append(allowance)
        return allowance

    def add_expectation(self, caller):
        expectation = Expectation(self._target, self._method_name, caller)
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

    def _verify_method(self):
        # TODO: Find a way to set class_level without manual type checking.
        if isinstance(self._target.obj, ClassDouble):
            class_level = True
        elif isinstance(self._target.obj, InstanceDouble):
            class_level = False
        else:
            class_level = self._target.is_class()

        verify_method(self._target, self._method_name, class_level=class_level)
