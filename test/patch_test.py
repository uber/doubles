import dobles.testing
import pytest
from dobles import (ClassDouble, InstanceDouble, allow_constructor, patch,
                    patch_class)
from dobles.exceptions import VerifyingDoubleError, VerifyingDoubleImportError
from dobles.lifecycle import teardown


class TestPatch(object):

    def test_patch_wth_new_object_supplied(self):
        patch('dobles.testing.User', 'Bob Barker')

        assert dobles.testing.User == 'Bob Barker'

    def test_restores_original_value(self):
        original_value = dobles.testing.User
        patch('dobles.testing.User', 'Bob Barker')

        teardown()

        assert original_value == dobles.testing.User

    def test_creating_instance_double_after_patching(self):
        patch('dobles.testing.User', InstanceDouble('dobles.testing.User'))

        assert InstanceDouble('dobles.testing.User')

    def test_patch_non_existent_object(self):
        with pytest.raises(VerifyingDoubleError):
            patch('dobles.testing.NotReal', True)


class TestPatchClass(object):

    def test_raises_an_error_trying_to_patch_a_function(self):
        with pytest.raises(VerifyingDoubleImportError):
            patch_class('dobles.test.top_level_function')

    def test_using_the_patched_class(self):
        allow_constructor(patch_class('dobles.testing.User')).and_return(
            'result_1',
            'result_2',
        )

        r1, r2 = dobles.testing.top_level_function_that_creates_an_instance()

        assert r1 == 'result_1'
        assert r2 == 'result_2'

    def test_restores_original_value(self):
        original_value = dobles.testing.User
        patch_class('dobles.testing.User')

        teardown()

        assert original_value == dobles.testing.User

    def test_non_existent_class(self):
        with pytest.raises(VerifyingDoubleImportError):
            patch_class('dobles.testing.NotReal')

    def test_class_double_after_patching(self):
        patch_class('dobles.testing.User')
        assert ClassDouble('dobles.testing.User')
