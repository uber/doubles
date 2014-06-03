from doubles.proxy import Proxy


class Space(object):
    def __init__(self):
        self._proxies = {}

    def proxy_for(self, obj):
        return self._proxies.setdefault(id(obj), Proxy(obj))

    def verify(self):
        for proxy in self._proxies.values():
            proxy.verify()
