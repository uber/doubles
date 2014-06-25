from doubles.exceptions import VerifyingDoubleError


def verify_method(target, method_name):
    if not hasattr(target, method_name):
        raise VerifyingDoubleError

    attr = getattr(target, method_name)

    if not callable(attr):
        raise VerifyingDoubleError


def verify_arguments(argspec, args, kwargs):
    if not argspec.varargs and len(argspec.args) != args:
        raise VerifyingDoubleError
