from doubles.verifying_doubles.contracts import verify_arguments, verify_method
from doubles.verifying_doubles.verifying_double import VerifyingDouble


class ObjectDouble(VerifyingDouble):
    def _doubles_verify_method_name(self, method_name):
        verify_method(self._doubles_target, method_name)

    def _doubles_verify_arguments(self, method_name, args, kwargs):
        verify_arguments(getattr(self._doubles_target, method_name), args, kwargs)
