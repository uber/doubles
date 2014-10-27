from __future__ import absolute_import

import sys

from nose.plugins.base import Plugin

from doubles.lifecycle import verify, teardown
from doubles.exceptions import MockExpectationError


class NoseIntegration(Plugin):
    name = 'doubles'

    def afterTest(self, test):
        teardown()

    def prepareTestCase(self, test):
        def wrapped(result):
            test.test(result)

            try:
                verify()
            except MockExpectationError:
                result.addFailure(test.test,  sys.exc_info())

        return wrapped
