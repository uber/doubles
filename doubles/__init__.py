__version__ = '1.1.2'

from doubles.class_double import ClassDouble  # noqa
from doubles.instance_double import InstanceDouble  # noqa
from doubles.object_double import ObjectDouble  # noqa
from doubles.targets.allowance_target import allow, allow_constructor  # noqa
from doubles.targets.expectation_target import expect, expect_constructor  # noqa
from doubles.targets.patch_target import patch, patch_class  # noqa
from doubles.lifecycle import (  # noqa
    teardown,
    verify,
    no_builtin_verification,
    clear,
)
