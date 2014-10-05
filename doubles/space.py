from doubles.proxy import Proxy


class Space(object):
    """
    A container object for all the doubles created during the execution of a test case. Maintains
    a one-to-one mapping of target objects and ``Proxy`` objects. Maintained by the ``lifecycle``
    module and not intended to be used directly by other objects.
    """

    def __init__(self):
        self._proxies = {}
        self._is_verified = False
        self.skip_builtin_verification = False

    def proxy_for(self, obj):
        """
        Returns the ``Proxy`` for the target object, creating it if necessary.

        :param object obj: The object that will be doubled.
        :return: The mapped ``Proxy``.
        :rtype: Proxy
        """

        obj_id = id(obj)

        if obj_id not in self._proxies:
            self._proxies[obj_id] = Proxy(obj)

        return self._proxies[obj_id]

    def teardown(self):
        """Restores all doubled objects to their original state."""

        for proxy in self._proxies.values():
            proxy.restore_original_object()

    def verify(self):
        """
        Verifies expectations on all doubled objects.

        :raise: ``MockExpectationError`` on the first expectation that is not satisfied, if any.
        """

        if self._is_verified:
            return

        for proxy in self._proxies.values():
            proxy.verify()

        self._is_verified = True
