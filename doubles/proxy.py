from doubles.method_double import MethodDouble
from doubles.target import Target


class Proxy(object):
    def __init__(self, obj):
        self._target = Target(obj)
        self._method_doubles = {}

    def add_allowance(self, method_name):
        return self.method_double_for(method_name).add_allowance()

    def add_expectation(self, method_name, caller):
        return self.method_double_for(method_name).add_expectation(caller)

    def restore_original_object(self):
        for method_double in self._method_doubles.values():
            method_double.restore_original_method()

    def verify(self):
        for method_double in self._method_doubles.values():
            method_double.verify()

    def method_double_for(self, method_name):
        if method_name not in self._method_doubles:
            self._method_doubles[method_name] = MethodDouble(method_name, self._target)

        return self._method_doubles[method_name]
