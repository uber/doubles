from __future__ import absolute_import
import unittest

from doubles.lifecycle import teardown, verify


def wrap_test(test_func):
    def wrapper():
        test_func()
        verify()

    return wrapper


class TestCase(unittest.TestCase):
    def __init__(self, methodName='runTest'):
        super(TestCase, self).__init__(methodName)

        setattr(self, self._testMethodName, wrap_test(getattr(self, self._testMethodName)))

    def setUp(self):
        self.addCleanup(teardown)
