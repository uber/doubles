from doubles.lifecycle import current_space


def expect(target):
    return ExpectationTarget(target)


class ExpectationTarget(object):
    def __init__(self, target):
        self._proxy = current_space().proxy_for(target)

    def __getattribute__(self, attr_name):
        __dict__ = object.__getattribute__(self, '__dict__')

        if __dict__ and attr_name in __dict__:
            return __dict__[attr_name]

        return self._proxy.add_expectation(attr_name)
