from inspect import getcallargs

from doubles.exceptions import VerifyingDoubleError


def verify_method(target, method_name):
    if not hasattr(target, method_name):
        raise VerifyingDoubleError

    attr = getattr(target, method_name)

    if not callable(attr):
        raise VerifyingDoubleError


def verify_arguments(method, args, kwargs):
    try:
        getcallargs(method, *args, **kwargs)
    except TypeError:
        raise VerifyingDoubleError
