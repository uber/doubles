from doubles.lifecycle import teardown, verify


def pytest_runtest_call(item, __multicall__):
    __multicall__.execute()
    verify()
    teardown()
