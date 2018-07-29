from doubles.exceptions import VerifyingDoubleError
from doubles.utils import get_module, get_path_components


class Patch(object):
    """
    A wrapper around an object that has been ``patched``
    """
    def __init__(self, target):
        """
        :param str path: The absolute module path to the class.
        """
        module_path, self._name = get_path_components(target)
        self.target = get_module(module_path, target)
        self._capture_original_object()
        self.set_value(None)

    def _capture_original_object(self):
        """Capture the original python object."""
        try:
            self._doubles_target = getattr(self.target, self._name)
        except AttributeError:
            raise VerifyingDoubleError(self.target, self._name)

    def set_value(self, value):
        """Set the value of the target.

        :param obj value: The value to set.
        """
        self._value = value
        setattr(self.target, self._name, value)

    def restore_original_object(self):
        """Restore the target to it's original value."""
        self.set_value(self._doubles_target)
