from pytest import raises

from doubles.lifecycle import teardown
from doubles.targets.allowance_target import allow
from doubles.testing import User


class TestInstanceMethods(object):
    def test_stubs_instance_methods(self):
        user = User('Alice', 25)

        allow(user).get_name.and_return('Bob')

        assert user.get_name() == 'Bob'

    def test_restores_instance_methods_on_teardown(self):
        user = User('Alice', 25)
        allow(user).get_name.and_return('Bob')

        teardown()

        assert user.get_name() == 'Alice'

    def test_only_affects_stubbed_method(self):
        user = User('Alice', 25)

        allow(user).get_name.and_return('Bob')

        assert user.age == 25

    def test_stubs_nonexistent_instance_methods(self):
        user = User('Alice', 25)

        allow(user).gender.and_return('Female')

        assert user.gender() == 'Female'

    def test_removes_nonexistent_instance_methods_on_teardown(self):
        user = User('Alice', 25)
        allow(user).gender.and_return('Female')

        teardown()

        with raises(AttributeError):
            user.gender()


class TestClassMethods(object):
    def test_stubs_constructors(self):
        user = object()

        allow(User).__new__.and_return(user)

        assert User('Alice', 25) is user

    def test_restores_constructor_on_teardown(self):
        user = object()
        allow(User).__new__.and_return(user)

        teardown()

        assert User('Alice', 25) is not user

    def test_stubs_class_methods(self):
        allow(User).class_method.and_return('overridden value')

        assert User.class_method() == 'overridden value'

    def test_restores_class_methods_on_teardown(self):
        allow(User).class_method.and_return('overridden value')

        teardown()

        assert User.class_method() == 'class method'

    def test_stubs_class_attributes(self):
        allow(User).class_attribute.and_return('bar')

        assert User.class_attribute() == 'bar'

    def test_restores_class_attributes_on_teardown(self):
        allow(User).class_attribute.and_return('bar')

        teardown()

        assert User.class_attribute == 'foo'

    def test_stubs_nonexistent_class_methods(self):
        allow(User).nonexistent_method.and_return('bar')

        assert User.nonexistent_method() == 'bar'

    def test_removes_nonexistent_class_methods_on_teardown(self):
        allow(User).nonexistent_method.and_return('bar')

        teardown()

        with raises(AttributeError):
            User.nonexistent_method()
