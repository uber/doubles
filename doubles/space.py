from doubles.proxy import Proxy


class Space(object):
    def __init__(self):
        self._proxies = {}
        self._is_verified = False

    def proxy_for(self, obj):
        obj_id = id(obj)

        if obj_id not in self._proxies:
            self._proxies[obj_id] = Proxy(obj)

        return self._proxies[obj_id]

    def teardown(self):
        for proxy in self._proxies.values():
            proxy.restore_original_object()

    def verify(self):
        if self._is_verified:
            return

        self._is_verified = True

        for proxy in self._proxies.values():
            proxy.verify()
