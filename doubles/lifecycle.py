from doubles.space import Space


_current_space = None


def current_space():
    return _current_space


def setup():
    global _current_space

    _current_space = Space()


def teardown():
    global _current_space

    _current_space = None


def verify():
    if current_space():
        current_space().verify()
    else:
        raise NoSpaceError('Verification can only occur between calls to setup and teardown.')


class NoSpaceError(StandardError):
    pass
