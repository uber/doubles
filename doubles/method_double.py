from doubles.allowance import Allowance
from doubles.class_double import ClassDouble
from doubles.expectation import Expectation
from doubles.instance_double import InstanceDouble
from doubles.proxy_method import ProxyMethod
from doubles.verification import verify_method


class MethodDouble(object):
    """A double of an individual method."""

    def __init__(self, method_name, target):
        """
        :param str method_name: The name of the method to double.
        :param Target target: A ``Target`` object containing the object with the method to double.
        """

        self._method_name = method_name
        self._target = target

        self._verify_method()

        self._expectations = []

        self._proxy_method = ProxyMethod(
            target,
            method_name,
            lambda args, kwargs: self._find_matching_expectation(args, kwargs)
        )

    def add_allowance(self, caller):
        """
        Adds a new allowance for the method.

        :param: tuple caller: A tuple indicating where the method was called
        :return: The new ``Allowance``.
        :rtype: Allowance
        """

        allowance = Allowance(self._target, self._method_name, caller)
        self._expectations.append(allowance)
        return allowance

    def add_expectation(self, caller):
        """
        Adds a new expectation for the method.

        :return: The new ``Expectation``.
        :rtype: Expectation
        """

        expectation = Expectation(self._target, self._method_name, caller)
        self._expectations.append(expectation)
        return expectation

    def restore_original_method(self):
        """Removes the proxy method on the target and replaces it with its original value."""

        self._proxy_method.restore_original_method()

    def verify(self):
        """
        Verifies all expectations on the method.

        :raise: ``MockExpectationError`` on the first expectation that is not satisfied, if any.
        """

        for expectation in self._expectations:
            if not expectation.is_satisfied():
                expectation.raise_failure_exception()

    def _find_matching_expectation(self, args, kwargs):
        """
        Returns the first expectation that matches the ones declared. Tries one with specific
        arguments first, then falls back to an expectation that allows arbitrary arguments.

        :return: The matching ``Allowance`` or ``Expectation``, if one was found.
        :rtype: Allowance, Expectation, None
        """

        for expectation in self._expectations:
            if expectation.satisfy_exact_match(args, kwargs):
                return expectation

        for expectation in self._expectations:
            if expectation.satisfy_any_args_match():
                return expectation

    def _verify_method(self):
        """
        Verifies that the target object has a method matching the name the user is attempting to
        double.

        :raise: ``VerifyingDoubleError`` if no matching method is found.
        """

        # TODO: Find a way to set class_level without manual type checking.
        if isinstance(self._target.obj, ClassDouble):
            class_level = True
        elif isinstance(self._target.obj, InstanceDouble):
            class_level = False
        else:
            class_level = self._target.is_class()

        verify_method(self._target, self._method_name, class_level=class_level)
