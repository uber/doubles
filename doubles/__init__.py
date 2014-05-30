__version__ = '0.0.1'

from doubles.double import Double
from doubles.verifying_double import VerifyingDouble


def double(target=None, verify=True):
    if verify:
        return VerifyingDouble(target)
    else:
        return Double(target)
