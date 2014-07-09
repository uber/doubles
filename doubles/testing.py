class User(object):
    """An importable dummy class used for testing purposes."""

    class_attribute = 'foo'

    @staticmethod
    def static_method():
        return 'static_method return value'

    @classmethod
    def class_method(cls):
        return 'class_method return value'

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def get_name(self):
        return self.name

    def instance_method(self):
        return 'instance_method return value'

    def method_with_varargs(self, *args):
        return 'method_with_varargs return value'

    def method_with_default_args(self, foo, bar='baz'):
        return 'method_with_default_args return value'

    def method_with_varkwargs(self, **kwargs):
        return 'method_with_varkwargs return value'

    def method_with_positional_arguments(self, foo):
        return 'method_with_positional_arguments return value'

    @property
    def some_property(self):
        return 'some_property return value'
