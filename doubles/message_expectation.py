from doubles.message_allowance import MessageAllowance


class MessageExpectation(MessageAllowance):
    def __init__(self, obj, method_name):
        super(MessageExpectation, self).__init__(obj, method_name)
        self._is_satisfied = False

    def satisfy_any_args_match(self):
        is_match = super(MessageExpectation, self).satisfy_any_args_match()

        if is_match:
            self._satisfy()

        return is_match

    def satisfy_exact_match(self, args, kwargs):
        is_match = super(MessageExpectation, self).satisfy_exact_match(args, kwargs)

        if is_match:
            self._satisfy()

        return is_match

    def _satisfy(self):
        self._is_satisfied = True
