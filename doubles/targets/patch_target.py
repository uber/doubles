from doubles.lifecycle import current_space
from doubles.class_double import ClassDouble


def patch_class(target):
    """
    Replace the specified class with a ClassDouble

    :param str target: A string pointing to the target to patch.
    :param obj values: Values to return when new instances are created.
    :rtype Patch:
    """
    return patch(target, ClassDouble(target)).value


def patch(target, value):
    """
    Replace the specified object

    :param str target: A string pointing to the target to patch.
    :param object value: The value to replace the target with.
    :rtype Patch:
    """
    patch = current_space().patch_for(target)
    patch.set_value(value)
    return patch
