from coverage import coverage


cov = coverage(source=('doubles',))
cov.start()


from doubles import lifecycle


def pytest_sessionfinish(session, exitstatus):
    cov.stop()


def pytest_terminal_summary(terminalreporter):
    print "\nCoverage report:\n"
    cov.report(show_missing=True, ignore_errors=True, file=terminalreporter._tw)
    cov.html_report()


def pytest_runtest_setup(item):
    lifecycle.setup()


def pytest_runtest_teardown(item, nextitem):
    lifecycle.verify()
    lifecycle.teardown()
