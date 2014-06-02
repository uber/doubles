class Proxy(object):
    def __init__(self, obj):
        self._obj = obj

    def __repr__(self):
        return "<Proxy({!r})>".format(self._obj)
