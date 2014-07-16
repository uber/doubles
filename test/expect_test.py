import re

from pytest import raises

from doubles.exceptions import MockExpectationError
from doubles.instance_double import InstanceDouble
from doubles.lifecycle import verify, teardown
from doubles.targets.expectation_target import expect


class TestExpect(object):
    def test_raises_if_an_expected_method_call_is_not_made(self):
        subject = InstanceDouble('doubles.testing.User')

        expect(subject).instance_method

        with raises(MockExpectationError) as e:
            verify()

        assert re.match(
            r"Expected 'instance_method' to be called on "
            r"<InstanceDouble of <class '?doubles.testing.User'?"
            r"(?: at 0x[0-9a-f]{9})?> object at .+> "
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
            r"<InstanceDouble of <class '?doubles.testing.User'?"
            r"(?: at 0x[0-9a-f]{9})?> object at .+> "
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


class TestTwice(object):
    def test_passes_when_called_twice(self):
        subject = InstanceDouble('doubles.testing.User')

        expect(subject).instance_method.twice()

        subject.instance_method()
        subject.instance_method()

    def test_fails_when_called_once(self):
        subject = InstanceDouble('doubles.testing.User')

        expect(subject).instance_method.twice()

        subject.instance_method()
        with raises(MockExpectationError) as e:
            verify()
        teardown()

        assert re.match(
            r"Expected 'instance_method' to be called 2 times but was called 1 time on "
            r"<InstanceDouble of <class 'doubles.testing.User'> object at .+> "
            r"with any args, but was not."
            r" \(.*doubles/test/expect_test.py:\d+\)",
            e.value.message
        )

    def test_fails_when_called_three_times(self):
        subject = InstanceDouble('doubles.testing.User')

        expect(subject).instance_method.twice()

        subject.instance_method()
        subject.instance_method()
        with raises(MockExpectationError) as e:
            subject.instance_method()
        teardown()

        assert re.match(
            r"Expected 'instance_method' to be called 2 times but was called 3 times on "
            r"<InstanceDouble of <class 'doubles.testing.User'> object at .+> "
            r"with any args, but was not."
            r" \(.*doubles/test/expect_test.py:\d+\)",
            e.value.message
        )


class TestOnce(object):
    def test_passes_when_called_once(self):
        subject = InstanceDouble('doubles.testing.User')

        expect(subject).instance_method.once()

        subject.instance_method()

    def test_fails_when_called_two_times(self):
        subject = InstanceDouble('doubles.testing.User')

        expect(subject).instance_method.once()

        subject.instance_method()
        with raises(MockExpectationError) as e:
            subject.instance_method()
        teardown()

        assert re.match(
            r"Expected 'instance_method' to be called 1 time but was called 2 times on "
            r"<InstanceDouble of <class 'doubles.testing.User'> object at .+> "
            r"with any args, but was not."
            r" \(.*doubles/test/expect_test.py:\d+\)",
            e.value.message
        )


class TestExactly(object):
    def test_calls_are_chainable(self):
        subject = InstanceDouble('doubles.testing.User')

        expect(subject).instance_method.exactly(1).times.exactly(2).times

        subject.instance_method()
        subject.instance_method()

    def test_fails_when_called_less_than_expected_times(self):
        subject = InstanceDouble('doubles.testing.User')

        expect(subject).instance_method.exactly(2).times

        subject.instance_method()
        with raises(MockExpectationError) as e:
            verify()
        teardown()

        assert re.match(
            r"Expected 'instance_method' to be called 2 times but was called 1 time on "
            r"<InstanceDouble of <class 'doubles.testing.User'> object at .+> "
            r"with any args, but was not."
            r" \(.*doubles/test/expect_test.py:\d+\)",
            e.value.message
        )

    def test_passes_when_called_exactly_expected_times(self):
        subject = InstanceDouble('doubles.testing.User')

        expect(subject).instance_method.exactly(1).times

        subject.instance_method()

    def test_fails_when_called_more_than_expected_times(self):
        subject = InstanceDouble('doubles.testing.User')

        expect(subject).instance_method.exactly(1).times

        subject.instance_method()
        with raises(MockExpectationError) as e:
            subject.instance_method()
        teardown()

        assert re.match(
            r"Expected 'instance_method' to be called 1 time but was called 2 times on "
            r"<InstanceDouble of <class 'doubles.testing.User'> object at .+> "
            r"with any args, but was not."
            r" \(.*doubles/test/expect_test.py:\d+\)",
            e.value.message
        )
