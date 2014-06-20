Integration with test frameworks
=============================

Integrating Doubles with your test framework of choice involves adding a few calls to the setup and teardown hooks. There are three methods from Doubles that must be invoked:

1. ``doubles.setup`` must be called before each test.
2. ``doubles.verify`` must be called after each test, but can be skipped if the test has already failed.
3. ``doubles.teardown`` must be called after each test and after the call to ``doubles.verify``.

If your test framework does not provide setup and teardown hooks that apply to all tests it runs, you might want to consolidate Doubles integration code in a shared base class.


unittest
--------

::

    import unittest

    import doubles


    class TestUsingDoubles(unittest.TestCase):
        def setUp(self):
            doubles.setup()
            self.addCleanup(doubles.teardown)

        def tearDown(self):
            doubles.verify()

pytest
------

In your ``conftest.py`` file:

::

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
