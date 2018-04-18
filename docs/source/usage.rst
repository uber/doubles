Usage
=====

**Doubles** is used by creating stubs and mocks with the ``allow`` and ``expect`` functions. Each of these functions takes a "target" object as an argument. The target is the object whose methods will be allowed or expected to be called. For example, if you wanted to expect a call to something like ``User.find_by_id``, then ``User`` would be the target. Using a real object from your system as the target creates a so-called "partial double."

There are also three constructors, ``InstanceDouble``, ``ClassDouble``, and ``ObjectDouble``, which can be used to create so-called "pure double" targets, meaning they are unique objects which don't modify any existing object in the system.

The details of ``allow``, ``expect``, and the three pure double constructors follow.

Stubs and allowances
--------------------

Stubs are doubles which have a predetermined result when called. To stub out a method on an object, use the ``allow`` function::

    from doubles import allow

    from myapp import User


    def test_allows_get_name():
        user = User('Carl')

        allow(user).get_name

        assert user.get_name() is None

On the first line of the test, we create a user object from a theoretical class called ``User`` in the application we're testing. The second line declares an *allowance*, after which ``user.get_name`` will use the stub method rather than the real implementation when called. The default return value of a stub is ``None``, which the third line asserts.

To instruct the stub to return a predetermined value, use the ``and_return`` method::


    from doubles import allow

    from myapp import User


    def test_allows_get_name():
        user = User('Carl')

        allow(user).get_name.and_return('Henry')

        assert user.get_name() == 'Henry'

By default, once a method call has been allowed, it can be made any number of times and it will always return the value specified.

The examples shown so far will allow the stubbed method to be called with any arguments that match its signature. To specify that a method call is allowed only with specific arguments, use ``with_args``::

    from doubles import allow

    from myapp import User


    def test_allows_set_name_with_args():
        user = User('Carl')

        allow(user).set_name.with_args('Henry')

        user.set_name('Henry')  # Returns None
        user.set_name('Teddy')  # Raises an UnallowedMethodCallError

You do not need to specifically call ``with_args``, calling the allowance directly is the same as calling ``with_args``.  The following example is identical to the code above::

    from doubles import allow

    from myapp import User


    def test_allows_set_name_with_args():
        user = User('Carl')

        allow(user).set_name('Henry')

        user.set_name('Henry')  # Returns None
        user.set_name('Teddy')  # Raises an UnallowedMethodCallError

Multiple allowances can be specified for the same method with different arguments and return values::

    from doubles import allow

    from myapp import User

    def test_returns_different_values_for_different_arguments():
        user = User('Carl')

        allow(user).speak.with_args('hello').and_return('Carl says hello')
        allow(user).speak.with_args('thanks').and_return('Carl says thanks')

        assert user.speak('hello') == 'Carl says hello'
        assert user.speak('thanks') == 'Carl says thanks'

To specify that a method can only be called *with no arguments*, use ``with_no_args``::

    from doubles import allow

    from myapp import User


    def test_allows_greet_with_no_args():
        user = User('Carl')

        allow(user).greet.with_no_args().and_return('Hello!')

        user.greet()  # Returns 'Hello!'
        user.greet('Henry')  # Raises an UnallowedMethodCallError

Without the call to ``with_no_args``, ``user.greet('Henry')`` would have returned ``'Hello!'``.

Mocks and expectations
----------------------

Stubs are useful for returning predetermined values, but they do not verify that they were interacted with. To add assertions about double interaction into the mix, create a mock object by declaring an *expectation*. This follows a very similar syntax, but uses ``expect`` instead of ``allow``::

    from doubles import expect

    from myapp import User


    def test_allows_get_name():
        user = User('Carl')

        expect(user).get_name

The above test will fail with a ``MockExpectationError`` exception, because we expected ``user.get_name`` to be called, but it was not. To satisfy the mock and make the test pass::

    from doubles import expect

    from myapp import User


    def test_allows_get_name():
        user = User('Carl')

        expect(user).get_name

        user.get_name()

Mocks support the same interface for specifying arguments that stubs do. Mocks do not, however, support specification of return values or exceptions. If you want a test double to return a value or raise an exception, use a stub. Mocks are intended for verifying calls to methods that do not return a meaningful value. If the method does return a value, write an assertion about that value instead of using a mock.

