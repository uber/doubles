Integration with test frameworks
================================

Doubles includes a class for integrating with the standard unittest test framework. Other test frameworks currently require manual integration.

If you're not using unittest, you'll need to add a few calls to your suite's setup and teardown hooks. There are three methods from Doubles that must be invoked:

1. ``doubles.setup`` must be called before each test.
2. ``doubles.verify`` must be called after each test, but can be skipped if the test has already failed.
3. ``doubles.teardown`` must be called after each test and after the call to ``doubles.verify``.

If your test framework does not provide setup and teardown hooks that apply to all tests it runs, you might want to consolidate Doubles integration code in a shared base class.


unittest
--------

Inherit from ``doubles.unittest.TestCase`` in your test case classes and the Doubles lifecycle will be managed automatically, including automatic verification of expectations for each test.

pytest
------

In your ``conftest.py`` file::

    import doubles


    def pytest_runtest_setup(item):
        doubles.setup()


    def pytest_runtest_teardown(item, nextitem):
        doubles.verify()
        doubles.teardown()


nose
----

::

    from nose import with_setup
    import doubles


    def setup():
        doubles.setup()


    def teardown():
        doubles.verify()
        doubles.teardown()


    @with_setup(setup, teardown)
    def test_example():
        """Your test case goes here."""

        pass
