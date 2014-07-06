from __future__ import absolute_import

import sys

from nose.plugins.base import Plugin

from doubles.lifecycle import setup, verify, teardown
from doubles.exceptions import MockExpectationError


class NoseIntegration(Plugin):
    name = 'doubles'

    def beforeTest(self, test):
        setup()

    def afterTest(self, test):
        teardown()

    def prepareTestCase(self, test):
        def wrapped(result):
            test.test.run()
            if result.failures or result.errors:
                return
            try:
                verify()
            except MockExpectationError:
                result.addFailure(test.test,  sys.exc_info())
        return wrapped
