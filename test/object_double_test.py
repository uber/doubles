from pytest import raises

from doubles import allow, ObjectDouble
from doubles.exceptions import VerifyingDoubleError


class User(object):
    def __init__(self, name, age):
        self.name = name
        self._age = age

    @property
    def age(self):
        return self._age

    def get_name(self):
        return self.name

user = User('Alice', 25)


class TestObjectDouble(object):
    def test_allows_stubs_on_existing_methods(self):
        doubled_user = ObjectDouble(user)

        allow(doubled_user).to_receive('get_name').and_return('Bob')

        assert doubled_user.get_name() == 'Bob'

    def test_raises_when_stubbing_nonexistent_methods(self):
        doubled_user = ObjectDouble(user)

        with raises(VerifyingDoubleError):
            allow(doubled_user).to_receive('foo')
