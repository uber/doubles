from doubles.targets.allowance_target import allow, AllowanceTarget


class TestAllow(object):
    def test_returns_an_allowance_target(self):
        assert isinstance(allow('foo'), AllowanceTarget)
