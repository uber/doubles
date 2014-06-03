from mock import patch
from pytest import raises

from doubles import lifecycle


class TestSetupAndTeardown(object):
    def setup(self):
        lifecycle.teardown()

    def test_creates_and_stores_a_new_space(self):
        lifecycle.setup()

        assert isinstance(lifecycle._current, lifecycle.Space)

    def test_deletes_the_space(self):
        lifecycle.setup()
        lifecycle.teardown()

        assert lifecycle._current is None


class TestVerify(object):
    def setup(self):
        lifecycle.teardown()

    @patch('doubles.lifecycle._current')
    def test_verifies_current_space(self, _current):
        lifecycle.verify()

        assert _current.verify.call_count == 1

    def test_raises_when_verify_is_called_without_a_space(self):
        with raises(lifecycle.NoSpaceError):
            lifecycle.verify()
