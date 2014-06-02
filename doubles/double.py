class Double(object):
    def __init__(self, target=None):
        self.target = target

    def __repr__(self):
        class_name = self.__class__.__name__

        if self.target is None:
            return '{} (unnamed)'.format(class_name)
        else:
            return '{}({!r})'.format(class_name, self.target)
