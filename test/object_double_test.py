import re

from pytest import raises

from doubles.exceptions import VerifyingDoubleError
from doubles.object_double import ObjectDouble
from doubles.targets.allowance_target import allow
from doubles.testing import User

user = User('Alice', 25)


class TestRepr(object):
    def test_displays_correct_class_name(self):
        subject = ObjectDouble(user)

        assert re.match(
            r"<ObjectDouble of <doubles.testing.User object at 0x[0-9a-f]{9}> object "
            r"at 0x[0-9a-f]{9}>",
            repr(subject)
        )


class TestObjectDouble(object):
    def test_allows_stubs_on_existing_methods(self):
        doubled_user = ObjectDouble(user)

        allow(doubled_user).get_name.and_return('Bob')

        assert doubled_user.get_name() == 'Bob'

    def test_raises_when_stubbing_nonexistent_methods(self):
        doubled_user = ObjectDouble(user)

        with raises(VerifyingDoubleError):
            allow(doubled_user).foo

    def test_raises_when_stubbing_noncallable_attributes(self):
        doubled_user = ObjectDouble(user)

        with raises(VerifyingDoubleError):
            allow(doubled_user).class_attribute

    def test_raises_when_specifying_different_arity(self):
        doubled_user = ObjectDouble(user)

        with raises(VerifyingDoubleError):
            allow(doubled_user).get_name.with_args('foo', 'bar')

    def test_allows_varargs_if_specified(self):
        doubled_user = ObjectDouble(user)

        allow(doubled_user).method_with_varargs.with_args('foo', 'bar', 'baz')

        assert doubled_user.method_with_varargs('foo', 'bar', 'baz') is None

    def test_allows_missing_default_arguments(self):
        doubled_user = ObjectDouble(user)

        allow(doubled_user).method_with_default_args.with_args('blah')

        assert doubled_user.method_with_default_args('blah') is None

    def test_allows_default_arguments_specified_positionally(self):
        doubled_user = ObjectDouble(user)

        allow(doubled_user).method_with_default_args.with_args('blah', 'blam')

        assert doubled_user.method_with_default_args('blah', 'blam') is None

    def test_allows_default_arguments_specified_with_keywords(self):
        doubled_user = ObjectDouble(user)

        allow(doubled_user).method_with_default_args.with_args('blah', bar='blam')

        assert doubled_user.method_with_default_args('blah', bar='blam') is None

    def test_raises_when_specifying_higher_arity_to_method_with_default_arguments(self):
        doubled_user = ObjectDouble(user)

        with raises(VerifyingDoubleError):
            allow(doubled_user).method_with_default_args.with_args(1, 2, 3)

    def test_raises_when_specifying_extra_keyword_arguments(self):
        doubled_user = ObjectDouble(user)

        with raises(VerifyingDoubleError):
            allow(doubled_user).method_with_default_args.with_args(1, moo='woof')

    def test_allows_varkwargs_if_specified(self):
        doubled_user = ObjectDouble(user)

        allow(doubled_user).method_with_varkwargs.with_args(foo='bar')

        assert doubled_user.method_with_varkwargs(foo='bar') is None
