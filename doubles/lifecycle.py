from threading import local

from doubles.exceptions import NoSpaceError
from doubles.space import Space


_thread_local_data = local()


def current_space():
    if hasattr(_thread_local_data, 'current_space'):
        return _thread_local_data.current_space


def setup():
    """Sets up the Doubles environment. Must be called before each test case."""

    _thread_local_data.current_space = Space()


def teardown():
    """Tears down the current Doubles environment. Must be called after each test case."""
    if current_space():
        current_space().teardown()

    _thread_local_data.current_space = None


def verify():
    """
    Verifies any mocks that have been created during the test run. Must be called after each
    test case, but before teardown.
    """

    if current_space():
        current_space().verify()
    else:
        raise NoSpaceError('Verification can only occur between calls to setup and teardown.')
