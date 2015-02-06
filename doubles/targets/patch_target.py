from doubles.lifecycle import current_space
from doubles.class_double import ClassDouble


def patch_class(target):
    """
    Replace the specified class with a ClassDouble

    :param str target: A string pointing to the target to patch.
    :param obj values: Values to return when new instances are created.
    :return: A ``ClassDouble`` object.
    """
    class_double = ClassDouble(target)
    patch(target, class_double)
    return class_double


def patch(target, value):
    """
    Replace the specified object

    :param str target: A string pointing to the target to patch.
    :param object value: The value to replace the target with.
    :return: A ``Patch`` object.
    """
    patch = current_space().patch_for(target)
    patch.set_value(value)
    return patch
