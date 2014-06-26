from inspect import isfunction, ismethod, getcallargs

from doubles.exceptions import VerifyingDoubleError


def _is_callable_without_instance(callable_obj, owner):
    if isfunction(callable_obj):
        return True

    if ismethod(callable_obj):
        if callable_obj.__self__ is owner:
            return True

    return False


def verify_method(target, method_name, class_level=False):
    if not hasattr(target, method_name):
        raise VerifyingDoubleError('no matching method')

    attr = getattr(target, method_name)

    if not callable(attr):
        raise VerifyingDoubleError('not callable')

    if class_level and not _is_callable_without_instance(attr, target):
        raise VerifyingDoubleError('not a class method')


def verify_arguments(method, args, kwargs):
    try:
        getcallargs(method, *args, **kwargs)
    except TypeError:
        raise VerifyingDoubleError('bad arguments')
