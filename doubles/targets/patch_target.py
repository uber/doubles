from doubles.lifecycle import current_space
from doubles.class_patcher import ClassPatcher
from doubles.targets.allowance_target import allow_constructor


def patch_class(target, *values):
    """
    Replace the specified class with a ClassPatcher

    :param str target: A string pointing to the target to patch.
    :param obj values: Values to return when new instances are created.
    :rtype Patch:
    """
    output = patch(target, ClassPatcher(target)).value
    if values:
        allow_constructor(output).and_return(*values)
    return output


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
