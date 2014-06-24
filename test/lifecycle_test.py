from pytest import raises

from doubles import lifecycle
from doubles.exceptions import NoSpaceError


class TestLifecycle(object):
    def test_raises_on_verify_without_a_space(self):
        lifecycle.teardown()

        with raises(NoSpaceError):
            lifecycle.verify()
