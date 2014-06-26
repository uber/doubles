import unittest

from doubles.double import Double
from doubles.targets.expectation_target import expect
from doubles.unittest import TestCase


class UnittestIntegration(TestCase):
    def runTest(self):
        subject = Double()

        expect(subject).to_receive('foo')

unittest.main()
