import unittest

from nose.plugins import PluginTester

from doubles.nose import NoseIntegration
from doubles.instance_double import InstanceDouble
from doubles.targets.expectation_target import expect


def test_nose_plugin():
    class TestNosePlugin(PluginTester, unittest.TestCase):
        activate = '--with-doubles'
        plugins = [NoseIntegration()]

        def test_expect(self):
            assert 'MockExpectationError' in self.output
            assert 'FAILED (failures=1)' in self.output

        def makeSuite(self):
            class TestCase(unittest.TestCase):
                def runTest(self):
                    subject = InstanceDouble('doubles.testing.User')

                    expect(subject).instance_method

            return [TestCase()]

    result = unittest.TestResult()
    TestNosePlugin('test_expect')(result)
    assert result.wasSuccessful()
