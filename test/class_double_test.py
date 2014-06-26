from pytest import raises

from doubles import allow, ClassDouble
from doubles.exceptions import VerifyingDoubleError


class TestClassDouble(object):
    def test_allows_stubs_on_existing_class_methods(self):
        User = ClassDouble('doubles.testing.User')

        allow(User).to_call('class_method')

        assert User.class_method() is None

    def test_raises_when_stubbing_nonexistent_methods(self):
        User = ClassDouble('doubles.testing.User')

        with raises(VerifyingDoubleError):
            allow(User).to_call('non_existent_method')

    def test_allows_stubs_on_existing_static_methods(self):
        User = ClassDouble('doubles.testing.User')

        allow(User).to_call('static_method')

        assert User.static_method() is None

    def test_raises_when_stubbing_noncallable_class_attributes(self):
        User = ClassDouble('doubles.testing.User')

        with raises(VerifyingDoubleError):
            allow(User).to_call('class_attribute')

    def test_raises_when_argspec_does_not_match(self):
        User = ClassDouble('doubles.testing.User')

        with raises(VerifyingDoubleError):
            allow(User).to_call('class_method').with_args('foo')

    def test_raises_when_stubbing_instance_methods(self):
        User = ClassDouble('doubles.testing.User')

        with raises(VerifyingDoubleError):
            allow(User).to_call('instance_method')
