from __future__ import absolute_import

import sys

from nose.plugins.base import Plugin

from doubles.lifecycle import setup, verify, teardown, current_space
from doubles.exceptions import MockExpectationError


class NoseIntegration(Plugin):
    name = 'doubles'

    def beforeTest(self, test):
        setup()

    def afterTest(self, test):
        if current_space():
            teardown()

    def prepareTestCase(self, test):
        def wrapped(result):
            test.test.run()
            if result.failures or result.errors:
                return
            try:
                if current_space():
                    verify()
            except MockExpectationError:
                result.addFailure(test.test,  sys.exc_info())
        return wrapped
