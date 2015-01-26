from doubles.class_double import ClassDouble
from doubles.verification import verify_arguments
from doubles.target import Target
from doubles.exceptions import UnallowedMethodCallError


class Instantiator(object):
    @classmethod
    def _doubles__new__(self, *args, **kwargs):
        return None


def patch_class(input_class):
    new_class = type('Doubled' + input_class.__name__, (input_class, Instantiator), {})
    return new_class


class ClassPatcher(ClassDouble):
    def __init__(self, path, *values):
        super(ClassPatcher, self).__init__(path)
        self._doubles_target = patch_class(self._doubles_target)
        self._set_target()

    def __call__(self, *args, **kwargs):
        self.verify_arguments(args, kwargs)
        return self._doubles__new__(*args, **kwargs)

    def _set_target(self):
        self._target = Target(self._doubles_target)

    def verify_arguments(self, args, kwargs):
        verify_arguments(self._target, '__init__', args, kwargs)

    def _doubles__new__(self, *args, **kwargs):
        raise UnallowedMethodCallError('Foobar')
