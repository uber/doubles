import pytest

from doubles import (
    patch,
    patch_class,
    InstanceDouble,
    ClassDouble,
    allow_constructor,
)
from doubles.exceptions import (
    VerifyingDoubleImportError,
    VerifyingDoubleError,
)
from doubles.lifecycle import teardown
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

    def test_restores_original_value(self):
        original_value = doubles.testing.User
        patch_class('doubles.testing.User')

        teardown()

        assert original_value == doubles.testing.User

    def test_non_existent_class(self):
        with pytest.raises(VerifyingDoubleImportError):
            patch_class('doubles.testing.NotReal')

    def test_class_double_after_patching(self):
        patch_class('doubles.testing.User')
        assert ClassDouble('doubles.testing.User')
