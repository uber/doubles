class OldStyleEmptyClass():
    pass


class EmptyClass(OldStyleEmptyClass, object):
    pass


class OldStyleUser():
    """An importable dummy class used for testing purposes."""

    class_attribute = 'foo'
    callable_class_attribute = classmethod(lambda cls: 'dummy result')

    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.callable_instance_attribute = lambda: 'dummy result'

    @staticmethod
    def static_method(arg):
        return 'static_method return value: {}'.format(arg)

    @classmethod
    def class_method(cls, arg):
        return 'class_method return value: {}'.format(arg)

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

    def method_with_doc(self):
        """A basic method of OldStyleUser to illustrate existance of a docstring"""
        return

    @property
    def some_property(self):
        return 'some_property return value'

    def __call__(self, *args):
        return 'user was called'

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass


class User(OldStyleUser, object):
    pass


class UserWithCustomNew(User):
    def __new__(cls, name, age):
        instance = User.__new__(cls)
        instance.name_set_in__new__ = name
        return instance


def top_level_function(arg1, arg2='default'):
    return "{arg1} -- {arg2}".format(
        arg1=arg1,
        arg2=arg2
    )


def top_level_function_that_creates_an_instance():
    return User('Bob Barker', 100), OldStyleUser('Bob Barker', 100)


class ClassWithGetAttr(object):
    def __init__(self):
        self.attr = 'attr'

    def method(self):
        return 'method'

    def __getattr__(self, name):
        return 'attr {name}'.format(name=name)


class Callable(object):
    def __call__(self, arg1):
        return arg1


def return_callable(func):
    return Callable()


def decorate_me(func):
    def decorated(arg1):
        return '{arg1} decorated'.format(arg1=arg1)

    return decorated


@return_callable
def decorated_function_callable(arg1):
    return arg1


@decorate_me
def decorated_function(arg1):
    return arg1

callable_variable = Callable()

class_method = User.class_method
instance_method = User('Bob', 25).get_name


class NeverEquals(object):
    def __eq__(self, other):
        return False


class AlwaysEquals(object):
    def __eq__(self, other):
        return True


class DictSubClass(dict):
    pass


class ListSubClass(list):
    pass


class SetSubClass(set):
    pass


class TupleSubClass(tuple):
    pass
