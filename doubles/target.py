from inspect import classify_class_attrs, isclass, ismodule, isfunction, getmembers
from collections import namedtuple

ModuleAttribute = namedtuple('ModuleAttribute', ['object', 'kind'])


class Target(object):
    """
    A wrapper around an object that owns methods to be doubled. Provides additional introspection
    such as the class and the kind (method, class, property, etc.)
    """

    def __init__(self, obj):
        """
        :param object obj: The real target object.
        """

        self.obj = obj
        self.doubled_obj = self._determine_doubled_obj()
        self.doubled_obj_type = self._determine_doubled_obj_type()
        self.attrs = self._generate_attrs()

    def is_class(self):
        """
        Determines if the object is a class.

        :return: True if the object is a class, False otherwise.
        :rtype: bool
        """

        return self.doubled_obj == self.doubled_obj_type

    def _determine_doubled_obj(self):
        """
        Returns the object that should be treated as the target object. For partial doubles, this
        will be the same as ``self.obj``, but for pure doubles, it's pulled from the special
        ``_doubles_target`` attribute.

        :return: The object to be doubled.
        :rtype: object
        """

        if hasattr(self.obj, '_doubles_target'):
            return self.obj._doubles_target
        else:
            return self.obj

    def _determine_doubled_obj_type(self):
        """
        Returns the type (class) of the target object.

        :return: The type (class) of the target.
        :rtype: type, classobj
        """

        if isclass(self.doubled_obj) or ismodule(self.doubled_obj):
            return self.doubled_obj

        return self.doubled_obj.__class__

    def _generate_attrs(self):
        """
        Uses ``inspect.classify_class_attrs`` to get several important details about each attribute
        on the target object.

        :return: The attribute details dict.
        :rtype: dict
        """
        attrs = {}

        if ismodule(self.doubled_obj):
            for name, func in getmembers(self.doubled_obj, isfunction):
                attrs[name] = ModuleAttribute(func, 'toplevel')
        else:
            for attr in classify_class_attrs(self.doubled_obj_type):
                attrs[attr.name] = attr

        return attrs
