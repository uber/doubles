from doubles.double import Double


class VerifyingDouble(Double):
    def __init__(self, target):
        self._doubles_target = target
