import re

from pytest import raises

from doubles.exceptions import UnallowedMethodCallError, MockExpectationError
from doubles.instance_double import InstanceDouble
from doubles.targets.allowance_target import allow
from doubles.lifecycle import teardown


class UserDefinedException(Exception):
    pass


class TestBasicAllowance(object):
    def test_allows_method_calls_on_doubles(self):
        subject = InstanceDouble('doubles.testing.User')

        allow(subject).instance_method

        assert subject.instance_method() is None

    def test_raises_on_undefined_attribute_access(self):
        subject = InstanceDouble('doubles.testing.User')

        with raises(AttributeError):
            subject.instance_method


class TestReturnValues(object):
    def test_returns_result_of_a_callable(self):
        subject = InstanceDouble('doubles.testing.User')

        allow(subject).instance_method.and_return_result_of(lambda: 'bar')

        assert subject.instance_method() == 'bar'

    def test_raises_provided_exception(self):
        subject = InstanceDouble('doubles.testing.User')

        allow(subject).instance_method.and_raise(UserDefinedException)

        with raises(UserDefinedException):
            subject.instance_method()

    def test_chaining_result_methods_gives_the_last_one_precedence(self):
        subject = InstanceDouble('doubles.testing.User')

        allow(subject).instance_method.and_return('bar').and_return_result_of(
            lambda: 'baz'
        ).and_raise(UserDefinedException).and_return('final')

        assert subject.instance_method() == 'final'


class TestAndReturn(object):
    def test_raises_if_no_arguments_supplied(self):
        subject = InstanceDouble('doubles.testing.User')

        with raises(TypeError) as e:
            allow(subject).instance_method.and_return()

        assert e.value.message == 'and_return() expected at least 1 return value'

    def test_returns_specified_value(self):
        subject = InstanceDouble('doubles.testing.User')

        allow(subject).instance_method.and_return('bar')

        assert subject.instance_method() == 'bar'

    def test_returns_specified_values_in_order(self):
        subject = InstanceDouble('doubles.testing.User')

        allow(subject).instance_method.and_return('bar', 'bazz')

        assert subject.instance_method() == 'bar'
        assert subject.instance_method() == 'bazz'

    def test_returns_the_last_specified_value_multiple_times(self):
        subject = InstanceDouble('doubles.testing.User')

        allow(subject).instance_method.and_return('bar', 'bazz')

        assert subject.instance_method() == 'bar'
        assert subject.instance_method() == 'bazz'
        assert subject.instance_method() == 'bazz'


class TestWithArgs(object):
    def test_allows_any_arguments_if_none_are_specified(self):
        subject = InstanceDouble('doubles.testing.User')

        allow(subject).instance_method.and_return('bar')

        assert subject.instance_method('unspecified argument') == 'bar'

    def test_allows_specification_of_arguments(self):
        subject = InstanceDouble('doubles.testing.User')

        allow(subject).method_with_positional_arguments.with_args('foo')

        assert subject.method_with_positional_arguments('foo') is None

    def test_raises_if_arguments_were_specified_but_not_provided_when_called(self):
        subject = InstanceDouble('doubles.testing.User')

        allow(subject).method_with_default_args.with_args('one', bar='two')

        with raises(UnallowedMethodCallError) as e:
            subject.method_with_default_args()

        assert re.match(
            r"Received unexpected call to 'method_with_default_args' on "
            r"<InstanceDouble of <class '?doubles.testing.User'?"
            r"(?: at 0x[0-9a-f]{9})?> object at .+> "
            r"with \(args=\(\), kwargs={}\).",
            e.value.message
        )

    def test_matches_most_specific_allowance(self):
        subject = InstanceDouble('doubles.testing.User')

        allow(subject).method_with_varargs.and_return('bar')
        allow(subject).method_with_varargs.with_args('baz').and_return('blah')

        assert subject.method_with_varargs('baz') == 'blah'


class TestWithNoArgs(object):
    def test_allows_call_with_no_arguments(self):
        subject = InstanceDouble('doubles.testing.User')

        allow(subject).instance_method.with_no_args()

        assert subject.instance_method() is None

    def test_raises_if_called_with_args(self):
        subject = InstanceDouble('doubles.testing.User')

        allow(subject).instance_method.with_no_args()

        with raises(UnallowedMethodCallError) as e:
            subject.instance_method('bar')

        assert re.match(
            r"Received unexpected call to 'instance_method' on "
            r"<InstanceDouble of <class '?doubles.testing.User'?"
            r"(?: at 0x[0-9a-f]{9})?> object at .+> "
            r"with \(args=\('bar',\), kwargs={}\).",
            e.value.message
        )

    def test_chains_with_return_values(self):
        subject = InstanceDouble('doubles.testing.User')

        allow(subject).instance_method.with_no_args().and_return('bar')

        assert subject.instance_method() == 'bar'


