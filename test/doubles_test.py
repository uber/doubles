from mock import patch

import doubles


class TestSetupAndTeardown(object):
    def test_creates_and_stores_a_new_space(self):
        doubles.setup()

        assert isinstance(doubles._current, doubles.Space)

    def test_deletes_the_space(self):
        doubles.setup()
        doubles.teardown()

        assert doubles._current is None


@patch('doubles._current')
class TestVerify(object):
    def test_verifies_current_space(self, _current):
        doubles.verify()

        assert _current.verify.call_count == 1
