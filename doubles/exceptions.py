class MockExpectationError(Exception):
    """An exception raised when a mock fails verification."""

    pass


class NoSpaceError(Exception):
    """An exception raised when attempting to verify the lifecycle after it's been torn down."""

    pass


class UnallowedMethodCallError(Exception):
    """An exception raised when a double receives a message that has not been allowed."""

    pass


class VerifyingDoubleError(Exception):
    """An exception raised when a stub on a verifying double is inconsitent with the underlying object"""  # noqa

    pass
