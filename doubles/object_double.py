from doubles.verification import verify_arguments, verify_method


class ObjectDouble(object):
    def __init__(self, target):
        self._doubles_target = target

    def __repr__(self):
        address = hex(id(self))
        class_name = self.__class__.__name__

        return '<{} of {!r} object at {}>'.format(
            class_name,
            getattr(self, '_doubles_target'),
            address
        )

    def _doubles_verify_arguments(self, method_name, args, kwargs):
        verify_arguments(getattr(self._doubles_target, method_name), args, kwargs)

    def _doubles_verify_method_name(self, method_name):
        verify_method(self._doubles_target, method_name)
