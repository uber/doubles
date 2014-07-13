from inspect import stack

from doubles.lifecycle import current_space


def allow(target):
    """
    Prepares a target object for a method call allowance (stub). The name of the method to allow
    should be called as a method on the return value of this function::

        allow(foo).bar

    Accessing the ``bar`` attribute will return an ``Allowance`` which provides additional methods
    to configure the stub.

    :param object target: The object that will be stubbed.
    :return: An ``AllowanceTarget`` for the target object.
    """

    return AllowanceTarget(target)


class AllowanceTarget(object):
    """A wrapper around a target object that creates new allowances on attribute access."""

    def __init__(self, target):
        """
        :param object target: The object to wrap.
        """

        self._proxy = current_space().proxy_for(target)

    def __getattribute__(self, attr_name):
        """
        Returns the value of existing attributes, and returns a new allowance for any attribute
        that doesn't yet exist.

        :param str attr_name: The name of the attribute to look up.
        :return: The existing value or a new ``Allowance``.
        :rtype: object, Allowance
        """

        __dict__ = object.__getattribute__(self, '__dict__')

        if __dict__ and attr_name in __dict__:
            return __dict__[attr_name]

        caller = stack()[1]
        return self._proxy.add_allowance(attr_name, caller)