Doubling top-level functions
----------------------------

The previous sections have shown examples where methods on classes are stubbed or mocked. It's also possible to double a top-level function by importing the module where the function is defined into your test file. Pass the module to ``allow`` or ``expect`` and proceed as normal. In the follow example, imagine that we want to stub a function called ``generate_user_token`` in the ``myapp.util`` module::

    from doubles import allow

    from myapp import util, User

    def test_get_token_returns_a_newly_generated_token_for_the_user():
        user = User('Carl')

        allow(util).generate_user_token.with_args(user).and_return('dummy user token')

        assert user.get_token() == 'dummy user token'

Fakes
-----

Fakes are doubles that have special logic to determine their return values, rather than returning a simple static value. A double can be given a fake implementation with the ``and_return_result_of`` method, which accepts any callable object::

    from doubles import allow

    from myapp import User


    def test_fake():
        user = User('Carl')

        allow(user).greet.and_return_result_of(lambda: 'Hello!')

        assert user.greet() == 'Hello!'

Although this example is functionally equivalent to calling ``and_return('Hello!')``, the callable passed to ``and_return_result_of`` can be arbitrarily complex. Fake functionality is available for both stubs and mocks.

Raising exceptions
------------------

Both stubs and mocks allow a method call to raise an exception instead of returning a result using the ``and_raise`` method. Simply pass the object you want to raise as an argument. The following test will pass::

    from doubles import allow

    from myapp import User


    def test_raising_an_exception():
        user = User('Carl')

        allow(user).get_name.and_raise(StandardError)

        try:
            user.get_name()
        except StandardError:
            pass
        else:
            raise AssertionError('Expected test to raise StandardError.')

If the exception to be raised requires arguments, they can be passed to the Exception constructor directly before ``and_raises`` is invoked::

    from doubles import allow

    from myapp import User


    def test_raising_an_exception():
        user = User('Carl')

        allow(user).get_name.and_raise(NonStandardError('an argument', arg2='another arg'))

        try:
            user.get_name()
        except NonStandardError:
            pass
        else:
            raise AssertionError('Expected test to raise NonStandardError.')

Call counts
-----------

Limits can be set on how many times a doubled method can be called. In most cases, you'll specify an exact call count with the syntax ``exactly(n).times``, which will cause the test to fail if the doubled method is called fewer or more times than you declared::

    from doubles import expect

    from myapp import User

    def test_expect_one_call():
        user = User('Carl')

        expect(user).get_name.exactly(1).time

        user.get_name()
        user.get_name()  # Raises a MockExpectationError because it should only be called once

The convenience methods ``once``, ``twice`` and ``never`` are provided for the most common use cases. The following test will pass::

    from doubles import expect

    from myapp import User

    def test_call_counts():
        user = User('Carl')

        expect(user).get_name.once()
        expect(user).speak.twice()
        expect(user).not_called.never()

        user.get_name()
        user.speak('hello')
        user.speak('good bye')

To specify lower or upper bounds on call count instead of an exact number, use ``at_least`` and ``at_most``::

    from doubles import expect

    from myapp import User

    def test_bounded_call_counts():
        user = User('Carl')

        expect(user).get_name.at_least(1).time
        expect(user).speak.at_most(2).times

        user.get_name  # The test would fail if this wasn't called at least once
        user.speak('hello')
        user.speak('good bye')
        user.speak('oops')  # Raises a MockExpectationError because we expected at most two calls

Call counts can be specified for allowances in addition to expectations, with the caveat that only upper bounds are enforced for allowances, making ``at_least`` a no-op.

Partial doubles
---------------

In all of the examples so far, we added stubs and mocks to an instance of our production ``User`` class. These are called a partial doubles, because only the parts of the object that were explicitly declared as stubs or mocks are affected. The untouched methods on the object behave as usual. Let's take a look at an example that illustrates this.::

    from doubles import allow


    class User(object):
        @classmethod
        def find_by_email(cls, email):
            pass

        @classmethod
        def find_by_id(cls, user_id):
            pass

    def test_partial_double():
        dummy_user = object()

        allow(User).find_by_email.and_return(dummy_user)

        User.find_by_email('alice@example.com')  # Returns <object object at 0x100290090>
        User.find_by_id(1)  # Returns <User object at 0x1006a8cd0>

