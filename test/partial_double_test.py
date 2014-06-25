from pytest import raises

from doubles import allow, Double, teardown


class User(object):
    class_attribute = 'foo'

    def __init__(self, name, age):
        self.name = name
        self._age = age

    @property
    def age(self):
        return self._age

    @classmethod
    def get_first(self):
        return 'First user'

    def get_name(self):
        return self.name


class TestInstanceMethods(object):
    def test_stubs_instance_methods(self):
        user = User('Alice', 25)

        allow(user).to_receive('get_name').and_return('Bob')

        assert user.get_name() == 'Bob'

    def test_restores_instance_methods_on_teardown(self):
        user = User('Alice', 25)
        allow(user).to_receive('get_name').and_return('Bob')

        teardown()

        assert user.get_name() == 'Alice'

    def test_only_affects_stubbed_method(self):
        user = User('Alice', 25)

        allow(user).to_receive('get_name').and_return('Bob')

        assert user.age == 25

    def test_stubs_nonexistent_instance_methods(self):
        user = User('Alice', 25)

        allow(user).to_receive('gender').and_return('Female')

        assert user.gender() == 'Female'

    def test_removes_nonexistent_instance_methods_on_teardown(self):
        user = User('Alice', 25)
        allow(user).to_receive('gender').and_return('Female')

        teardown()

        with raises(AttributeError):
            user.gender()


class TestClassMethods(object):
    def test_stubs_constructors(self):
        user = Double('User')

        allow(User).to_receive('__new__').and_return(user)

        assert User('Alice', 25) is user

    def test_restores_constructor_on_teardown(self):
        user = Double('User')
        allow(User).to_receive('__new__').and_return(user)

        teardown()

        assert User('Alice', 25) is not user

    def test_stubs_class_methods(self):
        user = Double('User')

        allow(User).to_receive('get_first').and_return(user)

        assert User.get_first() is user

    def test_restores_class_methods_on_teardown(self):
        user = Double('User')
        allow(User).to_receive('get_first').and_return(user)

        teardown()

        assert User.get_first() == 'First user'

    def test_stubs_class_attributes(self):
        allow(User).to_receive('class_attribute').and_return('bar')

        assert User.class_attribute() == 'bar'

    def test_restores_class_attributes_on_teardown(self):
        allow(User).to_receive('class_attribute').and_return('bar')

        teardown()

        assert User.class_attribute == 'foo'

    def test_stubs_nonexistent_class_methods(self):
        allow(User).to_receive('class_method').and_return('bar')

        assert User.class_method() == 'bar'

    def test_removes_nonexistent_class_methods_on_teardown(self):
        allow(User).to_receive('class_method').and_return('bar')

        teardown()

        with raises(AttributeError):
            User.class_method()
