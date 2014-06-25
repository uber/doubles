class Double(object):
    def __init__(self, *args):
        if len(args) >= 1:
            self._doubles_target = args[0]

    def __repr__(self):
        address = hex(id(self))
        class_name = self.__class__.__name__

        if hasattr(self, '_doubles_target'):
            return '<{} of {!r} object at {}>'.format(
                class_name,
                getattr(self, '_doubles_target'),
                address
            )
        else:
            return '<{} object at {}>'.format(class_name, address)
