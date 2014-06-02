class Proxy(object):
    def __init__(self, obj):
        self._obj = obj

    def verify(self):
        pass

    def __repr__(self):
        return "<Proxy({!r})>".format(self._obj)
