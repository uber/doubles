from doubles.proxy import Proxy


class Space(object):
    current = None

    @classmethod
    def setup(cls):
        cls.current = cls()

    @classmethod
    def teardown(cls):
        cls.current = None

    def __init__(self):
        self._proxies = {}

    def proxy_for(self, obj):
        return self._proxies.setdefault(id(obj), Proxy(obj))
