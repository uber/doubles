from doubles.exceptions import UnallowedMethodCallError


class ProxyMethod(object):
    def __init__(self, obj, method_name, find_expectation):
        self._obj = obj
        self._method_name = method_name
        self._find_expectation = find_expectation

        self._capture_original_method()

    def __call__(self, *args, **kwargs):
        expectation = self._find_expectation(args, kwargs)

        if not expectation:
            self._raise_exception(args, kwargs)

        return expectation.return_value

    def restore_original_method(self):
        try:
            setattr(self._obj, self._method_name, self._original_method)
        except AttributeError:
            delattr(self._obj, self._method_name)

    def _capture_original_method(self):
        try:
            self._original_method = getattr(self._obj, self._method_name)
        except AttributeError:
            pass

        setattr(self._obj, self._method_name, self)

    def _raise_exception(self, args, kwargs):
        raise UnallowedMethodCallError(
            "Received unexpected call to '{}' on {!r} with (args={}, kwargs={}).".format(
                self._method_name,
                self._obj,
                args,
                kwargs
            )
        )
