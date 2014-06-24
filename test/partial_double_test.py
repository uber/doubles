from doubles import allow, teardown


class User(object):
    def __init__(self, name):
        self.name = name

    def get_name(self):
        return self.name


class TestPartialDouble(object):
    def test_stubs_real_object(self):
        user = User('Alice')

        allow(user).to_receive('get_name').and_return('Bob')

        assert user.get_name() == 'Bob'

    def test_restores_original(self):
        user = User('Alice')
        allow(user).to_receive('get_name').and_return('Bob')

        teardown()

        assert user.get_name() == 'Alice'
