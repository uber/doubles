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
            assert 'Ran 2 tests' in self.output

        def makeSuite(self):
            class TestCase(unittest.TestCase):
                def runTest(self):
                    subject = InstanceDouble('doubles.testing.User')

                    expect(subject).instance_method

                def test2(self):
                    pass

            return [TestCase('runTest'), TestCase('test2')]

    result = unittest.TestResult()
    TestNosePlugin('test_expect')(result)
    assert result.wasSuccessful()
