from doubles.allowance import Allowance
from doubles.exceptions import MockExpectationError


class Expectation(Allowance):
    """An individual method expectation (mock). Provides the same interface as ``Allowance``."""

    def __init__(self, obj, method_name, caller):
        super(Expectation, self).__init__(obj, method_name)
        self._is_satisfied = False
        self._caller = caller

    def satisfy_any_args_match(self):
        is_match = super(Expectation, self).satisfy_any_args_match()

        if is_match:
            self._satisfy()

        return is_match

    def satisfy_exact_match(self, args, kwargs):
        is_match = super(Expectation, self).satisfy_exact_match(args, kwargs)

        if is_match:
            self._satisfy()

        return is_match

    def _satisfy(self):
        self._is_satisfied = True

    def raise_failure_exception(self):
        raise MockExpectationError(
            "Expected '{}' to be called on {!r} with {}, but was not. ({}:{})".format(
                self._method_name,
                self._target.obj,
                self._expected_argument_string(),
                self._caller[1],
                self._caller[2]
            )
        )
