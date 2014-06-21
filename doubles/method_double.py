from doubles.message_allowance import MessageAllowance


class MethodDouble(object):
    def __init__(self, method_name, obj):
        self._method_name = method_name
        self._obj = obj

        self._allowances = []

    def add_allowance(self):
        self._define_proxy_method()
        allowance = MessageAllowance()
        self._allowances.append(allowance)
        return allowance

    def _define_proxy_method(self):
        def proxy_method(*args, **kwargs):
            return self._find_matching_allowance(args, kwargs).return_value

        setattr(self._obj, self._method_name, proxy_method)

    def _find_matching_allowance(self, args, kwargs):
        return self._allowances[0]
