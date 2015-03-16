FAQ
===

Common Issues
+++++++++++++


When I double __new__, it breaks other tests, why?
--------------------------------------------------

This feature is deprecated, I recommend  using the ``patch_class`` method, which fixes this issue and is much cleaner.


I get a ``VerifyingDoubleError`` "Cannot double method ... does not implement it", whats going on?
--------------------------------------------------------------------------------------------------

Make sure you are using a version of doubles greater than 1.0.1.  There was a bug prior to 1.0.1 that would not allow you to mock callable objects.


I get a ``VerifyingBuiltinDoubleArgumentError`` "... is not a Python func", what is going on?
---------------------------------------------------------------------------------------------

Python does not allow doubles to look into builtin functions and asked them what their call signatures are.  Since we can't do this it is impossible to verify the arguments passed into a stubbed method.  By default if doubles cannot inspect a function it raises a ``VerifyingBuiltinDoubleArgumentError``, this is most common with builtins.  To bypass this functionality for builtins you can do::

      import functools

      from doubles import no_builtin_verification, allow


      with no_builtin_verification():
          allow(functools).reduce

          # The test that uses this allowance must be within the context manager.
          run_test()


Patches
++++++++

How can I make SomeClass(args, kwargs) return my double?
--------------------------------------------------------

Use ``patch_class`` and ``allow_constructor``::

    from doubles import patch_class, allow_constructor

    import myapp

    def test_something_that_uses_user():
        patched_class = patch_class('myapp.user.User')
        allow_constructor(patched_class).and_return('Bob Barker')

        assert myapp.user.User() == 'Bob Barker'


``patch_class`` creates a ``ClassDouble`` of the class specified, patches the original class and returns the ``ClassDouble``.  We then stub the constructor which controls what is is returned when an instance is created.

``allow_constructor`` supports all of the same functionality as ``allow``::

    from doubles import patch_class, allow_constructor

    import myapp

    def test_something_that_uses_user():
        bob_barker = InstanceDouble('myapp.user.User')

        patched_class = patch_class('myapp.user.User')
        allow_constructor(patched_class).with_args('Bob Barker', 100).and_return(bob_barker)

        assert myapp.user.User('Bob Barker', 100) is bob_barker


How can I patch something like I do with mock?
----------------------------------------------

Doubles also has ``patch`` but it isn't a decorator::

    from doubles import allow, patch

    import myapp

    def test_something_that_uses_user():
        patch('myapp.user.User', 'Bob Barker')

        assert myapp.user.User == 'Bob Barker'

Patches do not verify against the underlying object, so use them carefully.  Patches are automatically restored at the end of the test.

Expectations
+++++++++++++

How do I assert that a function is not called?
----------------------------------------------

If you expect the ``send_mail`` method never to be called on ``user``::

    expect(user).send_mail.never()
