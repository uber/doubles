from doubles.space import Space


_current = None


def setup():
    global _current

    _current = Space()


def teardown():
    global _current

    _current = None


def verify():
    if _current:
        _current.verify()
    else:
        raise NoSpaceError('Verification can only occur between calls to setup and teardown.')


class NoSpaceError(StandardError):
    pass
