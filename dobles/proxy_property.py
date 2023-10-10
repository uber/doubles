class ProxyProperty(property):
    def __init__(self, name, original):
        """
        :param str name: name of the doubled property
        :param property original: the original property
        """
        self._name = name
        self._original = original

    def __get__(self, obj, objtype=None):
        if self._name in obj.__dict__:
            return obj.__dict__[self._name].__get__(obj, objtype)
        return self._original.__get__(obj, objtype)