For the sake of the example, assume that the two class methods on ``User`` are implemented to return an instance of the class. We create a sentinel value to use as a dummy user, and stub ``User`` to return that specific object when ``User.find_by_email`` is called. When we then call the two class methods, we see that the method we stubbed returns the sentinel value as we declared, and ``User.find_by_id`` retains its real implementation, returning a ``User`` object.

After a test has run, all partial doubles will be restored to their pristine, undoubled state.

Verifying doubles
-----------------

One of the trade offs of using test doubles is that production code may change after tests are written, and the doubles may no longer match the interface of the real object they are doubling. This is known as "API drift" and is one possible cause of the situation where a test suite is passing but the production code is broken. The potential for API drift is often used as an argument against using test doubles. **Doubles** provides a feature called verifying doubles to help address API drift and to increase confidence in test suites.

All test doubles created by **Doubles** are verifying doubles. They will cause the test to fail by raising a ``VerifyingDoubleError`` if an allowance or expectation is declared for a method that does not exist on the real object. In addition, the test will fail if the method exists but is specified with arguments that don't match the real method's signature.

In all the previous examples, we added stubs and mocks for real methods on the ``User`` object. Let's see what happens if we try to stub a method that doesn't exist::

    from doubles import allow

    from myapp import User


    def test_verification():
        user = User('Carl')

        allow(user).foo  # Raises a VerifyingDoubleError, because User objects have no foo method

Similarly, we cannot declare an allowance or expectation with arguments that don't match the actual signature of the doubled method::

    from doubles import allow

    from myapp import User


    def test_verification_of_arguments():
        user = User('Carl')

        # Raises a VerifyingDoubleArgumentError, because set_name accepts only one argument
        allow(user).set_name.with_args('Henry', 'Teddy')

Disabling builtin verification
++++++++++++++++++++++++++++++

Some of the objects in Python's standard library are written in C and do not support the same introspection capabilities that user-created objects do. Because of this, the automatic verification features of **Doubles** may not work when you try to double a standard library function. There are two approaches to work around this:

*Recommended*: Create a simple object that wraps the standard library you want to use. Use your wrapper object from your production code and double the wrapper in your tests. Test the wrapper itself in integration with the real standard library calls, without using test doubles, to ensure that your wrapper works as expected. Although this may seem heavy handed, it's actually a good approach, since it's a common adage of test doubles never to double objects you don't own.

Alternatively, use the ``no_builtin_verification`` context manager to disable the automatic verification. This is not a recommended approach, but is available if you must use it::

    from doubles import allow, InstanceDouble, no_builtin_verification

    with no_builtin_verification():
        date = InstanceDouble('datetime.date')

        allow(date).ctime

        assert date.ctime() is None

Pure doubles
------------

Often it's useful to have a test double that represents a real object, but does not actually touch the real object. These doubles are called pure doubles, and like partial doubles, stubs and mocks are verified against the real object. In contrast to partial doubles, pure doubles do not implement any methods themselves, so allowances and expectations must be explicitly declared for any method that will be called on them. Calling a method that has not been allowed or expected on a pure double will raise an exception, even if the object the pure double represents has such a method.

There are three different constructors for creating pure doubles, depending on what type of object you're doubling and how it should be verified:

InstanceDouble
++++++++++++++

``InstanceDouble`` creates a pure test double that will ensure its usage matches the API of an instance of the provided class. It's used as follows::

    from doubles import InstanceDouble, allow


    def test_verifying_instance_double():
      user = InstanceDouble('myapp.User')

      allow(user).foo

The argument to ``InstanceDouble`` is the fully qualified module path to the class in question. The double that's created will verify itself against an instance of that class. The example above will fail with a ``VerifyingDoubleError`` exception, assuming ``foo`` is not a real instance method.

ClassDouble
+++++++++++

``ClassDouble`` is the same as ``InstanceDouble``, except that it verifies against the class itself instead of an instance of the class. The following test will fail, assuming ``find_by_foo`` is not a real class method::

    from doubles import ClassDouble, allow

    def test_verifying_class_double():
      User = ClassDouble('myapp.User')

      allow(User).find_by_foo


