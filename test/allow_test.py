import inspect
import re
import sys

import pytest
from pytest import raises

from doubles.exceptions import (
    UnallowedMethodCallError,
    MockExpectationError,
    VerifyingDoubleArgumentError
)
from doubles.instance_double import InstanceDouble
from doubles import allow, no_builtin_verification
from doubles.lifecycle import teardown
from doubles.testing import AlwaysEquals, NeverEquals


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

    def test_raises_if_called_with_args_that_do_not_match_signature(self):
        subject = InstanceDouble('doubles.testing.User')
        allow(subject).instance_method

        with raises(VerifyingDoubleArgumentError):
            subject.instance_method('bar')

    def test_skip_builtin_verification_does_not_affect_non_builtins(self):
        with no_builtin_verification():
            subject = InstanceDouble('doubles.testing.User')
            allow(subject).instance_method

            with raises(VerifyingDoubleArgumentError):
                subject.instance_method('bar')

    def test_objects_with_custom__eq__method_one(self):
        subject = InstanceDouble('doubles.testing.User')
        allow(subject).method_with_positional_arguments.with_args(NeverEquals())

        subject.method_with_positional_arguments(AlwaysEquals())

    def test_objects_with_custom__eq__method_two(self):
        subject = InstanceDouble('doubles.testing.User')
        allow(subject).method_with_positional_arguments.with_args(AlwaysEquals())

        subject.method_with_positional_arguments(NeverEquals())

    def test_proxies_docstring(self):
        subject = InstanceDouble('doubles.testing.User')

        allow(subject).method_with_doc

        assert subject.method_with_doc.__doc__ == (
            """A basic method of OldStyleUser to illustrate existence of a docstring"""
        )

    def test_proxies_name(self):
        subject = InstanceDouble('doubles.testing.User')

        allow(subject).method_with_doc

        assert subject.method_with_doc.__name__ == "method_with_doc"

    @pytest.mark.skipif(sys.version_info <= (3, 3), reason="requires Python 3.3 or higher")
    def test_proxies_can_be_inspected(self):
        subject = InstanceDouble("doubles.testing.User")
        allow(subject).instance_method
        parameters = inspect.signature(subject.instance_method).parameters
        assert len(parameters) == 1


