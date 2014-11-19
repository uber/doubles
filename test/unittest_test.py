import unittest

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

from doubles.instance_double import InstanceDouble
from doubles.targets.expectation_target import expect
from doubles.unittest import TestCase


def test_unittest_integration():
    class UnittestIntegration(TestCase):
        def runTest(self):
            subject = InstanceDouble('doubles.testing.User')

            expect(subject).instance_method

    test_loader = unittest.TestLoader()
    suite = test_loader.loadTestsFromTestCase(UnittestIntegration)
    stream = StringIO()
    runner = unittest.TextTestRunner(stream=stream)
    result = runner.run(suite)

    assert len(result.failures) == 1
    assert 'MockExpectationError' in stream.getvalue()
