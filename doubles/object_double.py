from doubles.exceptions import VerifyingDoubleError
from doubles.verifying_double import VerifyingDouble


class ObjectDouble(VerifyingDouble):
    def _verify_method_name(self, method_name):
        if not hasattr(self._target, method_name):
            raise VerifyingDoubleError

        attr = getattr(self._target, method_name)

        if not callable(attr):
            raise VerifyingDoubleError
