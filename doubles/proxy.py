from doubles.method_double import MethodDouble


class Proxy(object):
    def __init__(self, obj):
        self._obj = obj

    def add_allowance(self, method_name):
        self._method_double_for(method_name).add_allowance()

    def add_expectation(self, method_name):
        self._method_double_for(method_name).add_expectation()

    def verify(self):
        pass

    def _method_double_for(self, method_name):
        return MethodDouble(method_name, self._obj)

    def __repr__(self):
        return "<Proxy({!r})>".format(self._obj)


class MockExpectationError(Exception):
    pass
