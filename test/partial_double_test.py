from pytest import raises, mark

from doubles.exceptions import VerifyingDoubleError
from doubles.lifecycle import teardown
from doubles.targets.allowance_target import allow
from doubles.testing import User, OldStyleUser


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
        user = object()

        allow(User).__new__.and_return(user)

        assert User('Alice', 25) is user

    def test_restores_constructor_on_teardown(self):
        user = object()
        allow(User).__new__.and_return(user)

        teardown()

        assert User('Alice', 25) is not user
