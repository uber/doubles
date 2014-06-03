from mock import patch
from pytest import raises

import doubles


class TestSetupAndTeardown(object):
    def setup(self):
        doubles.teardown()

    def test_creates_and_stores_a_new_space(self):
        doubles.setup()

        assert isinstance(doubles._current, doubles.Space)

    def test_deletes_the_space(self):
        doubles.setup()
        doubles.teardown()

        assert doubles._current is None


class TestVerify(object):
    def setup(self):
        doubles.teardown()

    @patch('doubles._current')
    def test_verifies_current_space(self, _current):
        doubles.verify()

        assert _current.verify.call_count == 1

    def test_raises_when_verify_is_called_without_a_space(self):
        with raises(doubles.NoSpaceError):
            doubles.verify()
