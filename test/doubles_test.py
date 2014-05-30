from doubles import double


class TestDouble(object):
    def test_returns_a_verifying_double(self):
        subject = double('foo')

        assert repr(subject) == "VerifyingDouble('foo')"

    def test_returns_an_unnamed_verifying_double(self):
        subject = double()

        assert repr(subject) == "VerifyingDouble (unnamed)"

    def test_returns_a_double(self):
        subject = double(verify=False)

        assert repr(subject) == "Double (unnamed)"

    def test_returns_an_unnamed_double(self):
        subject = double('foo', verify=False)

        assert repr(subject) == "Double('foo')"
