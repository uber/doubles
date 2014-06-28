from doubles.instance_double import InstanceDouble
from doubles.verification import verify_arguments, verify_method


class ClassDouble(InstanceDouble):
    def _doubles_verify_method_name(self, method_name):
        verify_method(self._doubles_target, method_name, class_level=True)

    def _doubles_verify_arguments(self, method_name, args, kwargs):
        args = list(args).insert(0, 'cls')
        verify_arguments(getattr(self._doubles_target, method_name), args, kwargs)
