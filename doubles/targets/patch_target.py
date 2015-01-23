from doubles.lifecycle import current_space
from doubles.instance_double_factory import InstanceDoubleFactory, ClassDouble


def patch_constructor(target, *values):
    return patch(target, InstanceDoubleFactory(target, *values)).value


def patch(target, value=None):
    if value is None:
        value = ClassDouble(target)
    patch = current_space().patch_for(target)
    patch.set_value(value)
    return patch
