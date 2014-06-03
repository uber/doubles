__version__ = '0.0.1'

from doubles.double import Double  # noqa
from doubles.space import Space


_current = None


def setup():
    global _current

    _current = Space()


def teardown():
    global _current

    _current = None


def verify():
    _current.verify()
