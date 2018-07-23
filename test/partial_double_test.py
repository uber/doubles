from pytest import raises, mark

from doubles.exceptions import (
    VerifyingDoubleError,
    VerifyingDoubleArgumentError,
    UnallowedMethodCallError,
)
from doubles.lifecycle import teardown
from doubles import allow, no_builtin_verification
from doubles.testing import User, OldStyleUser, UserWithCustomNew
import doubles.testing


@mark.parametrize('test_class', [User, OldStyleUser])
class TestInstanceMethods(object):
    def test_arbitrary_callable_on_instance(self, test_class):
        instance = test_class('Bob', 10)
        allow(instance).arbitrary_callable.and_return('Bob Barker')
        assert instance.arbitrary_callable() == 'Bob Barker'
        teardown()
        assert instance.arbitrary_callable() == 'ArbitraryCallable Value'

    def test_arbitrary_callable_on_class(self, test_class):
        allow(test_class).arbitrary_callable.and_return('Bob Barker')
        assert test_class.arbitrary_callable() == 'Bob Barker'
        teardown()
        assert test_class.arbitrary_callable() == 'ArbitraryCallable Value'

    def test_callable_class_attribute(self, test_class):
        allow(test_class).callable_class_attribute.and_return('Bob Barker')
        assert test_class.callable_class_attribute() == 'Bob Barker'
        teardown()
        assert test_class.callable_class_attribute() == 'dummy result'

    def test_callable_instance_attribute(self, test_class):
        user = test_class('Alice', 25)
        allow(user).callable_instance_attribute.and_return('Bob Barker')

        assert user.callable_instance_attribute() == 'Bob Barker'
        teardown()
        assert user.callable_instance_attribute() == 'dummy result'

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

        assert str(e.value) == 'Properties do not accept arguments.'

    def test_calling_stubbed_property_with_args_works(self, test_class):
        user = test_class('Alice', 25)
        allow(user).some_property.and_return(lambda x: x)

        assert user.some_property('bob') == 'bob'

    def test_stubbing_properties_on_multiple_instances(self, test_class):
        user_1 = test_class('Bob', 25)
        user_2 = test_class('Drew', 25)

        allow(user_1).some_property.and_return('Barker')
        allow(user_2).some_property.and_return('Carey')

        assert user_1.some_property == 'Barker'
        assert user_2.some_property == 'Carey'

    def test_stubbing_property_does_not_affect_other_instances(self, test_class):
        user_1 = test_class('Bob', 25)
        user_2 = test_class('Drew', 25)

        allow(user_1).some_property.and_return('Barker')

        assert user_1.some_property == 'Barker'
        assert user_2.some_property == 'some_property return value'

    def test_teardown_restores_properties(self, test_class):
        user_1 = test_class('Bob', 25)
        user_2 = test_class('Drew', 25)

        allow(user_1).some_property.and_return('Barker')
        allow(user_2).some_property.and_return('Carey')

        teardown()

        assert user_1.some_property == 'some_property return value'
        assert user_2.some_property == 'some_property return value'


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
class Test__enter__(object):
    def test_basic_usage(self, test_class):
        user = test_class('Alice', 25)
        allow(user).__enter__.and_return(user)

        with user as u:
            assert user == u

    def test_stubbing_two_objects_does_not_interfere(self, test_class):
        alice = test_class('Alice', 25)
        bob = test_class('Bob', 25)

        allow(alice).__enter__.and_return('alice')
        allow(bob).__enter__.and_return('bob')

        with alice as a:
            assert a == 'alice'

        with bob as b:
            assert b == 'bob'

    def test_does_not_intefere_with_unstubbed_objects(self, test_class):
        alice = test_class('Alice', 25)
        bob = test_class('Bob', 25)

        allow(alice).__enter__.and_return('user')

        with alice as a:
            assert a == 'user'

        with bob as b:
            assert b == bob

    def test_teardown_restores_previous_functionality(self, test_class):
        user = test_class('Alice', 25)
        allow(user).__enter__.and_return('bob barker')

        with user as u:
            assert u == 'bob barker'

        teardown()

        with user as u:
            assert u == user

    def test_raises_when_mocked_with_invalid_call_signature(self, test_class):
        user = test_class('Alice', 25)
        with raises(VerifyingDoubleArgumentError):
            allow(user).__enter__.with_args(1)


