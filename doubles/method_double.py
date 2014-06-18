from doubles.message_allowance import MessageAllowance


class MethodDouble(object):
    def __init__(self, method_name, obj):
        self._method_name = method_name
        self._obj = obj

        self._allowances = []

    def add_allowance(self):
        self._define_proxy_method()
        self._allowances.append(MessageAllowance())

    def add_expectation(self):
        self._define_proxy_method()
        self._allowances.append(MessageAllowance(verify=True))

    def _define_proxy_method(self):
        def proxy_method():
            pass

        setattr(self._obj, self._method_name, proxy_method)
