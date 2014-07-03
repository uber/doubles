from doubles import lifecycle


def pytest_runtest_call(item, __multicall__):
    lifecycle.setup()

    __multicall__.execute()

    if lifecycle.current_space():
        lifecycle.verify()
        lifecycle.teardown()
