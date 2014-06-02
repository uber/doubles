from doubles.proxy import Proxy


class Space(object):
    current = None

    @classmethod
    def setup(cls):
        cls.current = cls()

    @classmethod
    def teardown(cls):
        cls.current = None

    @classmethod
    def verify(cls):
        cls.current.verify_each()

    def __init__(self):
        self._proxies = {}

    def proxy_for(self, obj):
        return self._proxies.setdefault(id(obj), Proxy(obj))

    def verify_each(self):
        for proxy in self._proxies.values():
            proxy.verify()
