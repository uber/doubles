from mock import Mock, patch

from doubles.space import Space


class TestSetupAndTeardown(object):
    def teardown(self):
        Space.teardown()

    def test_has_no_initial_current(self):
        assert Space.current is None

    def test_creates_and_stores_a_new_space(self):
        Space.setup()

        assert isinstance(Space.current, Space)

    def test_deletes_the_space(self):
        Space.setup()
        Space.teardown()

        assert Space.current is None


@patch('doubles.space.Proxy')
class TestVerify(object):
    def setup(self):
        Space.setup()

    def test_verifies_all_proxies(self, Proxy):
        Proxy.side_effect = iter([Mock(), Mock(), Mock()])
        objects = [object(), object(), object()]
        proxies = [Space.current.proxy_for(obj) for obj in objects]

        Space.verify()

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