class TestWithArgs(object):
    def test__call__is_short_hand_for_with_args(self):
        subject = InstanceDouble('doubles.testing.User')

        allow(subject).method_with_positional_arguments('Bob').and_return('Barker')
        assert subject.method_with_positional_arguments('Bob') == 'Barker'

    def test_allows_any_arguments_if_none_are_specified(self):
        subject = InstanceDouble('doubles.testing.User')

        allow(subject).method_with_positional_arguments.and_return('bar')

        assert subject.method_with_positional_arguments('unspecified argument') == 'bar'

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
            r"(?: at 0x[0-9a-f]{9})?> object at .+>\."
            r"  The supplied arguments \(\)"
            r" do not match any available allowances.",
            str(e.value)
        )

    def test_raises_if_arguments_were_specified_but_wrong_kwarg_used_when_called(self):
        subject = InstanceDouble('doubles.testing.User')

        allow(subject).method_with_default_args.with_args('one', bar='two')

        with raises(UnallowedMethodCallError) as e:
            subject.method_with_default_args('one', bob='barker')

        assert re.match(
            r"Received unexpected call to 'method_with_default_args' on "
            r"<InstanceDouble of <class '?doubles.testing.User'?"
            r"(?: at 0x[0-9a-f]{9})?> object at .+>\."
            r"  The supplied arguments \('one', bob='barker'\)"
            r" do not match any available allowances.",
            str(e.value)
        )

    def test_raises_if_method_is_called_with_wrong_arguments(self):
        subject = InstanceDouble('doubles.testing.User')

        allow(subject).method_with_varargs.with_args('bar')

        with raises(UnallowedMethodCallError) as e:
            subject.method_with_varargs('baz')

        assert re.match(
            r"Received unexpected call to 'method_with_varargs' on "
            r"<InstanceDouble of <class '?doubles.testing.User'?"
            r"(?: at 0x[0-9a-f]{9})?> object at .+>\."
            r"  The supplied arguments \('baz'\)"
            r" do not match any available allowances.",
            str(e.value)
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
            r"(?: at 0x[0-9a-f]{9})?> object at .+>\."
            r"  The supplied arguments \('bar'\)"
            r" do not match any available allowances.",
            str(e.value)
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

    def test_fails_when_called_three_times(self):
        subject = InstanceDouble('doubles.testing.User')

        allow(subject).instance_method.twice()

        subject.instance_method()
        subject.instance_method()
        with raises(MockExpectationError) as e:
            subject.instance_method()
        teardown()

        assert re.match(
            r"Allowed 'instance_method' to be called 2 times instead of 3 times on "
            r"<InstanceDouble of <class 'doubles.testing.User'> object at .+> "
            r"with any args, but was not."
            r" \(.*doubles/test/allow_test.py:\d+\)",
            str(e.value)
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
            r"Allowed 'instance_method' to be called 1 time instead of 2 times on "
            r"<InstanceDouble of <class 'doubles.testing.User'> object at .+> "
            r"with any args, but was not."
            r" \(.*doubles/test/allow_test.py:\d+\)",
            str(e.value)
        )


class TestZeroTimes(object):
    def test_passes_when_called_never(self):
        subject = InstanceDouble('doubles.testing.User')

        allow(subject).instance_method.never()

    def test_fails_when_called_once_times(self):
        subject = InstanceDouble('doubles.testing.User')

        allow(subject).instance_method.never()

        with raises(MockExpectationError) as e:
            subject.instance_method()
        teardown()

        assert re.match(
            r"Allowed 'instance_method' to be called 0 times instead of 1 "
            r"time on <InstanceDouble of <class 'doubles.testing.User'> "
            r"object at .+> with any args, but was not."
            r" \(.*doubles/test/allow_test.py:\d+\)",
            str(e.value)
        )


class TestExactly(object):
    def test_raises_if_called_with_negative_value(self):
        subject = InstanceDouble('doubles.testing.User')

        with raises(TypeError) as e:
            allow(subject).instance_method.exactly(-1).times
        teardown()

        assert re.match(
            r"exactly requires one positive integer argument",
            str(e.value)
        )

    def test_called_with_zero(self):
        subject = InstanceDouble('doubles.testing.User')

        allow(subject).instance_method.exactly(0).times

        with raises(MockExpectationError) as e:
            subject.instance_method()
        teardown()

        assert re.match(
            r"Allowed 'instance_method' to be called 0 times instead of 1 "
            r"time on <InstanceDouble of <class 'doubles.testing.User'> "
            r"object at .+> with any args, but was not."
            r" \(.*doubles/test/allow_test.py:\d+\)",
            str(e.value)
        )

    def test_calls_are_chainable(self):
        subject = InstanceDouble('doubles.testing.User')

        allow(subject).instance_method.exactly(1).time.exactly(2).times

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
            r"Allowed 'instance_method' to be called 1 time instead of 2 times on "
            r"<InstanceDouble of <class 'doubles.testing.User'> object at .+> "
            r"with any args, but was not."
            r" \(.*doubles/test/allow_test.py:\d+\)",
            str(e.value)
        )


class TestAtLeast(object):
    def test_raises_if_called_with_negative_value(self):
        subject = InstanceDouble('doubles.testing.User')

        with raises(TypeError) as e:
            allow(subject).instance_method.at_least(-1).times
        teardown()

        assert re.match(
            r"at_least requires one positive integer argument",
            str(e.value)
        )

    def test_if_called_with_zero(self):
        subject = InstanceDouble('doubles.testing.User')

        allow(subject).instance_method.at_least(0).times

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
    def test_raises_if_called_with_negative_value(self):
        subject = InstanceDouble('doubles.testing.User')

        with raises(TypeError) as e:
            allow(subject).instance_method.at_most(-1).times
        teardown()

        assert re.match(
            r"at_most requires one positive integer argument",
            str(e.value)
        )

    def test_called_with_zero(self):
        subject = InstanceDouble('doubles.testing.User')

        allow(subject).instance_method.at_most(0).times

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
            r"Allowed 'instance_method' to be called at most 1 time instead of 2 times on "
            r"<InstanceDouble of <class 'doubles.testing.User'> object at .+> "
            r"with any args, but was not."
            r" \(.*doubles/test/allow_test.py:\d+\)",
            str(e.value)
        )


