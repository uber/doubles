class MessageAllowance(object):
    def __init__(self, verify=False):
        self.return_value = None

    def and_return(self, return_value):
        self.return_value = return_value
