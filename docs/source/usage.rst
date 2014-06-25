Usage
=====

Pure doubles
------------

To create a pure test double, use the ``Double`` constructor. Pure test doubles do not respond to any messages by default. If the object receives an unknown message, the test will fail with an ``UnallowedMethodCallError`` exception.

The following test will fail with such an exception:

::

    from doubles import Double


    def test_raises_exception_on_unallowed_method_call():
        dummy = Double()

        dummy.foo()

Calling the ``Double`` constructor with no arguments creates an unnamed test double. It's a good idea to give test doubles names so that failure messages are more meaningful. This is achieved by providing a string name to the constructor::

    dummy = Double('dummy')

Stubs and message allowances
----------------------------

Doubles are not particularly useful if they don't respond to any messages. To stub out a method on an object, use the ``allow`` function::

    from doubles import Double, allow

    def test_allows_foo():
        dummy = Double('dummy')

        allow(dummy).to_receive('foo')

        assert dummy.foo() is None

On the first line, we create a pure test double which does not respond to any messages. The second line declares a *message allowance*, after which the double will respond to "foo" without raising an exception. The default return value of a stub is ``None``, which the third line asserts.

To instruct the stub to return a predetermined value, use the ``and_return`` method::


    from doubles import Double, allow

    def test_allows_foo():
        dummy = Double('dummy')

        allow(dummy).to_receive('foo').and_return('bar')

        assert dummy.foo() == 'bar'

Once a message has been allowed, the double can receive it any number of times and it will always return the value specified.

The examples shown so far will allow the ``foo`` method to be called with any arguments. To specify that a message is allowed only with specific arguments, use ``with_args``::

    from doubles import Double, allow

    def test_allows_foo_with_args():
        dummy = Double('dummy')

        allow(dummy).to_receive('foo').with_args(2, 'arguments', some='keyword').and_return('bar')

        dummy.foo()  # Raises an UnallowedMethodCallError
        dummy.foo(2, 'arguments', some='keyword')  # Returns 'bar'

Multiple message allowances can be specified for the same method with different arguments. To specify that a method can only be called *with no arguments*, use ``with_no_args``::

    from doubles import Double, allow

    def test_allows_foo_with_no_args():
        dummy = Double('dummy')

        allow(dummy).to_receive('foo').with_no_args().and_return('bar')

        dummy.foo('an argument')  # Raises an UnallowedMethodCallError
        dummy.foo()  # Returns 'bar'

Without the call to ``with_no_args``, ``dummy.foo`` could be called with any combination of arguments.

Mocks and message expectations
------------------------------

Stubs are useful for returning predetermined values, but they do not verify that they were interacted with. To add assertions about double interaction into the mix, create a mock object by declaring a *message expectation*. This follows a very similar syntax, but uses ``expect`` instead of ``allow``::

    from doubles import Double, expect

    def test_expects_foo():
        dummy = Double('dummy')

        expect(dummy).to_receive('foo')

The above test will fail with a ``MockExpectationError`` exception, because we expected the double to receive "foo", but it did not. To satisfy the mock and make the test pass::

    from doubles import Double, expect

    def test_expects_foo():
        dummy = Double('dummy')

        expect(dummy).to_receive('foo')

        dummy.foo()

Mocks support the same interface for specifying arguments and return values that stubs do.

Fakes
-----

Fakes are doubles that have special logic to determine their return values, rather than returning a simple static value. A double can be given a fake implementation with the ``and_return_result_of`` method, which accepts any callable object::

    from doubles import Double, allow

    def test_fake():
        dummy = Double('dummy')

        allow(dummy).to_receive('foo').and_return_result_of(lambda: 'bar')

        assert dummy.foo() == 'bar'

Although this example is functionally equivalent to calling ``and_return('bar')``, the callable passed to ``and_return_result_of`` can be arbitrarily complex. Fake functionality is available for both stubs and mocks.

Raising exceptions
------------------

