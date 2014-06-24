from doubles import allow, teardown


class User(object):
    def __init__(self, name, age):
        self.name = name
        self._age = age

    @property
    def age(self):
        return self._age

    def get_name(self):
        return self.name


class TestPartialDouble(object):
    def test_stubs_real_object(self):
        user = User('Alice', 25)

        allow(user).to_receive('get_name').and_return('Bob')

        assert user.get_name() == 'Bob'

    def test_restores_original(self):
        user = User('Alice', 25)
        allow(user).to_receive('get_name').and_return('Bob')

        teardown()

        assert user.get_name() == 'Alice'

    def test_only_affects_stubbed_method(self):
        user = User('Alice', 25)

        allow(user).to_receive('get_name').and_return('Bob')

        assert user.age == 25
