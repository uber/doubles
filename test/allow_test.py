from pytest import raises

from doubles import allow, Double
from doubles.exceptions import UnallowedMethodCallError


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

    def test_allows_any_arguments_if_none_are_specified(self):
        subject = Double()

        allow(subject).to_receive('foo').and_return('bar')

        assert subject.foo('unspecified argument') == 'bar'

    def test_allows_specification_of_arguments(self):
        subject = Double()

        allow(subject).to_receive('foo').with_args('bar', baz='blah')

        assert subject.foo('bar', baz='blah') is None

    def test_raises_if_arguments_were_specified_but_not_provided_when_called(self):
        subject = Double()

        allow(subject).to_receive('foo').with_args('bar', baz='blah')

        with raises(UnallowedMethodCallError):
            subject.foo()

    def test_matches_most_specific_allowance(self):
        subject = Double()

        allow(subject).to_receive('foo').and_return('bar')
        allow(subject).to_receive('foo').with_args('baz').and_return('blah')

        assert subject.foo('baz') == 'blah'

    def test_returns_result_of_a_callable(self):
        subject = Double()

        allow(subject).to_receive('foo').and_return_result_of(lambda: 'bar')

        assert subject.foo() == 'bar'

    def test_returns_result_of_callable_if_specified_after_regular_return(self):
        subject = Double()

        allow(subject).to_receive('foo').and_return('bar').and_return_result_of(lambda: 'baz')

        assert subject.foo() == 'baz'

    def test_returns_static_value_if_specified_after_callable_return_value(self):
        subject = Double()

        allow(subject).to_receive('foo').and_return_result_of(lambda: 'bar').and_return('baz')

        assert subject.foo() == 'baz'
