from doubles.allowance import Allowance


class Expectation(Allowance):
    """An individual method expectation (mock)."""

    def __init__(self, target, method_name, caller):
        """
        :param Target target: The object owning the method to mock.
        :param str method_name: The name of the method to mock.
        :param tuple caller: Details of the stack frame where the expectation was made.
        """

        super(Expectation, self).__init__(target, method_name, caller)
        self._is_satisfied = False

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

    def satisfy_custom_matcher(self, args, kwargs):
        """Returns a boolean indicating whether or not the mock will accept the provided arguments.

        :param tuple args: A tuple of possition args
        :param dict kwargs: A dictionary of keyword args
        :return: Whether or not the mock accepts the provided arguments.
        :rtype: bool
        """

        is_match = super(Expectation, self).satisfy_custom_matcher(args, kwargs)

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

        super(Expectation, self).raise_failure_exception('Expected')

    def is_satisfied(self):
        """
        Returns a boolean indicating whether or not the double has been satisfied. Stubs are
        always satisfied, but mocks are only satisifed if they've been called as was declared,
        or if call is expected not to happen.

        :return: Whether or not the double is satisfied.
        :rtype: bool
        """

        return self._call_counter.has_correct_call_count() and (
            self._call_counter.never() or self._is_satisfied)
