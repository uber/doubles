from doubles import allow, Double, teardown


class User(object):
    class_attribute = 'foo'

    def __init__(self, name, age):
        self.name = name
        self._age = age

    @property
    def age(self):
        return self._age

    @classmethod
    def get_first(self):
        return 'First user'

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

    def test_allows_constructor_to_be_stubbed(self):
        user = Double('User')

        allow(User).to_receive('__new__').and_return(user)

        assert User('Alice', 25) is user

    def test_stubs_class_methods(self):
        user = Double('User')

        allow(User).to_receive('get_first').and_return(user)

        assert User.get_first() is user

    def test_stubs_class_attributes(self):
        allow(User).to_receive('class_attribute').and_return('bar')

        assert User.class_attribute() == 'bar'

    def test_stubs_nonexistent_class_methods(self):
        allow(User).to_receive('class_method').and_return('bar')

        assert User.class_method() == 'bar'
