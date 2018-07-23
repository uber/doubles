import pytest

from doubles.lifecycle import teardown, verify


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_call(item):
    outcome = yield

    try:
        outcome.get_result()
        verify()
    finally:
        teardown()
