from pytest import raises

from doubles import allow, InstanceDouble, no_builtin_verification
from doubles.exceptions import (
    VerifyingDoubleArgumentError,
    VerifyingDoubleError,
    VerifyingDoubleImportError
)


class TestInstanceDouble(object):
    def test_allows_stubs_on_existing_methods(self):
        with no_builtin_verification():
            date = InstanceDouble('datetime.date')

            allow(date).ctime

            assert date.ctime() is None

    def test_raises_when_stubbing_nonexistent_methods(self):
        date = InstanceDouble('datetime.date')

        with raises(VerifyingDoubleError):
            allow(date).nonexistent_method

    def test_raises_when_stubbing_noncallable_attributes(self):
        date = InstanceDouble('datetime.date')

        with raises(VerifyingDoubleError):
            allow(date).year

    def test_raises_when_argspec_does_not_match(self):
        date = InstanceDouble('datetime.date')

        with raises(VerifyingDoubleArgumentError):
            allow(date).ctime.with_args('foo')

    def test_allows_stubs_on_existing_class_methods(self):
        with no_builtin_verification():
            date = InstanceDouble('datetime.date')

            allow(date).today.with_args()

            assert date.today() is None

    def test_raises_when_target_is_a_top_level_module(self):
        with raises(VerifyingDoubleImportError) as e:
            InstanceDouble('foo')

        assert str(e.value) == 'Invalid import path: foo.'

    def test_raises_on_import_error(self):
        with raises(VerifyingDoubleImportError) as e:
            InstanceDouble('foo.bar')

        assert str(e.value) == 'Cannot import object from path: foo.bar.'

    def test_raises_when_importing_a_non_class_object(self):
        with raises(VerifyingDoubleImportError) as e:
            InstanceDouble('unittest.signals')

        assert str(e.value) == 'Path does not point to a class: unittest.signals.'

    def test_raises_when_class_does_not_exist_in_module(self):
        with raises(VerifyingDoubleImportError) as e:
            InstanceDouble('unittest.foo')

        assert str(e.value) == 'No object at path: unittest.foo.'

    def test_mocking__call__works(self):
        user = InstanceDouble('doubles.testing.User')
        allow(user).__call__.and_return('bob barker')
        assert user() == 'bob barker'

    def test_mocking__enter__and__exit__works(self):
        user = InstanceDouble('doubles.testing.User')
        allow(user).__enter__.and_return('bob barker')
        allow(user).__exit__

        with user as u:
            assert u == 'bob barker'

    def test_passing_kwargs_assings_them_as_attrs(self):
        user = InstanceDouble('doubles.testing.User', name='Bob Barker')

        assert user.name == 'Bob Barker'

    def test_class_with__getattr__(self):
        test_obj = InstanceDouble('doubles.testing.ClassWithGetAttr')
        allow(test_obj).method.and_return('bob barker')
        assert test_obj.method() == 'bob barker'