class TestCustomMatcher(object):
    def setup(self):
        self.subject = InstanceDouble('doubles.testing.User')

    def test_matcher_raises_an_exception(self):
        def func():
            raise Exception('Bob Barker')

        allow(self.subject).instance_method.with_args_validator(func)
        with raises(UnallowedMethodCallError):
            self.subject.instance_method()

    def test_matcher_with_no_args_returns_true(self):
        allow(self.subject).instance_method.with_args_validator(lambda: True).and_return('Bob')
        self.subject.instance_method() == 'Bob'

    def test_matcher_with_no_args_returns_false(self):
        allow(self.subject).instance_method.with_args_validator(lambda: False)
        with raises(UnallowedMethodCallError):
            self.subject.instance_method()

    def test_matcher_with_positional_args_returns_true(self):
        (allow(self.subject)
            .method_with_positional_arguments
            .with_args_validator(lambda x: True)
            .and_return('Bob'))
        self.subject.method_with_positional_arguments('Bob Barker') == 'Bob'

    def test_matcher_with_positional_args_returns_false(self):
        allow(self.subject).method_with_positional_arguments.with_args_validator(lambda x: False)
        with raises(UnallowedMethodCallError):
            self.subject.method_with_positional_arguments('Bob Barker')

    def test_matcher_with_kwargs_args_returns_false(self):
        def func(bar=None):
            return False
        allow(self.subject).instance_method.with_args_validator(func)
        with raises(UnallowedMethodCallError):
            self.subject.instance_method()

    def test_matcher_with_kwargs_args_returns_true(self):
        def func(bar=None):
            return True
        allow(self.subject).instance_method.with_args_validator(func).and_return('Bob')
        self.subject.instance_method() == 'Bob'

    def test_matcher_with_positional_and_kwargs_returns_true(self):
        def func(foo, bar=None):
            return True
        allow(self.subject).method_with_default_args.with_args_validator(func).and_return('Bob')
        self.subject.method_with_default_args('bob', bar='Barker') == 'Bob'

    def test_matcher_with_positional_and_kwargs_returns_false(self):
        def func(foo, bar=None):
            return False
        allow(self.subject).method_with_default_args.with_args_validator(func).and_return('Bob')
        with raises(UnallowedMethodCallError):
            self.subject.method_with_default_args('bob', bar='Barker')

    def test_matcher_returns_true_but_args_do_not_match_call_signature(self):
        allow(self.subject).instance_method.with_args_validator(lambda x: True)
        with raises(VerifyingDoubleArgumentError):
            self.subject.instance_method('bob')


class TestAsync(object):
    def setup(self):
        self.subject = InstanceDouble('doubles.testing.User')

    def test_and_return_future(self):
        allow(self.subject).instance_method.and_return_future('Bob Barker')

        result = self.subject.instance_method()
        assert result.result() == 'Bob Barker'

    def test_and_return_future_multiple_values(self):
        allow(self.subject).instance_method.and_return_future('Bob Barker', 'Drew Carey')

        result1 = self.subject.instance_method()
        result2 = self.subject.instance_method()
        assert result1.result() == 'Bob Barker'
        assert result2.result() == 'Drew Carey'

    def test_and_raise_future(self):
        exception = Exception('Bob Barker')
        allow(self.subject).instance_method.and_raise_future(exception)

        result = self.subject.instance_method()
        with raises(Exception) as e:
            result.result()

        assert e.value == exception
