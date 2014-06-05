from doubles import lifecycle


def pytest_runtest_setup(item):
    lifecycle.setup()


def pytest_runtest_teardown(item, nextitem):
    lifecycle.teardown()
