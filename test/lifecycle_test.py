from mock import patch
from pytest import raises

from doubles import lifecycle


class TestSetupAndTeardown(object):
    def setup(self):
        lifecycle.teardown()

    def test_creates_and_stores_a_new_space(self):
        lifecycle.setup()

        assert isinstance(lifecycle.current_space(), lifecycle.Space)

    def test_deletes_the_space(self):
        lifecycle.setup()
        lifecycle.teardown()

        assert lifecycle.current_space() is None


class TestVerify(object):
    def setup(self):
        lifecycle.teardown()

    @patch('doubles.lifecycle.current_space')
    def test_verifies_current_space(self, current_space):
        lifecycle.setup()
        lifecycle.verify()

        assert current_space.return_value.verify.call_count == 1

    def test_raises_when_verify_is_called_without_a_space(self):
        with raises(lifecycle.NoSpaceError):
            lifecycle.verify()
