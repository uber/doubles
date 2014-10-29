__version__ = '1.0.1'

from doubles.class_double import ClassDouble  # noqa
from doubles.instance_double import InstanceDouble  # noqa
from doubles.object_double import ObjectDouble  # noqa
from doubles.targets.allowance_target import allow  # noqa
from doubles.targets.expectation_target import expect  # noqa
from doubles.lifecycle import teardown, verify, no_builtin_verification  # noqa
