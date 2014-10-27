from importlib import import_module
from inspect import isclass

from doubles.exceptions import VerifyingDoubleImportError
from doubles.object_double import ObjectDouble


def _get_doubles_target(module, class_name, path):
    """
    Validate and return the class to be doubled.

    :param module module: The module that contains the class that will be doubled.
    :param str class_name: The name of the class that will be doubled.
    :param str path: The full path to the class that will be doubled.
    :return: The class that will be doubled.
    :rtype: type
    :raise: ``VerifyingDoubleImportError`` if the target object doesn't exist or isn't a class.
    """

    try:
        doubles_target = getattr(module, class_name)

        if not isclass(doubles_target):
            raise VerifyingDoubleImportError(
                'Path does not point to a class: {}.'.format(path)
            )

        return doubles_target
    except AttributeError:
        raise VerifyingDoubleImportError(
            'No object at path: {}.'.format(path)
        )


def _get_module(module_path, full_path):
    """
    Return the module given its path.

    :param str module_path: The path to the module to import.
    :param str full_path: The full path to the class that will be doubled.
    :return: The module object.
    :rtype: module
    :raise: ``VerifyingDoubleImportError`` if the module can't be imported.
    """

    try:
        return import_module(module_path)
    except ImportError:
        raise VerifyingDoubleImportError('Cannot import object from path: {}.'.format(full_path))


def _get_path_components(path):
    """
    Extract the module name and class name out of the fully qualified path to the class.

    :param str path: The full path to the class.
    :return: The module path and the class name.
    :rtype: str, str
    :raise: ``VerifyingDoubleImportError`` if the path is to a top-level module.
    """

    path_segments = path.split('.')
    module_path = '.'.join(path_segments[:-1])

    if module_path == '':
        raise VerifyingDoubleImportError('Invalid import path: {}.'.format(path))

    class_name = path_segments[-1]

    return module_path, class_name


class InstanceDouble(ObjectDouble):
    """
    A pure double representing an instance of the target class.

    Any kwargs supplied will be set as attributes on the instance that is
    created.

    ::

        user = InstanceDouble('myapp.User', name='Bob Barker')

    :param str path: The absolute module path to the class.
    """

    def __init__(self, path, **kwargs):
        module_path, class_name = _get_path_components(path)
        module = _get_module(module_path, path)
        self._doubles_target = _get_doubles_target(module, class_name, path)
        for k, v in kwargs.items():
            setattr(self, k, v)
