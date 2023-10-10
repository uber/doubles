Integration with test frameworks
================================

dobles includes plugins for automatic integration with popular test runners.

Pytest
------

Pytest integration will automatically be loaded and activated via setuptools entry points. To disable dobles for a particular test run, run Pytest as::

    $ py.test -p no:dobles file_or_directory


unittest
--------

Inherit from ``dobles.unittest.TestCase`` in your test case classes and the dobles lifecycle will be managed automatically.

Manual integration
------------------

If you are using another test runner or need manual control of the dobles lifecycle, these are the two methods you'll need to use:

1. ``dobles.verify`` should be called after each test to verify any expectations made. It can be skipped if the test case has already failed for another reason.
2. ``dobles.teardown`` must be called after each test and after the call to ``dobles.verify``.
