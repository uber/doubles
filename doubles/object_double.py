class ObjectDouble(object):
    """
    A pure double representing the target object.

    ::

        dummy_user = ObjectDouble(user)

    :param object target: The object the newly created ObjectDouble will verify against.
    """
    is_class = False

    def __init__(self, target):
        self._doubles_target = target

    def __repr__(self):
        """Provides a string representation of the double.

        NOTE: Includes the memory address and the name of the object being doubled.

        :return: A string representation of the double.
        :rtype: str
        """

        address = hex(id(self))
        class_name = self.__class__.__name__

        return '<{} of {!r} object at {}>'.format(
            class_name,
            self._doubles_target,
            address
        )
