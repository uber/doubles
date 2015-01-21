from doubles.utils import get_module, get_path_components
from doubles.exceptions import VerifyingDoubleError


class Patch(object):
    def __init__(self, target):
        module_path, self._name = get_path_components(target)
        self.target = get_module(module_path, target)
        self._capture_original_object()
        self.set_value(None)

    def _capture_original_object(self):
        try:
            self._original_obect = getattr(self.target, self._name)
        except AttributeError:
            raise VerifyingDoubleError(self.target, self._name)

    def set_value(self, value):
        self._value = value
        setattr(self.target, self._name, value)

    @property
    def value(self):
        return self._value

    @property
    def original_obect(self):
        return self._original_obect

    def restore_original_object(self):
        self.set_value(self._original_obect)
