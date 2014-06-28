from importlib import import_module

from doubles.object_double import ObjectDouble
from doubles.verification import verify_arguments


class InstanceDouble(ObjectDouble):
    def __init__(self, target):
        path_segments = target.split('.')
        module_path = '.'.join(path_segments[:-1])
        module = import_module(module_path)
        self._doubles_target = getattr(module, path_segments[-1])

    def _doubles_verify_arguments(self, method_name, args, kwargs):
        attr = getattr(self._doubles_target, method_name)
        verify_arguments(attr, self._doubles_add_owner_to_args(args), kwargs)

    def _doubles_add_owner_to_args(self, args):
        l = list(args)
        l.insert(0, 'owner')
        return l
