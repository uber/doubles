from doubles.method_double import MethodDouble
from doubles.target import Target


class Proxy(object):
    """
    An intermediate object used to maintain a mapping between target objects and method doubles.
    """

    def __init__(self, obj):
        """
        :param object obj: The object that will be doubled.
        """

        self._target = Target(obj)
        self._method_doubles = {}

    def add_allowance(self, method_name, caller):
        """Adds a new allowance for the given method name.

        :param str method_name: The name of the method to allow.
        :param tuple caller: A tuple indicating where the allowance was added
        :return: The new ``Allowance``.
        :rtype: Allowance
        """

        return self.method_double_for(method_name).add_allowance(caller)

    def add_expectation(self, method_name, caller):
        """Adds a new expectation for the given method name.

        :param str method_name: The name of the method to expect.
        :return: The new ``Expectation``.
        :rtype: Expectation
        """

        return self.method_double_for(method_name).add_expectation(caller)

    def restore_original_object(self):
        """Remove all stubs from an object.

        Removes the proxy methods applied to each method double and replaces them with the original
        values.
        """

        for method_double in self._method_doubles.values():
            method_double.restore_original_method()

    def verify(self):
        """Verifies all expectations on all method doubles.

        :raise: ``MockExpectationError`` on the first expectation that is not satisfied, if any.
        """

        for method_double in self._method_doubles.values():
            method_double.verify()

    def method_double_for(self, method_name):
        """Returns the method double for the provided method name, creating one if necessary.

        :param str method_name: The name of the method to retrieve a method double for.
        :return: The mapped ``MethodDouble``.
        :rtype: MethodDouble
        """

        if method_name not in self._method_doubles:
            self._method_doubles[method_name] = MethodDouble(method_name, self._target)

        return self._method_doubles[method_name]
