API
===

Stubs and mocks
---------------

.. autofunction:: doubles.allow
.. autofunction:: doubles.expect

.. autoclass:: doubles.allowance.Allowance
    :members: and_raise, and_return, and_return_result_of, with_args, with_no_args
.. autoclass:: doubles.expectation.Expectation
    :members: and_raise, and_return, and_return_result_of, with_args, with_no_args

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
.. autofunction:: doubles.setup
.. autofunction:: doubles.verify
.. autofunction:: doubles.teardown

Exceptions
----------

.. automodule:: doubles.exceptions
    :members:
