from inspect import isdatadescriptor

from doubles.exceptions import UnallowedMethodCallError


class ProxyMethod(object):
    def __init__(self, target, method_name, find_expectation):
        self._target = target
        self._method_name = method_name
        self._find_expectation = find_expectation
        self._attr = target.attrs[method_name]

        self._capture_original_method()
        self._hijack_target()

    def __call__(self, *args, **kwargs):
        expectation = self._find_expectation(args, kwargs)

        if not expectation:
            self._raise_exception(args, kwargs)

        return expectation.return_value

    def __get__(self, instance, owner):
        if self._attr.kind == 'property':
            return self.__call__()

        return self

    def restore_original_method(self):
        if self._target.is_class():
            setattr(self._target.obj, self._method_name, self._original_method)
        elif isdatadescriptor(self._attr.object):
            setattr(self._target.obj.__class__, self._method_name, self._original_method)
        else:
            # TODO: Could there ever have been a value here that needs to be restored?
            del self._target.obj.__dict__[self._method_name]

    def _capture_original_method(self):
        self._original_method = self._attr.object

    def _hijack_target(self):
        if self._target.is_class():
            setattr(self._target.obj, self._method_name, self)
        elif isdatadescriptor(self._attr.object):
            setattr(self._target.obj.__class__, self._method_name, self)
        else:
            self._target.obj.__dict__[self._method_name] = self

    def _raise_exception(self, args, kwargs):
        raise UnallowedMethodCallError(
            "Received unexpected call to '{}' on {!r} with (args={}, kwargs={}).".format(
                self._method_name,
                self._target.obj,
                args,
                kwargs
            )
        )
