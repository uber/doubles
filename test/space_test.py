from mock import Mock, patch

from doubles.space import Space


@patch('doubles.space.Proxy')
class TestVerify(object):
    def test_verifies_all_proxies(self, Proxy):
        Proxy.side_effect = iter([Mock(), Mock(), Mock()])
        space = Space()
        objects = [object(), object(), object()]
        proxies = [space.proxy_for(obj) for obj in objects]

        space.verify()

        for proxy in proxies:
            assert proxy.verify.call_count == 1


class TestProxyFor(object):
    def test_creates_new_proxies(self):
        space = Space()
        subject = space.proxy_for('some object')

        assert repr(subject) == "<Proxy('some object')>"

    def test_retrieves_existing_proxies(self):
        space = Space()
        initial_proxy = space.proxy_for('some object')
        retrieved_proxy = space.proxy_for('some object')

        assert initial_proxy is retrieved_proxy
