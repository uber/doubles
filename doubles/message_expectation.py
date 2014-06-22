from doubles.message_allowance import MessageAllowance


class MessageExpectation(MessageAllowance):
    def is_satisfied(self):
        return self._called
