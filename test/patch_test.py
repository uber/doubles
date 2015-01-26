import pytest

from doubles import (
    patch,
    patch_class,
    InstanceDouble,
    allow,
    allow_constructor,
    expect_constructor,
)
from doubles.exceptions import (
    MockExpectationError,
    UnallowedMethodCallError,
    VerifyingDoubleImportError,
    VerifyingDoubleError,
    VerifyingDoubleArgumentError,
)
from doubles.lifecycle import teardown, verify
import doubles.testing


class TestPatch(object):
    def test_patch_wth_new_object_supplied(self):
        patch('doubles.testing.User', 'Bob Barker')

        assert doubles.testing.User == 'Bob Barker'

    def test_restores_original_value(self):
        original_value = doubles.testing.User
        patch('doubles.testing.User', 'Bob Barker')

        teardown()

        assert original_value == doubles.testing.User

    def test_patch_objects_value(self):
        p = patch('doubles.testing.User', 'Bob Barker')

        assert doubles.testing.User == p.value

    def test_creating_instance_double_after_patching(self):
        patch('doubles.testing.User', InstanceDouble('doubles.testing.User'))

        assert InstanceDouble('doubles.testing.User')

    def test_patch_non_existent_object(self):
        with pytest.raises(VerifyingDoubleError):
            patch('doubles.testing.NotReal', True)


class TestPatchClass(object):
    def test_raises_an_error_trying_to_patch_a_function(self):
        with pytest.raises(VerifyingDoubleImportError):
            patch_class('doubles.test.top_level_function')

    def test_using_the_patched_class(self):
        allow_constructor(patch_class('doubles.testing.User')).and_return('result_1')
        allow_constructor(patch_class('doubles.testing.OldStyleUser')).and_return('result_2')

        result_1, result_2 = doubles.testing.top_level_function_that_creates_an_instance()

        assert result_1 == 'result_1'
        assert result_2 == 'result_2'

    def test_with_supplied_instances(self):
        user_1 = InstanceDouble('doubles.testing.User')
        user_2 = InstanceDouble('doubles.testing.User')
        patch = patch_class('doubles.testing.User')

        allow_constructor(patch).and_return(user_1, user_2)

        assert doubles.testing.User('Bob', 10) is user_1
        assert doubles.testing.User('Bob', 10) is user_2

    def test_allowing_class_method(self):
        factory = patch_class('doubles.testing.User')
        allow(factory).class_method.and_return('Bob Barker')

        assert doubles.testing.User.class_method(1) == 'Bob Barker'

    def test_allowing_non_existent_method(self):
        factory = patch_class('doubles.testing.User')
        with pytest.raises(VerifyingDoubleError):
            allow(factory).not_a_class_method

    def test_unallowed_class_method(self):
        patch_class('doubles.testing.User')

        with pytest.raises(AttributeError):
            doubles.testing.User.class_method(1)

    def test_called_with_invalid_arguments(self):
        patch_class('doubles.testing.User')

        with pytest.raises(VerifyingDoubleArgumentError):
            doubles.testing.User()

    def test_allowing_with_args(self):
        patch = patch_class('doubles.testing.User')

        allow_constructor(patch).with_args('Bob', 1).and_return('Bob Barker')
        allow_constructor(patch).with_args('Drew', 1).and_return('Drew Carey')

        assert doubles.testing.User('Bob', 1) == 'Bob Barker'
        assert doubles.testing.User('Drew', 1) == 'Drew Carey'

    def test_with_no_allowances(self):
        patch_class('doubles.testing.User')

        with pytest.raises(UnallowedMethodCallError):
            doubles.testing.User('Bob', 1)

    def test_unsatisfied_expectation(self):
        patched_class = patch_class('doubles.testing.User')

        expect_constructor(patched_class)
        with pytest.raises(MockExpectationError):
            verify()
        teardown()

    def test_called_with_wrong_args(self):
        patch = patch_class('doubles.testing.User')

        allow_constructor(patch).with_args('Bob', 1).and_return('Bob Barker')

        with pytest.raises(UnallowedMethodCallError):
            doubles.testing.User('Bob', 101)

    def test_satisfied_exception(self):
        patch = patch_class('doubles.testing.User')

        expect_constructor(patch)

        doubles.testing.User('Bob', 10)

    def test_a_non_class(self):
        with pytest.raises(VerifyingDoubleImportError):
            patch_class('doubles.testing.top_level_function')
