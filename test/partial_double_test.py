from pytest import raises, mark

from doubles.exceptions import (
    VerifyingDoubleError,
    VerifyingDoubleArgumentError,
    UnallowedMethodCallError,
)
from doubles.lifecycle import teardown
from doubles import allow, no_builtin_verification
from doubles.testing import User, OldStyleUser
import doubles.testing


@mark.parametrize('test_class', [User, OldStyleUser])
class TestInstanceMethods(object):
    def test_stubs_instance_methods(self, test_class):
        user = test_class('Alice', 25)

        allow(user).get_name.and_return('Bob')

        assert user.get_name() == 'Bob'

    def test_restores_instance_methods_on_teardown(self, test_class):
        user = test_class('Alice', 25)
        allow(user).get_name.and_return('Bob')

        teardown()

        assert user.get_name() == 'Alice'

    def test_only_affects_stubbed_method(self, test_class):
        user = test_class('Alice', 25)

        allow(user).get_name.and_return('Bob')

        assert user.age == 25

    def test_raises_when_stubbing_nonexistent_methods(self, test_class):
        user = test_class('Alice', 25)

        with raises(VerifyingDoubleError):
            allow(user).gender

    def test_stubs_properties(self, test_class):
        user = test_class('Alice', 25)

        allow(user).some_property.and_return('foo')

        assert user.some_property == 'foo'

    def test_stubing_property_with_args_raises(self, test_class):
        user = test_class('Alice', 25)

        with raises(VerifyingDoubleArgumentError) as e:
            allow(user).some_property.with_args(1)

        assert e.value.message == 'Properties do not accept arguments.'

    def test_calling_stubbed_property_with_args_works(self, test_class):
        user = test_class('Alice', 25)
        allow(user).some_property.and_return(lambda x: x)

        assert user.some_property('bob') == 'bob'


@mark.parametrize('test_class', [User, OldStyleUser])
class Test__call__(object):
    def test_basic_usage(self, test_class):
        user = test_class('Alice', 25)
        allow(user).__call__.and_return('bob barker')

        assert user() == 'bob barker'

    def test_stubbing_two_objects_does_not_interfere(self, test_class):
        alice = test_class('Alice', 25)
        peter = test_class('Peter', 25)

        allow(alice).__call__.and_return('alice')
        allow(peter).__call__.and_return('peter')

        assert alice() == 'alice'
        assert peter() == 'peter'

    def test_does_not_intefere_with_unstubbed_objects(self, test_class):
        alice = test_class('Alice', 25)
        peter = test_class('Peter', 25)

        allow(alice).__call__.and_return('alice')

        assert alice() == 'alice'
        assert peter() == 'user was called'

    def test_teardown_restores_previous_functionality(self, test_class):
        user = test_class('Alice', 25)
        allow(user).__call__.and_return('bob barker')

        assert user() == 'bob barker'

        teardown()

        assert user() == 'user was called'

    def test_works_with_arguments(self, test_class):
        user = test_class('Alice', 25)
        allow(user).__call__.with_args(1, 2).and_return('bob barker')

        assert user(1, 2) == 'bob barker'

    def test_raises_when_called_with_invalid_args(self, test_class):
        user = test_class('Alice', 25)
        allow(user).__call__.with_args(1, 2).and_return('bob barker')

        with raises(UnallowedMethodCallError):
            user(1, 2, 3)

    def test_raises_when_mocked_with_invalid_call_signature(self, test_class):
        user = test_class('Alice', 25)
        with raises(VerifyingDoubleArgumentError):
            allow(user).__call__.with_args(1, 2, bob='barker')


@mark.parametrize('test_class', [User, OldStyleUser])
class TestClassMethods(object):
    def test_stubs_class_methods(self, test_class):
        allow(test_class).class_method.with_args('foo').and_return('overridden value')

        assert test_class.class_method('foo') == 'overridden value'

    def test_restores_class_methods_on_teardown(self, test_class):
        allow(test_class).class_method.and_return('overridden value')

        teardown()

        assert test_class.class_method('foo') == 'class_method return value: foo'

    def test_raises_when_stubbing_noncallable_attributes(self, test_class):
        with raises(VerifyingDoubleError):
            allow(test_class).class_attribute

    def test_raises_when_stubbing_nonexistent_class_methods(self, test_class):
        with raises(VerifyingDoubleError):
            allow(test_class).nonexistent_method


class TestConstructorMethods(object):
    def test_stubs_constructors(self):
        with no_builtin_verification():
            user = object()

            allow(User).__new__.and_return(user)

            assert User('Alice', 25) is user

    def test_restores_constructor_on_teardown(self):
        user = object()
        allow(User).__new__.and_return(user)

        teardown()

        assert User('Alice', 25) is not user


class TestTopLevelFunctions(object):
    def test_stubs_method(self):
        allow(doubles.testing).top_level_function.and_return('foo')

        assert doubles.testing.top_level_function('bob barker') == 'foo'

    def test_restores_the_orignal_method(self):
        allow(doubles.testing).top_level_function.and_return('foo')
        teardown()
        assert doubles.testing.top_level_function('foo', 'bar') == 'foo -- bar'

    def test_raises_if_incorrect_call_signature_used(self):
        with raises(VerifyingDoubleArgumentError):
            allow(doubles.testing).top_level_function.with_args(
                'bob',
                'barker',
                'is_great'
            )

    def test_allows_correct_call_signature(self):
        allow(doubles.testing).top_level_function.with_args(
            'bob',
            'barker',
        ).and_return('bar')
        assert doubles.testing.top_level_function('bob', 'barker') == 'bar'

    def test_verifies_the_function_exists(self):
        with raises(VerifyingDoubleError):
            allow(doubles.testing).fake_function

    def test_can_be_called_through_dict(self):
        allow(doubles.testing).top_level_function.with_args(
            'charles',
            'barkley'
        ).and_return('baz')

        # accessing the function directly works
        # func = doubles.testing.top_level_function

        # but accessing it through a dict in another module fails
        func = doubles.testing.func_set['top_level_function']

        assert func('charles', 'barkley') == 'baz'
