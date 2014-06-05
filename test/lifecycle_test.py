from mock import patch
from pytest import raises

from doubles import lifecycle


class TestSetupAndTeardown(object):
    def test_creates_and_stores_a_new_space(self):
        assert isinstance(lifecycle.current_space(), lifecycle.Space)

    def test_deletes_the_space(self):
        lifecycle.teardown()

        assert lifecycle.current_space() is None


class TestVerify(object):
    @patch('doubles.lifecycle.current_space')
    def test_verifies_current_space(self, current_space):
        lifecycle.verify()

        assert current_space.return_value.verify.call_count == 1

    def test_raises_when_verify_is_called_without_a_space(self):
        lifecycle.teardown()

        with raises(lifecycle.NoSpaceError):
            lifecycle.verify()
