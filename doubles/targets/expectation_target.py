def expect(target):
    return ExpectationTarget(target)


class ExpectationTarget(object):
    def __init__(self, target):
        self.target = target
