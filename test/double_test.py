from doubles.double import Double


class TestDouble(object):
    def test_returns_a_double(self):
        subject = Double()

        assert repr(subject) == "Double (unnamed)"

    def test_returns_an_unnamed_double(self):
        subject = Double('foo')

        assert repr(subject) == "Double('foo')"
