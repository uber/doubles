from importlib import import_module

from doubles.verifying_doubles.contracts import verify_arguments, verify_method
from doubles.verifying_doubles.verifying_double import VerifyingDouble


class ClassDouble(VerifyingDouble):
    def __init__(self, target):
        path_segments = target.split('.')
        module_path = '.'.join(path_segments[:-1])
        module = import_module(module_path)
        self._doubles_target = getattr(module, path_segments[-1])

    def _doubles_verify_method_name(self, method_name):
        verify_method(self._doubles_target, method_name, class_level=True)

    def _doubles_verify_arguments(self, method_name, args, kwargs):
        verify_arguments(getattr(self._doubles_target, method_name), args, kwargs)
