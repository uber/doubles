class ObjectDouble(object):
    """
    A pure double representing the target object.

    ::

        dummy_user = ObjectDouble(user)

    :param target: The object the newly created ObjectDouble will verify against.
    :type target: any object
    """
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
