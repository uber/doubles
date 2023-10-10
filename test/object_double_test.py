import re

from dobles.exceptions import (VerifyingDoubleArgumentError,
                               VerifyingDoubleError)
from dobles.object_double import ObjectDouble
from dobles.targets.allowance_target import allow
from dobles.testing import User
from pytest import raises

user = User('Alice', 25)


class TestRepr(object):

    def test_displays_correct_class_name(self):
        subject = ObjectDouble(user)

        assert re.match(
            r"<ObjectDouble of <dobles.testing.User "
            r"(?:instance|object) at 0x[0-9a-f]+> object "
            r"at 0x[0-9a-f]+>", repr(subject))


class TestObjectDouble(object):

    def test_allows_stubs_on_existing_methods(self):
        doubled_user = ObjectDouble(user)

        allow(doubled_user).get_name.and_return('Bob')

        assert doubled_user.get_name() == 'Bob'

    def test_raises_when_stubbing_nonexistent_methods(self):
        doubled_user = ObjectDouble(user)

        with raises(VerifyingDoubleError) as e:
            allow(doubled_user).foo

        assert re.search(r"does not implement it", str(e.value))

    def test_raises_when_stubbing_noncallable_attributes(self):
        doubled_user = ObjectDouble(user)

        with raises(VerifyingDoubleError) as e:
            allow(doubled_user).class_attribute

        assert re.search(r"not a callable attribute", str(e.value))

    def test_raises_when_specifying_different_arity(self):
        doubled_user = ObjectDouble(user)

        with raises(VerifyingDoubleArgumentError):
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

        allow(doubled_user).method_with_default_args.with_args('blah',
                                                               bar='blam')

        assert doubled_user.method_with_default_args('blah',
                                                     bar='blam') is None

    def test_raises_when_specifying_higher_arity_to_method_with_default_arguments(
            self):  # noqa
        doubled_user = ObjectDouble(user)

        with raises(VerifyingDoubleArgumentError):
            allow(doubled_user).method_with_default_args.with_args(1, 2, 3)

    def test_raises_when_specifying_extra_keyword_arguments(self):
        doubled_user = ObjectDouble(user)

        with raises(VerifyingDoubleArgumentError):
            allow(doubled_user).method_with_default_args.with_args(1,
                                                                   moo='woof')

    def test_allows_varkwargs_if_specified(self):
        doubled_user = ObjectDouble(user)

        allow(doubled_user).method_with_varkwargs.with_args(foo='bar')

        assert doubled_user.method_with_varkwargs(foo='bar') is None

    def test_mocking__call__works(self):
        doubled_user = ObjectDouble(user)

        allow(doubled_user).__call__.and_return('bob barker')

        assert doubled_user() == 'bob barker'

    def test_mocking__enter__and__exit__works(self):
        doubled_user = ObjectDouble(user)

        allow(doubled_user).__enter__.and_return('bob barker')
        # Not ideal to do both in the same test case,
        # but the with block won't execute at all unless both methods are defined.
        allow(doubled_user).__exit__

        with doubled_user as u:
            assert u == 'bob barker'
