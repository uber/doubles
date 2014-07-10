import re

from pytest import raises

from doubles.exceptions import MockExpectationError
from doubles.instance_double import InstanceDouble
from doubles.lifecycle import verify
from doubles.targets.expectation_target import expect


class TestExpect(object):
    def test_raises_if_an_expected_method_call_is_not_made(self):
        subject = InstanceDouble('doubles.testing.User')

        expect(subject).instance_method

        with raises(MockExpectationError) as e:
            verify()

        assert re.match(
            r"Expected 'instance_method' to be called on "
            r"<InstanceDouble of <class 'doubles.testing.User'> object at .+> "
            r"with any args, but was not."
            r" \(.*doubles/test/expect_test.py:\d+\)",
            e.value.message
        )

    def test_raises_if_method_is_called_with_wrong_arguments(self):
        subject = InstanceDouble('doubles.testing.User')

        expect(subject).method_with_varargs.with_args('bar')

        with raises(MockExpectationError) as e:
            verify()

        assert re.match(
            r"Expected 'method_with_varargs' to be called on "
            r"<InstanceDouble of <class 'doubles.testing.User'> object at .+> "
            r"with \(args=\('bar',\), kwargs={}\), but was not."
            r" \(.*doubles/test/expect_test.py:\d+\)",
            e.value.message
        )

    def test_passes_if_an_expected_method_call_is_made(self):
        subject = InstanceDouble('doubles.testing.User')

        expect(subject).instance_method

        subject.instance_method()

    def test_passes_if_method_is_called_with_specified_arguments(self):
        subject = InstanceDouble('doubles.testing.User')

        expect(subject).method_with_default_args.with_args('one', bar='two')

        assert subject.method_with_default_args('one', bar='two') is None
