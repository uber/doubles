import re

from pytest import raises

from doubles.exceptions import MockExpectationError, UnsupportedMethodError
from doubles.instance_double import InstanceDouble
from doubles.lifecycle import verify, teardown
from doubles.targets.allowance_target import allow
from doubles.targets.expectation_target import expect


class TestExpect(object):
    def test_raises_if_an_expected_method_call_without_args_is_not_made(self):
        subject = InstanceDouble('doubles.testing.User')

        expect(subject).instance_method

        with raises(MockExpectationError) as e:
            verify()
        teardown()

        assert re.match(
            r"Expected 'instance_method' to be called on "
            r"<InstanceDouble of <class '?doubles.testing.User'?"
            r"(?: at 0x[0-9a-f]{9})?> object at .+> "
            r"with any args, but was not."
            r" \(.*doubles/test/expect_test.py:\d+\)",
            e.value.message
        )

    def test_raises_if_an_expected_method_call_with_args_is_not_made(self):
        subject = InstanceDouble('doubles.testing.User')

        expect(subject).method_with_varargs.with_args('bar')

        with raises(MockExpectationError) as e:
            verify()
        teardown()

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

    def test_does_not_support_and_raise(self):
        subject = InstanceDouble('doubles.testing.User')

        with raises(UnsupportedMethodError) as e:
            expect(subject).instance_method.and_raise(Exception)

        assert re.match(r"`expect` does not support and_raise\.", e.value.message)

        teardown()

    def test_does_not_support_and_return(self):
        subject = InstanceDouble('doubles.testing.User')

        with raises(UnsupportedMethodError) as e:
            expect(subject).instance_method.and_return('foo')

        assert re.match(r"`expect` does not support and_return\.", e.value.message)

        teardown()

    def test_does_not_support_and_return_result_of(self):
        subject = InstanceDouble('doubles.testing.User')

        with raises(UnsupportedMethodError) as e:
            expect(subject).instance_method.and_return_result_of(lambda: 'foo')

        assert re.match(r"`expect` does not support and_return_result_of\.", e.value.message)

        teardown()

    def test_takes_precendence_over_previous_allowance(self):
        subject = InstanceDouble('doubles.testing.User')

        allow(subject).instance_method.and_return('foo')
        expect(subject).instance_method

        assert subject.instance_method() is None

    def test_takes_precedence_over_subsequent_allowances(self):
        subject = InstanceDouble('doubles.testing.User')

        expect(subject).instance_method
        allow(subject).instance_method.and_return('foo')

        with raises(MockExpectationError):
            verify()

        teardown()


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


class TestAtLeast(object):
    def test_calls_are_chainable(self):
        subject = InstanceDouble('doubles.testing.User')

        expect(subject).instance_method.at_least(2).times.at_least(1).times

        subject.instance_method()

    def test_fails_when_called_less_than_at_least_times(self):
        subject = InstanceDouble('doubles.testing.User')

        expect(subject).instance_method.at_least(2).times

        subject.instance_method()
        with raises(MockExpectationError) as e:
            verify()
        teardown()

        assert re.match(
            r"Expected 'instance_method' to be called at least 2 times but was called 1 time on "
            r"<InstanceDouble of <class 'doubles.testing.User'> object at .+> "
            r"with any args, but was not."
            r" \(.*doubles/test/expect_test.py:\d+\)",
            e.value.message
        )

    def test_passes_when_called_exactly_at_least_times(self):
        subject = InstanceDouble('doubles.testing.User')

        expect(subject).instance_method.at_least(1).times

        subject.instance_method()
        subject.instance_method()

    def test_passes_when_called_more_than_at_least_times(self):
        subject = InstanceDouble('doubles.testing.User')

        expect(subject).instance_method.at_least(1).times

        subject.instance_method()
        subject.instance_method()


class TestAtMost(object):
    def test_calls_are_chainable(self):
        subject = InstanceDouble('doubles.testing.User')

        expect(subject).instance_method.at_most(1).times.at_most(2).times

        subject.instance_method()
        subject.instance_method()

    def test_passes_when_called_exactly_at_most_times(self):
        subject = InstanceDouble('doubles.testing.User')

        expect(subject).instance_method.at_most(1).times

        subject.instance_method()

    def test_passes_when_called_less_than_at_most_times(self):
        subject = InstanceDouble('doubles.testing.User')

        expect(subject).instance_method.at_most(2).times

        subject.instance_method()

    def test_fails_when_called_more_than_at_most_times(self):
        subject = InstanceDouble('doubles.testing.User')

        expect(subject).instance_method.at_most(1).times

        subject.instance_method()
        with raises(MockExpectationError) as e:
            subject.instance_method()
        teardown()

        assert re.match(
            r"Expected 'instance_method' to be called at most 1 time but was called 2 times on "
            r"<InstanceDouble of <class 'doubles.testing.User'> object at .+> "
            r"with any args, but was not."
            r" \(.*doubles/test/expect_test.py:\d+\)",
            e.value.message
        )


class Test__call__(object):
    def test_satisfied_expectation(self):
        subject = InstanceDouble('doubles.testing.User')

        expect(subject).__call__.once()

        subject()

    def test_unsatisfied_expectation(self):
        subject = InstanceDouble('doubles.testing.User')

        expect(subject).__call__.once()

        with raises(MockExpectationError) as e:
            verify()
        teardown()

        assert re.match(
            r"Expected '__call__' to be called 1 time but was called 0 times on "
            r"<InstanceDouble of <class 'doubles.testing.User'> object at .+> "
            r"with any args, but was not."
            r" \(.*doubles/test/expect_test.py:\d+\)",
            e.value.message
        )


class Test__enter__(object):
    def test_satisfied_expectation(self):
        subject = InstanceDouble('doubles.testing.User')

        expect(subject).__enter__.once()
        allow(subject).__exit__

        with subject:
            pass

    def test_unsatisfied_expectation(self):
        subject = InstanceDouble('doubles.testing.User')

        expect(subject).__enter__.once()

        with raises(MockExpectationError) as e:
            verify()
        teardown()

        assert re.match(
            r"Expected '__enter__' to be called 1 time but was called 0 times on "
            r"<InstanceDouble of <class 'doubles.testing.User'> object at .+> "
            r"with any args, but was not."
            r" \(.*doubles/test/expect_test.py:\d+\)",
            e.value.message
        )


class Test__exit__(object):
    def test_satisfied_expectation(self):
        subject = InstanceDouble('doubles.testing.User')

        allow(subject).__enter__
        expect(subject).__exit__.once()

        with subject:
            pass

    def test_unsatisfied_expectation(self):
        subject = InstanceDouble('doubles.testing.User')

        expect(subject).__exit__.once()

        with raises(MockExpectationError) as e:
            verify()
        teardown()

        assert re.match(
            r"Expected '__exit__' to be called 1 time but was called 0 times on "
            r"<InstanceDouble of <class 'doubles.testing.User'> object at .+> "
            r"with any args, but was not."
            r" \(.*doubles/test/expect_test.py:\d+\)",
            e.value.message
        )
