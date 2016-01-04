import pytest

from doubles.lifecycle import teardown, verify


try:
    @pytest.hookimpl(hookwrapper=True)
    def pytest_runtest_protocol(item):
        try:
            outcome = yield  # noqa
            verify()
        finally:
            teardown()
except AttributeError:
    def pytest_runtest_call(item, __multicall__):
        try:
            __multicall__.execute()
            verify()
        finally:
            teardown()
