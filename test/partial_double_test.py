from doubles import Double, allow, teardown
from doubles.exceptions import VerifyingDoubleError
import pytest


class User(object):
    def __init__(self, name, age):
        self.name = name
        self._age = age

    @classmethod
    def get_first(cls):
        return 'First user'

    @property
    def age(self):
        return self._age

    def get_name(self):
        return self.name


class TestPartialDouble(object):
    def test_stubs_real_object(self):
        user = User('Alice', 25)

        allow(user).to_receive('get_name').and_return('Bob')

        assert user.get_name() == 'Bob'

    def test_restores_original(self):
        user = User('Alice', 25)
        allow(user).to_receive('get_name').and_return('Bob')

        teardown()

        assert user.get_name() == 'Alice'

    def test_only_affects_stubbed_method(self):
        user = User('Alice', 25)

        allow(user).to_receive('get_name').and_return('Bob')

        assert user.age == 25

    def test_allows_constructor_to_be_stubbed(self):
        user = Double('User')

        allow(User).to_receive('__new__').and_return(user)

        assert User('Alice', 25) is user

    def test_stubs_class_methods(self):
        user = Double('User')

        allow(User).to_receive('get_first').and_return(user)

        assert User.get_first() is user

    def test_nonexistent_instance_method(self):
        user = User('Alice', 25)

        with pytest.raises(VerifyingDoubleError):
            allow(user).to_receive('nonexistent_method')

    def test_nonexistent_class_method(self):
        with pytest.raises(VerifyingDoubleError):
            allow(User).to_receive('nonexistent_method')
