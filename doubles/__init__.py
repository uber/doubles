__version__ = '1.0.4'

from doubles.class_double import ClassDouble  # noqa
from doubles.instance_double import InstanceDouble  # noqa
from doubles.object_double import ObjectDouble  # noqa
from doubles.instance_double_factory import InstanceDoubleFactory  # noqa
from doubles.targets.allowance_target import allow  # noqa
from doubles.targets.expectation_target import expect  # noqa
from doubles.targets.patch_target import patch, patch_constructor  # noqa
from doubles.lifecycle import (  # noqa
    teardown,
    verify,
    no_builtin_verification,
    clear,
)
