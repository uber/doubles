class MockExpectationError(AssertionError):
    """An exception raised when a mock fails verification."""

    pass


class NoSpaceError(Exception):
    """An exception raised when attempting to verify the lifecycle after it's been torn down."""

    pass


class UnallowedMethodCallError(AssertionError):
    """An exception raised when an unallowed method call is made on a double."""

    pass


class VerifyingDoubleError(AssertionError):
    """
    An exception raised when attempting to double a method that does not exist on the real object
    or with arguments that do not match the signature of the real method.
    """
