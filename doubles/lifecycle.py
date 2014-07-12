from threading import local

from doubles.exceptions import NoSpaceError
from doubles.space import Space


_thread_local_data = local()


def current_space():
    if hasattr(_thread_local_data, 'current_space'):
        return _thread_local_data.current_space


def setup():
    _thread_local_data.current_space = Space()


def teardown():
    if current_space():
        current_space().teardown()

    _thread_local_data.current_space = None


def verify():
    if current_space():
        current_space().verify()
    else:
        raise NoSpaceError('Verification can only occur between calls to setup and teardown.')
