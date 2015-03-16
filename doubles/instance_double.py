from inspect import isclass

from doubles.exceptions import VerifyingDoubleImportError
from doubles.object_double import ObjectDouble
from doubles.utils import get_module, get_path_components


def _get_doubles_target(module, class_name, path):
    """Validate and return the class to be doubled.

    :param module module: The module that contains the class that will be doubled.
    :param str class_name: The name of the class that will be doubled.
    :param str path: The full path to the class that will be doubled.
    :return: The class that will be doubled.
    :rtype: type
    :raise: ``VerifyingDoubleImportError`` if the target object doesn't exist or isn't a class.
    """

    try:
        doubles_target = getattr(module, class_name)
        if isinstance(doubles_target, ObjectDouble):
            return doubles_target._doubles_target

        if not isclass(doubles_target):
            raise VerifyingDoubleImportError(
                'Path does not point to a class: {}.'.format(path)
            )

        return doubles_target
    except AttributeError:
        raise VerifyingDoubleImportError(
            'No object at path: {}.'.format(path)
        )


class InstanceDouble(ObjectDouble):
    """A pure double representing an instance of the target class.

    Any kwargs supplied will be set as attributes on the instance that is
    created.

    ::

        user = InstanceDouble('myapp.User', name='Bob Barker')

    :param str path: The absolute module path to the class.
    """

    def __init__(self, path, **kwargs):
        module_path, class_name = get_path_components(path)
        module = get_module(module_path, path)
        self._doubles_target = _get_doubles_target(module, class_name, path)
        for k, v in kwargs.items():
            setattr(self, k, v)
