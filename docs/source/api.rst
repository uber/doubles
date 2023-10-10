API
===

Stubs and mocks
---------------

.. autofunction:: dobles.allow
.. autofunction:: dobles.expect
.. autofunction:: dobles.allow_constructor
.. autofunction:: dobles.expect_constructor
.. autofunction:: dobles.patch
.. autofunction:: dobles.patch_class

.. autoclass:: dobles.allowance.Allowance
    :members: and_raise, and_return, and_return_result_of, with_args, with_no_args
.. autoclass:: dobles.expectation.Expectation
    :members: with_args, with_no_args

Pure dobles
------------

.. autoclass:: dobles.InstanceDouble
    :inherited-members:
.. autoclass:: dobles.ClassDouble
    :members:
    :inherited-members:
.. autoclass:: dobles.ObjectDouble
    :members:

Test lifecycle
--------------
.. autofunction:: dobles.verify
.. autofunction:: dobles.teardown

Exceptions
----------

.. automodule:: dobles.exceptions
    :members:
