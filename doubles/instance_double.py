from importlib import import_module

from doubles.object_double import ObjectDouble


class InstanceDouble(ObjectDouble):
    """
    A pure double representing an instance of the target class.

    ::

        user = InstanceDouble('myapp.User')

    :param str target: The absolute module path to the class.
    """

    def __init__(self, target):
        path_segments = target.split('.')
        module_path = '.'.join(path_segments[:-1])
        module = import_module(module_path)
        self._doubles_target = getattr(module, path_segments[-1])
