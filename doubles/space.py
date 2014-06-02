class Space(object):
    current = None

    @classmethod
    def setup(cls):
        cls.current = cls()

    @classmethod
    def teardown(cls):
        cls.current = None
