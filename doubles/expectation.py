from doubles.allowance import Allowance
from doubles.exceptions import MockExpectationError


class Expectation(Allowance):
    """An individual method expectation (mock)."""

    def __init__(self, target, method_name, caller):
        """
        :param Target target: The object owning the method to mock.
        :param str method_name: The name of the method to mock.
        :param tuple caller: Details of the stack frame where the expectation was made.
        """
        super(Expectation, self).__init__(target, method_name)
        self._is_satisfied = False
        self._caller = caller

    def satisfy_any_args_match(self):
        """
        Returns a boolean indicating whether or not the mock will accept arbitrary arguments.
        This will be true unless the user has specified otherwise using ``with_args`` or
        ``with_no_args``.

        :return: Whether or not the mock accepts arbitrary arguments.
        :rtype: bool
        """

        is_match = super(Expectation, self).satisfy_any_args_match()

        if is_match:
            self._satisfy()

        return is_match

    def satisfy_exact_match(self, args, kwargs):
        """
        Returns a boolean indicating whether or not the mock will accept the provided arguments.

        :return: Whether or not the mock accepts the provided arguments.
        :rtype: bool
        """

        is_match = super(Expectation, self).satisfy_exact_match(args, kwargs)

        if is_match:
            self._satisfy()

        return is_match

    def _satisfy(self):
        """Marks the mock as satisfied."""

        self._is_satisfied = True

    def raise_failure_exception(self):
        """
        Raises a ``MockExpectationError`` with a useful message.

        :raise: ``MockExpectationError``
        """

        raise MockExpectationError(
            "Expected '{}' to be called on {!r} with {}, but was not. ({}:{})".format(
                self._method_name,
                self._target.obj,
                self._expected_argument_string(),
                self._caller[1],
                self._caller[2]
            )
        )
