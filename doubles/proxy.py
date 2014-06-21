from doubles.method_double import MethodDouble


class Proxy(object):
    def __init__(self, obj):
        self._obj = obj
        self._method_doubles = {}

    def add_allowance(self, method_name):
        return self.method_double_for(method_name).add_allowance()

    def add_expectation(self, method_name):
        self.method_double_for(method_name).add_expectation()

    def verify(self):
        pass

    def method_double_for(self, method_name):
        if method_name in self._method_doubles:
            return self._method_doubles[method_name]
        else:
            method_double = self._method_doubles[method_name] = MethodDouble(method_name, self._obj)
            return method_double

    def __repr__(self):
        return "<Proxy({!r})>".format(self._obj)
