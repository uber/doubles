API
===

Stubs and mocks
---------------

.. autofunction:: doubles.allow
.. autofunction:: doubles.expect
.. autofunction:: doubles.allow_constructor
.. autofunction:: doubles.expect_constructor
.. autofunction:: doubles.patch
.. autofunction:: doubles.patch_class

.. autoclass:: doubles.allowance.Allowance
    :members: and_raise, and_return, and_return_result_of, with_args, with_no_args
.. autoclass:: doubles.expectation.Expectation
    :members: with_args, with_no_args

Pure doubles
------------

.. autoclass:: doubles.InstanceDouble
    :inherited-members:
.. autoclass:: doubles.ClassDouble
    :members:
    :inherited-members:
.. autoclass:: doubles.ObjectDouble
    :members:

Test lifecycle
--------------
.. autofunction:: doubles.verify
.. autofunction:: doubles.teardown

Exceptions
----------

.. automodule:: doubles.exceptions
    :members:
