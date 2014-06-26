class User(object):
    """An importable dummy class used for testing purposes."""

    class_attribute = 'foo'

    @staticmethod
    def static_method():
        pass

    @classmethod
    def class_method(cls):
        return 'class method'

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def get_name(self):
        return self.name

    def instance_method(self):
        pass

    def method_with_varargs(self, *args):
        pass

    def method_with_default_args(self, foo, bar='baz'):
        pass

    def method_with_varkwargs(self, **kwargs):
        pass

    def method_with_positional_arguments(self, foo):
        pass
