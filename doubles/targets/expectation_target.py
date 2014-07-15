from inspect import stack

from doubles.lifecycle import current_space


def expect(target):
    """
    Prepares a target object for a method call expectation (mock). The name of the method to expect
    should be called as a method on the return value of this function::

        expect(foo).bar

    Accessing the ``bar`` attribute will return an ``Expectation`` which provides additional methods
    to configure the mock.

    :param target: The object that will be mocked.
    :type target: any object
    :return: An ``ExpectationTarget`` for the target object.
    """

    return ExpectationTarget(target)


class ExpectationTarget(object):
    def __init__(self, target):
        self._proxy = current_space().proxy_for(target)

    def __getattribute__(self, attr_name):
        __dict__ = object.__getattribute__(self, '__dict__')

        if __dict__ and attr_name in __dict__:
            return __dict__[attr_name]

        caller = stack()[1]
        return self._proxy.add_expectation(attr_name, caller)
