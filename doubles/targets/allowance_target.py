import inspect

from doubles.class_double import ClassDouble
from doubles.exceptions import ConstructorDoubleError
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


def allow_constructor(target):
    """
    Set an allowance on a ``ClassDouble`` constructor

    This allows the caller to control what a ClassDouble returns when a new instance is created.

    :param ClassDouble target:  The ClassDouble to set the allowance on.
    :return: an ``Allowance`` for the __new__ method.
    :raise: ``ConstructorDoubleError`` if target is not a ClassDouble.
    """
    if not isinstance(target, ClassDouble):
        raise ConstructorDoubleError(
            'Cannot allow_constructor of {} since it is not a ClassDouble.'.format(target),
        )

    return allow(target)._doubles__new__


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

        caller = inspect.getframeinfo(inspect.currentframe().f_back)
        return self._proxy.add_allowance(attr_name, caller)