Both stubs and mocks allow a method call to raise an exception instead of returning a result using the ``and_raise`` method. Simply pass the object you want to raise as an argument. The following test will pass::

    from doubles import Double, allow

    def test_raising_an_exception():
        dummy = Double('dummy')

        allow(dummy).to_receive('foo').and_raise(StandardError)

        try:
            dummy.foo()
        except StandardError:
            pass
        else:
            raise AssertionError('Expected test to raise StandardError.')

Partial doubles
---------------

In addition to pure test doubles created with the ``Double`` constructor, Doubles also supports parital doubles, which allow you to stub or mock select methods on a real object without affecting the rest of it.

::

    class User(object):
        @classmethod
        def find_by_email(cls, email):
            pass

        @classmethod
        def find_by_id(cls, user_id):
            pass

    def test_partial_double():
        dummy_user = Double('user')

        allow(User).to_receive('find_by_email').and_return(dummy_user)

        assert User.find_by_email('alice@example.com') == dummy_user
        assert User.find_by_id(1).name == 'Bob'

For the sake of the example, assume that the two class methods on ``User`` are implemented. Instead of using a pure test double created by the ``Double`` constructor, we pass the real ``User`` object to ``allow`` and declare a message allowance for its ``find_by_email`` method. This creates a partial double, stubbing that particular method call on the real object, but allowing everything else, such as ``find_by_id`` to work as usual. The assertions show that the stubbed method returns the predetermined test double ``dummy_user``, while the unaffected method returns a real ``User`` object like normal.

After a test has run, all partial doubles will be restored to their pristine, undoubled state.

Verifying doubles
-----------------

One of the dangers of using test doubles is that production code may change after tests are written, and the doubles may no longer match the interface of the real object they are doubling. This is known as "API drift" and is the cause of the situation where a test suite is passing but the production code is broken. This potential for API drift is often used as an argument for avoiding the use of test doubles. Doubles provides a feature called verifying doubles to help address API drift and increase confidence in test suites.

Verifying doubles are used just like pure test doubles, except they will cause the test to fail if a message allowance or expectation is declared for a method that does not exist on the real object. In addition, the test will fail if the method exists but is called with an arity that doesn't match the real method's signature.

There are three ways of creating verifying doubles:

instance_double
+++++++++++++++

``instance_double`` creates a pure test double that will ensure its usage matches the API of an instance of the provided class. It's used as follows::

    from doubles import instance_double, allow

    def test_verifying_instance_double():
      user = instance_double('mypackage.User')

      allow(user).to_receive('nonexistent_method')

      assert user.nonexistent_method() is None

The argument to ``instance_double`` is the fully qualified module path to the class in question. The double that's created will verify itself against an instance of that class. The example above will fail with a ``VerifyingDoubleError`` exception. Note that the actual assertion made in this test is irrelevant, it's the call to ``allow`` and ``to_receive`` that will cause the failure.

class_double
++++++++++++

``class_double`` is the same as ``instance_double``, except that it verifies against the class itself instead of an instance of the class. The following test will fail::

    from doubles import class_double, allow

    def test_verifying_class_double():
      User = class_double('mypackage.User')

      allow(User).to_receive('find_by_nonexistent_attribute')

      assert User.find_by_nonexistent_attribute() is None

object_double
+++++++++++++

``object_double`` creates a pure test double that is verified against a specific object. The following test will fail::

    from doubles import object_double, allow

    from mypackage import some_object

    def test_verifying_object_double():
      something = object_double(some_object)

      allow(something).to_receive('nonexistent_method')

      assert something.nonexistent_method() is None

There is a subtle distinction between a pure test double created with ``object_double`` and a partial double created by passing a non-double object to ``allow`` or ``expect``. The former creates an object that does not respond to any messages which are not explicitly allowed, but verifies any that are against the real object. A partial double modifies parts of the real object itself, allowing some methods to be doubled and others to retain their usual implementation.
