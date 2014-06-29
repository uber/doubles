from doubles.lifecycle import current_space


def allow(target):
    return AllowanceTarget(target)


class AllowanceTarget(object):
    def __init__(self, target):
        self._proxy = current_space().proxy_for(target)

    def __getattr__(self, method_name):
        return self._proxy.add_allowance(method_name)
