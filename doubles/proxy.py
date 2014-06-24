from doubles.method_double import MethodDouble
from doubles import Double
from doubles.exceptions import VerifyingDoubleError


class Proxy(object):
    def __init__(self, obj):
        self._obj = obj
        self._method_doubles = {}
        self._pure_double = isinstance(self._obj, Double)

    def add_allowance(self, method_name):
        return self.method_double_for(method_name).add_allowance()

    def add_expectation(self, method_name):
        return self.method_double_for(method_name).add_expectation()

    def restore_original_object(self):
        for method_double in self._method_doubles.values():
            method_double.restore_original_method()

    def verify(self):
        for method_double in self._method_doubles.values():
            method_double.verify()

    def method_double_for(self, method_name):
        if method_name in self._method_doubles:
            return self._method_doubles[method_name]
        elif self._pure_double or self._is_valid_method(method_name):
            method_double = self._method_doubles[method_name] = MethodDouble(method_name, self._obj)
            return method_double
        else:
            raise VerifyingDoubleError

    def _is_valid_method(self, method_name):
        if hasattr(self._obj, method_name):
            method = getattr(self._obj, method_name)
            # this way would fail on built-in methods e.g. __new__
            # return ismethod(method) or isinstance(method, classmethod):
            return hasattr(method, '__call__')
        return False
