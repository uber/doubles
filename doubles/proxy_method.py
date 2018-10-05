import sys
from functools import wraps
from inspect import isbuiltin

from doubles.allowance import build_argument_repr_string
from doubles.exceptions import UnallowedMethodCallError
from doubles.proxy_property import ProxyProperty


def double_name(name):
    return 'double_of_' + name


def _restore__new__(target, original_method):
    """Restore __new__ to original_method on the target

    Python 3 does some magic to verify no arguments are sent to __new__ if it
    is the builtin version, to work in python 3 we must handle this:

        1) If original_method is the builtin version of __new__, wrap the
        builtin __new__ to ensure that no arguments are passed in.

        2) If original_method is a custom method treat it the same as we would
        in python2

    :param class target: The class to restore __new__ on
    :param func original_method: The method to set __new__ to
    """
    if isbuiltin(original_method):
        @wraps(original_method)
        def _new(cls, *args, **kwargs):
            return original_method(cls)

        target.__new__ = _new
    else:
        target.__new__ = original_method


class ProxyMethod(object):
    """
    The object that replaces the real value of a doubled method. Responsible for hijacking the
    target object, finding matching expectations and returning their values when called, and
    restoring the original value to the hijacked object during teardown.
    """

    def __init__(self, target, method_name, find_expectation):
        """
        :param Target target: The object to be hijacked.
        :param str method_name: The name of the method to replace.
        :param function find_expectation: A function to call to look for expectations that match
             any provided arguments.
        """

        self._target = target
        self._method_name = method_name
        self._find_expectation = find_expectation
        self._attr = target.get_attr(method_name)

        self._capture_original_method()
        self._hijack_target()

    def __call__(self, *args, **kwargs):
        """The actual invocation of the doubled method.

        :param tuple args: The arguments the doubled method was called with.
        :param dict kwargs: The keyword arguments the doubled method was called with.
        :return: The return value the doubled method was declared to return.
        :rtype: object
        :raise: ``UnallowedMethodCallError`` if no matching doubles were found.
        """

        expectation = self._find_expectation(args, kwargs)

        if not expectation:
            self._raise_exception(args, kwargs)

        expectation.verify_arguments(args, kwargs)

        return expectation.return_value(*args, **kwargs)

    def __get__(self, instance, owner):
        """Implements the descriptor protocol to allow doubled properties to behave as properties.

        :return: The return value of any matching double in the case of a property, self otherwise.
        :rtype: object, ProxyMethod
        """

        if self._attr.kind == 'property':
            return self.__call__()

        return self

    @property
    def __name__(self):
        return self._original_method.__name__

    @property
    def __doc__(self):
        return self._original_method.__doc__

    @property
    def __wrapped__(self):
        return self._original_method

    def restore_original_method(self):
        """Replaces the proxy method on the target object with its original value."""

        if self._target.is_class_or_module():
            setattr(self._target.obj, self._method_name, self._original_method)
            if self._method_name == '__new__' and sys.version_info >= (3, 0):
                _restore__new__(self._target.obj, self._original_method)
            else:
                setattr(self._target.obj, self._method_name, self._original_method)
        elif self._attr.kind == 'property':
            setattr(self._target.obj.__class__, self._method_name, self._original_method)
            del self._target.obj.__dict__[double_name(self._method_name)]
        elif self._attr.kind == 'attribute':
            self._target.obj.__dict__[self._method_name] = self._original_method
        else:
            # TODO: Could there ever have been a value here that needs to be restored?
            del self._target.obj.__dict__[self._method_name]

        if self._method_name in ['__call__', '__enter__', '__exit__']:
            self._target.restore_attr(self._method_name)

    def _capture_original_method(self):
        """Saves a reference to the original value of the method to be doubled."""

        self._original_method = self._attr.object

    def _hijack_target(self):
        """Replaces the target method on the target object with the proxy method."""

        if self._target.is_class_or_module():
            setattr(self._target.obj, self._method_name, self)
        elif self._attr.kind == 'property':
            proxy_property = ProxyProperty(
                double_name(self._method_name),
                self._original_method,
            )
            setattr(self._target.obj.__class__, self._method_name, proxy_property)
            self._target.obj.__dict__[double_name(self._method_name)] = self
        else:
            self._target.obj.__dict__[self._method_name] = self

        if self._method_name in ['__call__', '__enter__', '__exit__']:
            self._target.hijack_attr(self._method_name)

    def _raise_exception(self, args, kwargs):
        """ Raises an ``UnallowedMethodCallError`` with a useful message.

        :raise: ``UnallowedMethodCallError``
        """

        error_message = (
            "Received unexpected call to '{}' on {!r}.  The supplied arguments "
            "{} do not match any available allowances."
        )

        raise UnallowedMethodCallError(
            error_message.format(
                self._method_name,
                self._target.obj,
                build_argument_repr_string(args, kwargs)
            )
        )