ObjectDouble
++++++++++++

``ObjectDouble`` creates a pure test double that is verified against a specific object. The following test will fail, assuming ``foo`` is not a real method on ``some_object``::

    from doubles import ObjectDouble, allow

    from myapp import some_object


    def test_verifying_object_double():
      something = ObjectDouble(some_object)

      allow(something).foo

There is a subtle distinction between a pure test double created with ``ObjectDouble`` and a partial double created by passing a non-double object to ``allow`` or ``expect``. The former creates an object that does not accept any method calls which are not explicitly allowed, but verifies any that are against the real object. A partial double modifies parts of the real object itself, allowing some methods to be doubled and others to retain their real implementation.

Clearing Allowances
+++++++++++++++++++

If you ever want to to clear all allowances and expectations you have set without verifying them, use ``teardown``::

    from doubles import teardown, expect

    def test_clearing_allowances():
        expect(some_object).foobar

        teardown()

If you ever want to to clear all allowances and expectations you have set on an individual object  without verifying them, use ``clear``::

    from doubles import clear, expect

    def test_clearing_allowances():
        expect(some_object).foobar

        clear(some_object)

Patching
--------

``patch`` is used to replace an existing object::

    from doubles import patch
    import doubles.testing

    def test_patch():
        patch('doubles.testing.User', 'Bob Barker')

        assert doubles.testing.User == 'Bob Barker'

Patches do not verify against the underlying object, so use them carefully.  Patches are automatically restored at the end of the test.

Patching Classes
++++++++++++++++
``patch_class`` is a wrapper on top of ``patch`` to help you patch a python class with a ``ClassDouble``.  ``patch_class`` creates a ``ClassDouble`` of the class specified, patches the original class and returns the ``ClassDouble``::


    from doubles import patch_class, ClassDouble
    import doubles.testing

    def test_patch_class():
        class_double = patch_class('doubles.testing.User')

        assert doubles.testing.User is class_double
        assert isinstance(class_double, ClassDouble)

Stubbing Constructors
---------------------

By default ``ClassDoubles`` cannot create new instances::

    from doubles import ClassDouble

    def test_unstubbed_constructor():
        User = ClassDouble('doubles.testing.User')
        User('Teddy', 1901)  # Raises an UnallowedMethodCallError

Stubbing the constructor of a ``ClassDouble`` is very similar to using ``allow`` or ``expect`` except we use: ``allow_constructor`` or ``expect_constructor``, and don't specify a method::

    from doubles import allow_constructor, ClassDouble
    import doubles.testing

    def test_allow_constructor_with_args():
        User = ClassDouble('doubles.testing.User')

        allow_constructor(User).with_args('Bob', 100).and_return('Bob')

        assert User('Bob', 100) == 'Bob'

The return value of ``allow_constructor`` and ``expect_constructor`` support all of the same methods as allow/expect. (e.g. ``with_args``, ``once``, ``exactly``, .etc).


*NOTE*: Currently you can only stub the constructor of ``ClassDoubles``

Stubbing Asynchronous Methods
-----------------------------

Stubbing asynchronous methods requires returning futures ``and_return_future`` and ``and_raise_future`` do it for you.


Returning Values
++++++++++++++++

Stubbing a method with ``and_return_future`` is similar to using ``and_return``, except the value is wrapped in a ``Future``::

    from doubles import allow, InstanceDouble

    def test_and_return_future():
        user = InstanceDouble('doubles.testing.User')
        allow(user).instance_method.and_return_future('Bob Barker')

        result = user.instance_method()
        assert result.result() == 'Bob Barker'

Raising Exceptions
++++++++++++++++++

Stubbing a method with ``and_raise_future`` is similar to using ``and_raise``, except the exceptions is wrapped in a ``Future``::

    from doubles import allow, InstanceDouble
    from pytest import raises

    def test_and_raise_future():
        user = InstanceDouble('doubles.testing.User')
        exception = Exception('Bob Barker')
        allow(user).instance_method.and_raise_future(exception)
        result = user.instance_method()

        with raises(Exception) as e:
            result.result()

        assert e.value == exception
