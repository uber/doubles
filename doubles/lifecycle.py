from threading import local

from doubles.space import Space


_thread_local_data = local()


def current_space():
    """
    An accessor for the current thread's active ``Space``.

    :return: The active ``Space``.
    :rtype: Space
    """

    if not hasattr(_thread_local_data, 'current_space'):
        _thread_local_data.current_space = Space()

    return _thread_local_data.current_space


def teardown():
    """Tears down the current Doubles environment. Must be called after each test case."""
    if hasattr(_thread_local_data, 'current_space'):
        _thread_local_data.current_space.teardown()
        del _thread_local_data.current_space


def verify():
    """
    Verifies any mocks that have been created during the test run. Must be called after each
    test case, but before teardown.
    """

    if hasattr(_thread_local_data, 'current_space'):
        _thread_local_data.current_space.verify()
