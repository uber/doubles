import re

from pytest import raises, mark

from doubles import allow, allow_constructor, expect_constructor, ClassDouble
from doubles.lifecycle import teardown, verify
from doubles.exceptions import (
    MockExpectationError,
    UnallowedMethodCallError,
    VerifyingDoubleError,
    VerifyingDoubleArgumentError,
)

TEST_CLASSES = (
    'doubles.testing.User',
    'doubles.testing.OldStyleUser',
    'doubles.testing.EmptyClass',
    'doubles.testing.OldStyleEmptyClass',
)

VALID_ARGS = {
    'doubles.testing.User': ('Bob', 100),
    'doubles.testing.OldStyleUser': ('Bob', 100),
    'doubles.testing.EmptyClass': tuple(),
    'doubles.testing.OldStyleEmptyClass': tuple(),
}


class TestClassDouble(object):
    def test_allows_stubs_on_existing_class_methods(self):
        User = ClassDouble('doubles.testing.User')

        allow(User).class_method

        assert User.class_method('arg') is None

    def test_raises_when_stubbing_nonexistent_methods(self):
        User = ClassDouble('doubles.testing.User')

        with raises(VerifyingDoubleError):
            allow(User).non_existent_method

    def test_allows_stubs_on_existing_static_methods(self):
        User = ClassDouble('doubles.testing.User')

        allow(User).static_method

        assert User.static_method('arg') is None

    def test_raises_when_stubbing_noncallable_class_attributes(self):
        User = ClassDouble('doubles.testing.User')

        with raises(VerifyingDoubleError):
            allow(User).class_attribute

    def test_raises_when_argspec_does_not_match(self):
        User = ClassDouble('doubles.testing.User')

        with raises(VerifyingDoubleArgumentError):
            allow(User).class_method.with_no_args()

    def test_raises_when_stubbing_instance_methods(self):
        User = ClassDouble('doubles.testing.User')

        with raises(VerifyingDoubleError) as e:
            allow(User).instance_method

        assert re.search(r"not callable directly on", str(e))


class TestUsingStubbingConstructor(object):
    @mark.parametrize('test_class', TEST_CLASSES)
    class TestUserAndEmptyClass(object):
        """Run test against User and EmptyClass"""

        def test_allowing_with_args(self, test_class):
            TestClass = ClassDouble(test_class)

            allow_constructor(TestClass).with_args(*VALID_ARGS[test_class]).and_return('Bob Barker')

            assert TestClass(*VALID_ARGS[test_class]) == 'Bob Barker'

        def test_with_no_allowances(self, test_class):
            TestClass = ClassDouble(test_class)

            with raises(UnallowedMethodCallError):
                TestClass(*VALID_ARGS[test_class])

        def test_unsatisfied_expectation(self, test_class):
            TestClass = ClassDouble(test_class)

            expect_constructor(TestClass)
            with raises(MockExpectationError):
                verify()
            teardown()

        def test_satisfied_exception(self, test_class):
            TestClass = ClassDouble(test_class)

            expect_constructor(TestClass)

            TestClass(*VALID_ARGS[test_class])

    @mark.parametrize('test_class', TEST_CLASSES[0:2])
    class TestUserOnly(object):
        """Test using the constructor on a class witha custom __init__"""

        def test_called_with_wrong_args(self, test_class):
            TestClass = ClassDouble(test_class)

            allow_constructor(TestClass).with_args(*VALID_ARGS[test_class]).and_return('Bob Barker')

            with raises(UnallowedMethodCallError):
                TestClass('Bob', 101)


class TestStubbingConstructor(object):
    @mark.parametrize('test_class', TEST_CLASSES)
    class TestAllow(object):
        def test_with_no_args(self, test_class):
            TestClass = ClassDouble(test_class)

            allow_constructor(TestClass)
            assert TestClass(*VALID_ARGS[test_class]) is None

        def test_with_invalid_args(self, test_class):
            TestClass = ClassDouble(test_class)

            with raises(VerifyingDoubleArgumentError):
                allow_constructor(TestClass).with_args(10)

        def test_with_valid_args(self, test_class):
            TestClass = ClassDouble(test_class)

            allow_constructor(TestClass).with_args(*VALID_ARGS[test_class]).and_return('Bob')

            assert TestClass(*VALID_ARGS[test_class]) == 'Bob'

    @mark.parametrize('test_class', TEST_CLASSES)
    class TestExpect(object):
        def test_with_no_args(self, test_class):
            TestClass = ClassDouble(test_class)

            expect_constructor(TestClass)
            assert TestClass(*VALID_ARGS[test_class]) is None

        def test_with_invalid_args(self, test_class):
            TestClass = ClassDouble(test_class)

            with raises(VerifyingDoubleArgumentError):
                expect_constructor(TestClass).with_args(10)
            teardown()

        def test_with_valid_args(self, test_class):
            TestClass = ClassDouble(test_class)

            expect_constructor(TestClass).with_args(*VALID_ARGS[test_class])

            assert TestClass(*VALID_ARGS[test_class]) is None
