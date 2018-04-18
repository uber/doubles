from pytest import raises, mark

from doubles.instance_double import InstanceDouble
from doubles import allow, expect
from doubles.lifecycle import teardown


class UserDefinedException(Exception):
    pass


class UserDefinedExceptionWithArgs(Exception):
    def __init__(self, msg, arg1, arg2=None):
        pass


@mark.parametrize('stubber', [allow, expect])
class TestReturnValues(object):
    def test_returns_result_of_a_callable(self, stubber):
        subject = InstanceDouble('doubles.testing.User')

        stubber(subject).instance_method.and_return_result_of(lambda: 'bar')

        assert subject.instance_method() == 'bar'

    def test_returns_result_of_a_callable_with_positional_arg(self, stubber):
        subject = InstanceDouble('doubles.testing.User')

        stubber(subject).method_with_positional_arguments.and_return_result_of(lambda x: x)

        assert subject.method_with_positional_arguments('bar') == 'bar'

    def test_returns_result_of_a_callable_with_positional_vargs(self, stubber):
        subject = InstanceDouble('doubles.testing.User')

        stubber(subject).method_with_varargs.and_return_result_of(lambda *x: x)

        result = subject.method_with_varargs('bob', 'barker')
        assert result == ('bob', 'barker')

    def test_returns_result_of_a_callable_with_varkwargs(self, stubber):
        subject = InstanceDouble('doubles.testing.User')

        stubber(subject).method_with_varkwargs.and_return_result_of(lambda **kwargs: kwargs['bob'])

        assert subject.method_with_varkwargs(bob='barker') == 'barker'

    def test_raises_provided_exception(self, stubber):
        subject = InstanceDouble('doubles.testing.User')

        stubber(subject).instance_method.and_raise(UserDefinedException)

        with raises(UserDefinedException):
            subject.instance_method()

    def test_raises_provided_exception_with_complex_signature(self, stubber):
        subject = InstanceDouble('doubles.testing.User')

        stubber(subject).instance_method.and_raise(
            UserDefinedExceptionWithArgs('msg', 'arg1', arg2='arg2'),
        )

        with raises(UserDefinedExceptionWithArgs):
            subject.instance_method()

    def test_chaining_result_methods_gives_the_last_one_precedence(self, stubber):
        subject = InstanceDouble('doubles.testing.User')

        stubber(subject).instance_method.and_return('bar').and_return_result_of(
            lambda: 'baz'
        ).and_raise(UserDefinedException).and_return('final')

        assert subject.instance_method() == 'final'


@mark.parametrize('stubber', [allow, expect])
class TestAndReturn(object):
    def test_raises_if_no_arguments_supplied(self, stubber):
        subject = InstanceDouble('doubles.testing.User')

        with raises(TypeError) as e:
            stubber(subject).instance_method.and_return()

        assert str(e.value) == 'and_return() expected at least 1 return value'
        teardown()

    def test_returns_specified_value(self, stubber):
        subject = InstanceDouble('doubles.testing.User')

        stubber(subject).instance_method.and_return('bar')

        assert subject.instance_method() == 'bar'

    def test_returns_specified_values_in_order(self, stubber):
        subject = InstanceDouble('doubles.testing.User')

        stubber(subject).instance_method.and_return('bar', 'bazz')

        assert subject.instance_method() == 'bar'
        assert subject.instance_method() == 'bazz'

    def test_returns_the_last_specified_value_multiple_times(self, stubber):
        subject = InstanceDouble('doubles.testing.User')

        stubber(subject).instance_method.and_return('bar', 'bazz')

        assert subject.instance_method() == 'bar'
        assert subject.instance_method() == 'bazz'
        assert subject.instance_method() == 'bazz'

    def test_subsequent_allowances_override_previous_ones(self, stubber):
        subject = InstanceDouble('doubles.testing.User')

        stubber(subject).instance_method.never().and_return('bar')
        stubber(subject).instance_method.and_return('baz')

        assert subject.instance_method() == 'baz'
