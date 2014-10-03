from pytest import raises

from doubles import allow, InstanceDouble
from doubles.exceptions import (
    VerifyingDoubleArgumentError,
    VerifyingDoubleError,
    VerifyingDoubleImportError
)


class TestInstanceDouble(object):
    def test_allows_stubs_on_existing_methods(self):
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
        date = InstanceDouble('datetime.date')

        allow(date).today

        assert date.today() is None

    def test_raises_when_target_is_a_top_level_module(self):
        with raises(VerifyingDoubleImportError) as e:
            InstanceDouble('foo')

        assert e.value.message == 'Invalid import path: foo.'

    def test_raises_on_import_error(self):
        with raises(VerifyingDoubleImportError) as e:
            InstanceDouble('foo.bar')

        assert e.value.message == 'Cannot import object from path: foo.bar.'

    def test_raises_when_importing_a_non_class_object(self):
        with raises(VerifyingDoubleImportError) as e:
            InstanceDouble('unittest.signals')

        assert e.value.message == 'Path does not point to a class: unittest.signals.'

    def test_raises_when_class_does_not_exist_in_module(self):
        with raises(VerifyingDoubleImportError) as e:
            InstanceDouble('unittest.foo')

        assert e.value.message == 'No object at path: unittest.foo.'

    def test_mocking__call__works(self):
        user = InstanceDouble('doubles.testing.User')
        allow(user).__call__.and_return('bob barker')
        assert user() == 'bob barker'
