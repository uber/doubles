from doubles.lifecycle import teardown, verify


def pytest_runtest_call(item):
    try:
        verify()
    finally:
        teardown()
