from doubles.targets.expectation_target import expect, ExpectationTarget


class TestExpect(object):
    def test_returns_an_expectation_target(self):
        assert isinstance(expect('foo'), ExpectationTarget)
