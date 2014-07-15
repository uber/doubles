Integration with test frameworks
================================

Doubles includes plugins for automatic integration with popular test runners.

Pytest
------

Pytest integration will automatically be loaded and activated via setuptools entry points. To disable Doubles for a particular test run, run Pytest as::

    $ py.test -p no:doubles file_or_directory

Nose
----

Nose integration will be loaded and activated by running Nose as::

    $ nosetests --with-doubles file_or_directory

unittest
--------

Inherit from ``doubles.unittest.TestCase`` in your test case classes and the Doubles lifecycle will be managed automatically.

Manual integration
------------------

If you are using another test runner or need manual control of the Doubles lifecycle, these are the three methods you'll need to use:

1. ``doubles.setup`` must be called before each test.
2. ``doubles.verify`` must be called after each test, but can be skipped if the test has already failed.
3. ``doubles.teardown`` must be called after each test and after the call to ``doubles.verify``.
