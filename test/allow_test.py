from pytest import raises

from doubles import allow, Double
from doubles.double import UnallowedMethodCallError


class TestAllow(object):
    def test_allows_method_calls_on_doubles(self):
        subject = Double()

        allow(subject).to_receive('foo')

        assert subject.foo() is None

    def test_raises_on_unallowed_method_call(self):
        subject = Double()

        with raises(UnallowedMethodCallError):
            subject.foo()
