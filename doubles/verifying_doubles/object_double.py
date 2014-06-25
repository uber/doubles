from inspect import getargspec

from doubles.exceptions import VerifyingDoubleError
from doubles.verifying_doubles.verifying_double import VerifyingDouble


class ObjectDouble(VerifyingDouble):
    def _doubles_verify_method_name(self, method_name):
        if not hasattr(self._doubles_target, method_name):
            raise VerifyingDoubleError

        attr = getattr(self._doubles_target, method_name)

        if not callable(attr):
            raise VerifyingDoubleError

    def _doubles_verify_arguments(self, method_name, args, kwargs):
        argspec = getargspec(getattr(self._doubles_target, method_name))

        if len(args) != len(argspec.args):
            raise VerifyingDoubleError
