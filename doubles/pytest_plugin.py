import pytest

from doubles.lifecycle import teardown, verify

def pytest_runtest_call(item):
    def verify_and_teardown_doubles():
        try:
            verify()
        except Exception as e:
            pytest.fail(str(e))
        finally:
            teardown()

    item.addfinalizer(verify_and_teardown_doubles)
