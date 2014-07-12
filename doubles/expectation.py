from doubles.allowance import Allowance
from doubles.exceptions import MockExpectationError


def pluralize(word, n):
    return word if n == 1 else word + 's'


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
        self._expected_call_count = None
        self._call_count = 0

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

        self._call_count += 1
        self._is_satisfied = True

    def is_satisfied(self):
        if self._expected_call_count is None or self._expected_call_count == self._call_count:
            return self._is_satisfied
        return False

    def raise_failure_exception(self):
        """
        Raises a ``MockExpectationError`` with a useful message.

        :raise: ``MockExpectationError``
        """

        raise MockExpectationError(
            "Expected '{}' to be called {}on {!r} with {}, but was not. ({}:{})".format(
                self._method_name,
                self._expected_call_count_string(),
                self._target.obj,
                self._expected_argument_string(),
                self._caller[1],
                self._caller[2]
            )
        )

    def exactly_times(self, n):
        self._expected_call_count = n

    def never(self):
        self.exactly_times(0)

    def once(self):
        self.exactly_times(1)

    def _expected_call_count_string(self):
        if self._expected_call_count is None:
            return ''

        return '{} {} but was called {} {} '.format(
            self._expected_call_count,
            pluralize('time', self._expected_call_count),
            self._call_count,
            pluralize('time', self._call_count)
        )