@mark.parametrize('test_class', [User, OldStyleUser])
class Test__exit__(object):
    def test_basic_usage(self, test_class):
        user = test_class('Alice', 25)
        allow(user).__exit__.with_args(None, None, None)

        with user:
            pass

    def test_stubbing_two_objects_does_not_interfere(self, test_class):
        alice = test_class('Alice', 25)
        bob = test_class('Bob', 25)

        allow(alice).__exit__.and_return('alice')
        allow(bob).__exit__.and_return('bob')

        assert alice.__exit__(None, None, None) == 'alice'
        assert bob.__exit__(None, None, None) == 'bob'

    def test_does_not_intefere_with_unstubbed_objects(self, test_class):
        alice = test_class('Alice', 25)
        bob = test_class('Bob', 25)

        allow(alice).__exit__.and_return('user')

        assert alice.__exit__(None, None, None) == 'user'
        assert bob.__exit__(None, None, None) is None

    def test_teardown_restores_previous_functionality(self, test_class):
        user = test_class('Alice', 25)
        allow(user).__exit__.and_return('bob barker')

        assert user.__exit__(None, None, None) == 'bob barker'

        teardown()

        assert user.__exit__(None, None, None) is None

    def test_raises_when_mocked_with_invalid_call_signature(self, test_class):
        user = test_class('Alice', 25)
        with raises(VerifyingDoubleArgumentError):
            allow(user).__exit__.with_no_args()


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


class TestBuiltInConstructorMethods(object):
    def test_stubs_constructors(self):
        with no_builtin_verification():
            user = object()

            allow(User).__new__.and_return(user)

            assert User('Alice', 25) is user

    def test_restores_constructor_on_teardown(self):
        user = object()
        allow(User).__new__.and_return(user)

        teardown()

        result = User('Alice', 25)

        assert result is not user
        assert result.name == 'Alice'


class TestCustomConstructorMethods(object):
    def test_stubs_constructors(self):
        with no_builtin_verification():
            user = object()

            allow(UserWithCustomNew).__new__.and_return(user)

            assert UserWithCustomNew('Alice', 25) is user

    def test_restores_constructor_on_teardown(self):
        user = object()
        allow(UserWithCustomNew).__new__.and_return(user)

        teardown()

        result = UserWithCustomNew('Alice', 25)

        assert result is not user
        assert result.name_set_in__new__ == 'Alice'
        assert result.name == 'Alice'


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

    def test_callable_top_level_variable(self):
        allow(doubles.testing).callable_variable.and_return('foo')

        assert doubles.testing.callable_variable('bob barker') == 'foo'

    def test_decorated_function(self):
        allow(doubles.testing).decorated_function_callable.and_return('foo')

        assert doubles.testing.decorated_function_callable('bob barker') == 'foo'

    def test_decorated_function_that_returns_a_callable(self):
        allow(doubles.testing).decorated_function.and_return('foo')

        assert doubles.testing.decorated_function('bob barker') == 'foo'

    def test_variable_that_points_to_class_method(self):
        allow(doubles.testing).class_method.and_return('foo')

        assert doubles.testing.class_method('bob barker') == 'foo'

    def test_variable_that_points_to_instance_method(self):
        allow(doubles.testing).instance_method.and_return('foo')

        assert doubles.testing.instance_method() == 'foo'


class TestClassWithGetAttr(object):
    def test_can_allow_an_existing_method(self):
        test_obj = doubles.testing.ClassWithGetAttr()
        allow(test_obj).method.and_return('foobar')

        assert test_obj.method() == 'foobar'

    def test_raises_if_method_does_not_exist(self):
        test_obj = doubles.testing.ClassWithGetAttr()

        with raises(VerifyingDoubleError):
            allow(test_obj).fake_function
