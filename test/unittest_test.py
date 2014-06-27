from StringIO import StringIO
import unittest

from doubles.double import Double
from doubles.targets.expectation_target import expect
from doubles.unittest import TestCase


def test_unittest_integration():
    class UnittestIntegration(TestCase):
        def runTest(self):
            subject = Double()

            expect(subject).to_call('foo')

    test_loader = unittest.TestLoader()
    suite = test_loader.loadTestsFromTestCase(UnittestIntegration)
    stream = StringIO()
    runner = unittest.TextTestRunner(stream=stream)
    result = runner.run(suite)

    assert len(result.failures) == 1
    assert 'MockExpectationError' in stream.getvalue()
