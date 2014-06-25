from doubles.exceptions import VerifyingDoubleError

_SELF_LENGTH = 1


def verify_method(target, method_name):
    if not hasattr(target, method_name):
        raise VerifyingDoubleError

    attr = getattr(target, method_name)

    if not callable(attr):
        raise VerifyingDoubleError


def verify_arguments(argspec, args, kwargs):
    arg_count = len(args) + _SELF_LENGTH

    max_allowed = len(argspec.args)

    if argspec.defaults is None:
        min_allowed = max_allowed
    else:
        min_allowed = max_allowed - len(argspec.defaults)

    if not argspec.varargs and (arg_count > max_allowed or arg_count < min_allowed):
        raise VerifyingDoubleError

    if argspec.keywords is None:
        for key in kwargs.keys():
            if key not in argspec.args:
                raise VerifyingDoubleError
