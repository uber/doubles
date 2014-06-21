from pytest import raises

from doubles import Double, expect, verify
from doubles.exceptions import MockExpectationError


class TestExpect(object):
    def test_raises_if_an_expected_method_call_is_not_made(self):
        subject = Double()

        expect(subject).to_receive('foo')

        with raises(MockExpectationError):
            verify()
