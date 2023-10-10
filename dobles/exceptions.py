class MockExpectationError(AssertionError):
    """An exception raised when a mock fails verification."""

    pass


class UnallowedMethodCallError(AssertionError):
    """An exception raised when an unallowed method call is made on a double."""

    pass


class VerifyingDoubleError(AssertionError):
    """
    An exception raised when attempting to double a method that does not exist on the real object.
    """

    def __init__(self, method_name, doubled_obj):
        """
        :param str method_name: The name of the method to double.
        :param object doubled_obj: The real object being doubled.
        """

        self._method_name = method_name
        self._doubled_obj = doubled_obj
        self.args = (method_name, doubled_obj)
        self.message = "Cannot double method '{}' of '{}'."

    def no_matching_method(self):
        self.message = "Cannot double method '{}' because {} does not implement it."

        return self

    def not_callable(self):
        self.message = "Cannot double method '{}' because it is not a callable attribute on {}."

        return self

    def requires_instance(self):
        self.message = "Cannot double method '{}' because it is not callable directly on {}."

        return self

    def __str__(self):
        return self.message.format(self._method_name, self._doubled_obj)


class VerifyingDoubleArgumentError(AssertionError):
    """
    An exception raised when attempting to double a method with arguments that do not match the
    signature of the real method.
    """

    pass


class VerifyingBuiltinDoubleArgumentError(VerifyingDoubleArgumentError):
    """
    An exception raised when attempting to validate arguments of a builtin.
    """

    pass


class VerifyingDoubleImportError(AssertionError):
    """
    An exception raised when attempting to create a verifying double from an invalid module path.
    """


class ConstructorDoubleError(AssertionError):
    """
    An exception raised when attempting to double the constructor of a non ClassDouble.
    """
