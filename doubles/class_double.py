from doubles.instance_double import InstanceDouble


class ClassDouble(InstanceDouble):
    """
    A pure double representing the target class.

    ::

        User = ClassDouble('myapp.User')

    :param str path: The absolute module path to the class.
    """

    is_class = True
