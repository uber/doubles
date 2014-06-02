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
