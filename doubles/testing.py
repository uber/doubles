class OldStyleUser():
    """An importable dummy class used for testing purposes."""

    class_attribute = 'foo'

    @staticmethod
    def static_method(arg):
        return 'static_method return value: {}'.format(arg)

    @classmethod
    def class_method(cls, arg):
        return 'class_method return value: {}'.format(arg)

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

    def __call__(self, *args):
        return 'user was called'


class User(OldStyleUser, object):
    pass


def top_level_function(arg1, arg2='default'):
    return "{arg1} -- {arg2}".format(
        arg1=arg1,
        arg2=arg2
    )
