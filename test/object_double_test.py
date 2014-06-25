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

    def method_with_varargs(self, *args):
        pass

    def method_with_default_args(self, foo, bar='baz'):
        pass

    noncallable_attribute = 'not a method'

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

    def test_raises_when_stubbing_noncallable_attributes(self):
        doubled_user = ObjectDouble(user)

        with raises(VerifyingDoubleError):
            allow(doubled_user).to_receive('noncallable_attribute')

    def test_raises_when_specifying_different_arity(self):
        doubled_user = ObjectDouble(user)

        with raises(VerifyingDoubleError):
            allow(doubled_user).to_receive('get_name').with_args('foo', 'bar')

    def test_allows_varargs_if_specified(self):
        doubled_user = ObjectDouble(user)

        allow(doubled_user).to_receive('method_with_varargs').with_args('foo', 'bar', 'baz')

        assert doubled_user.method_with_varargs('foo', 'bar', 'baz') is None

    def test_allows_missing_default_arguments(self):
        doubled_user = ObjectDouble(user)

        allow(doubled_user).to_receive('method_with_default_args').with_args('blah')

        assert doubled_user.method_with_default_args('blah') is None

    def test_allows_default_arguments_specified_positionally(self):
        doubled_user = ObjectDouble(user)

        allow(doubled_user).to_receive('method_with_default_args').with_args('blah', 'blam')

        assert doubled_user.method_with_default_args('blah', 'blam') is None

    def test_allows_default_arguments_specified_with_keywords(self):
        doubled_user = ObjectDouble(user)

        allow(doubled_user).to_receive('method_with_default_args').with_args('blah', bar='blam')

        assert doubled_user.method_with_default_args('blah', bar='blam') is None
