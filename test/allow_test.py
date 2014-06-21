from pytest import raises

from doubles import allow, Double


class TestAllow(object):
    def test_allows_method_calls_on_doubles(self):
        subject = Double()

        allow(subject).to_receive('foo')

        assert subject.foo() is None

    def test_raises_on_undefined_attribute_access(self):
        subject = Double()

        with raises(AttributeError):
            subject.foo

    def test_returns_specified_value(self):
        subject = Double()

        allow(subject).to_receive('foo').and_return('bar')

        assert subject.foo() == 'bar'
