class ObjectDouble(object):
    def __init__(self, target):
        self._doubles_target = target

    def __repr__(self):
        address = hex(id(self))
        class_name = self.__class__.__name__

        return '<{} of {!r} object at {}>'.format(
            class_name,
            self._doubles_target,
            address
        )
