from inspect import isbuiltin, getcallargs

from doubles.exceptions import VerifyingDoubleError


def verify_method(target, method_name, class_level=False):
    attr = target.attrs.get(method_name)

    if not attr:
        raise VerifyingDoubleError('no matching method')

    if attr.kind == 'data' and not isbuiltin(attr.object):
        raise VerifyingDoubleError('not callable')

    if class_level and attr.kind == 'method':
        raise VerifyingDoubleError('not a class method')


def verify_arguments(target, method_name, args, kwargs):
    attr = target.attrs[method_name]
    method = attr.object

    if attr.kind != 'static method':
        args = ['self_or_cls'] + list(args)

    try:
        getcallargs(method, *args, **kwargs)
    except TypeError as e:
        raise VerifyingDoubleError(e.message)
