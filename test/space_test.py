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
