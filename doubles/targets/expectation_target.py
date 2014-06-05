from doubles.lifecycle import current_space


def expect(target):
    return ExpectationTarget(target)


class ExpectationTarget(object):
    def __init__(self, target):
        self.target = target
        self.proxy = current_space().proxy_for(target)