class TestTwice(object):
    def test_passes_when_called_twice(self):
        subject = InstanceDouble('doubles.testing.User')

        allow(subject).instance_method.twice()

        subject.instance_method()
        subject.instance_method()

    def test_passes_when_called_once(self):
        subject = InstanceDouble('doubles.testing.User')

        allow(subject).instance_method.twice()

        subject.instance_method()
        subject.instance_method()

    def test_fails_when_called_three_times(self):
        subject = InstanceDouble('doubles.testing.User')

        allow(subject).instance_method.twice()

        subject.instance_method()
        subject.instance_method()
        with raises(MockExpectationError) as e:
            subject.instance_method()
        teardown()

        assert re.match(
            r"Allowed 'instance_method' to be called 2 times but was called 3 times on "
            r"<InstanceDouble of <class 'doubles.testing.User'> object at .+> "
            r"with any args, but was not."
            r" \(.*doubles/test/allow_test.py:\d+\)",
            e.value.message
        )


class TestOnce(object):
    def test_passes_when_called_once(self):
        subject = InstanceDouble('doubles.testing.User')

        allow(subject).instance_method.once()

        subject.instance_method()

    def test_fails_when_called_two_times(self):
        subject = InstanceDouble('doubles.testing.User')

        allow(subject).instance_method.once()

        subject.instance_method()
        with raises(MockExpectationError) as e:
            subject.instance_method()
        teardown()

        assert re.match(
            r"Allowed 'instance_method' to be called 1 time but was called 2 times on "
            r"<InstanceDouble of <class 'doubles.testing.User'> object at .+> "
            r"with any args, but was not."
            r" \(.*doubles/test/allow_test.py:\d+\)",
            e.value.message
        )


class TestExactly(object):
    def test_calls_are_chainable(self):
        subject = InstanceDouble('doubles.testing.User')

        allow(subject).instance_method.exactly(1).times.exactly(2).times

        subject.instance_method()
        subject.instance_method()

    def test_passes_when_called_less_than_expected_times(self):
        subject = InstanceDouble('doubles.testing.User')

        allow(subject).instance_method.exactly(2).times

        subject.instance_method()

    def test_passes_when_called_exactly_expected_times(self):
        subject = InstanceDouble('doubles.testing.User')

        allow(subject).instance_method.exactly(1).times

        subject.instance_method()

    def test_fails_when_called_more_than_expected_times(self):
        subject = InstanceDouble('doubles.testing.User')

        allow(subject).instance_method.exactly(1).times

        subject.instance_method()
        with raises(MockExpectationError) as e:
            subject.instance_method()
        teardown()

        assert re.match(
            r"Allowed 'instance_method' to be called 1 time but was called 2 times on "
            r"<InstanceDouble of <class 'doubles.testing.User'> object at .+> "
            r"with any args, but was not."
            r" \(.*doubles/test/allow_test.py:\d+\)",
            e.value.message
        )


class TestAtLeast(object):
    def test_calls_are_chainable(self):
        subject = InstanceDouble('doubles.testing.User')

        allow(subject).instance_method.at_least(2).times.at_least(1).times

        subject.instance_method()

    def test_passes_when_called_less_than_at_least_times(self):
        subject = InstanceDouble('doubles.testing.User')

        allow(subject).instance_method.at_least(2).times

        subject.instance_method()

    def test_passes_when_called_exactly_at_least_times(self):
        subject = InstanceDouble('doubles.testing.User')

        allow(subject).instance_method.at_least(1).times

        subject.instance_method()
        subject.instance_method()

    def test_passes_when_called_more_than_at_least_times(self):
        subject = InstanceDouble('doubles.testing.User')

        allow(subject).instance_method.at_least(1).times

        subject.instance_method()
        subject.instance_method()


class TestAtMost(object):
    def test_calls_are_chainable(self):
        subject = InstanceDouble('doubles.testing.User')

        allow(subject).instance_method.at_most(1).times.at_most(2).times

        subject.instance_method()
        subject.instance_method()

    def test_passes_when_called_exactly_at_most_times(self):
        subject = InstanceDouble('doubles.testing.User')

        allow(subject).instance_method.at_most(1).times

        subject.instance_method()

    def test_passes_when_called_less_than_at_most_times(self):
        subject = InstanceDouble('doubles.testing.User')

        allow(subject).instance_method.at_most(2).times

        subject.instance_method()

    def test_fails_when_called_more_than_at_most_times(self):
        subject = InstanceDouble('doubles.testing.User')

        allow(subject).instance_method.at_most(1).times

        subject.instance_method()
        with raises(MockExpectationError) as e:
            subject.instance_method()
        teardown()

        assert re.match(
            r"Allowed 'instance_method' to be called at most 1 time but was called 2 times on "
            r"<InstanceDouble of <class 'doubles.testing.User'> object at .+> "
            r"with any args, but was not."
            r" \(.*doubles/test/allow_test.py:\d+\)",
            e.value.message
        )
