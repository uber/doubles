from doubles.lifecycle import current_space


def allow(target):
    """
    Prepares a target object for a method call allowance (stub). The name of the method to allow
    should be called as a method on the return value of this function::

        allow(foo).bar

    Accessing the ``bar`` attribute will return an ``Allowance`` which provides additional methods
    to configure the stub.

    :param target: The object that will be stubbed.
    :type target: any object
    :return: An ``AllowanceTarget`` for the target object.
    """

    return AllowanceTarget(target)


class AllowanceTarget(object):
    def __init__(self, target):
        self._proxy = current_space().proxy_for(target)

    def __getattribute__(self, attr_name):
        __dict__ = object.__getattribute__(self, '__dict__')

        if __dict__ and attr_name in __dict__:
            return __dict__[attr_name]

        return self._proxy.add_allowance(attr_name)
