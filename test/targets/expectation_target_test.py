from doubles import lifecycle
from doubles.targets.expectation_target import expect, ExpectationTarget


class TestExpect(object):
    def setup(self):
        lifecycle.setup()

    def teardown(self):
        lifecycle.teardown()

    def test_returns_an_expectation_target(self):
        assert isinstance(expect('foo'), ExpectationTarget)
