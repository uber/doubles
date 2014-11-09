FAQ
===

I get a ``VerifyingBuiltinDoubleArgumentError`` "... is not a Python func", what is going on?
---------------------------------------------------------------------------------------------

Python does not allow doubles to look into builtin functions and asked them what their call signatures are.  Since we can't do this it is impossible to verify the arguments passed into a stubbed method.  By default if doubles cannot inspect a function it raises a ``VerifyingBuiltinDoubleArgumentError``, this is most common with builtins.  To bypass this functionality for builtins you can do::

      import functools

      from doubles import no_builtin_verification, allow


      with no_builtin_verification():
          allow(functools).reduce

          # The test that uses this allowance must be within the context manager.
          run_test()


How can I make an expectation return a value?
---------------------------------------------

You can't.  If your function depends on the return value of the method you are mocking then you should use allow.   Then you should test that the value returned from the allow was used correctly by asserting something later on. e.g.::

    def func_to_test(user_id):
        emails = api_call_to_get_emails(user_id)

        for e in emails:
            send_email(email_address)

Here we shouldn't expect that ``api_call_to_get_emails`` is called, we should expect that ``send_email`` is called with each email returned by ``api_call_to_get_emails``.  This test would look like::

    import myapp

    from doubles import allow, expect


    def test_func():
        allow(myapp).api_call_to_get_emails.with_args(1).and_return(
          ['bob@barker.com', 'drew@carey.com'],
        )

        expect(myapp).send_email.with_args('bob@barker').once()
        expect(myapp).send_email.with_args('drew@carey').once()

        func_to_test(1)


How can I make SomeClass(args, kwargs) return my double?
--------------------------------------------------------

You need to allow the __new__ method on the class you are using::

    from doubles import allow, InstanceDouble, no_builtin_verification

    import myapp


    def test_something_that_uses_user():
        user = InstanceDouble('myapp.user.User')

        with no_builtin_verification():
            allow(myapp.User).__new__.and_return(user)

Anytime a new instance of user is created will now return the InstanceDouble we defined.


I get a ``VerifyingDoubleError`` "Cannot double method ... does not implement it", whats going on?
--------------------------------------------------------------------------------------------------

Make sure you are using a version of doubles greater than 1.0.1.  There was a bug prior to 1.0.1 that would not allow you to mock callable objects.
