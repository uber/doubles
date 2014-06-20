class MockExpectationError(Exception):
    """An exception raised when a mock fails verification."""

    pass


class UnallowedMethodCallError(Exception):
    """An exception raised when a double receives a message that has not been allowed."""

    pass
