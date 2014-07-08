from inspect import ismethod, getcallargs

from doubles.exceptions import VerifyingDoubleError


def _is_instance_method(callable_obj, owner):
    return ismethod(callable_obj) and callable_obj.__self__ is not owner


def verify_method(target, method_name, class_level=False):
    if not hasattr(target, method_name):
        raise VerifyingDoubleError('no matching method')

    attr = getattr(target, method_name)

    if not callable(attr):
        raise VerifyingDoubleError('not callable')

    if class_level and _is_instance_method(attr, target):
        raise VerifyingDoubleError('not a class method')


def verify_arguments(method, args, kwargs):
    try:
        getcallargs(method, *args, **kwargs)
    except TypeError as e:
        raise VerifyingDoubleError(e.message)
