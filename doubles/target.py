from inspect import classify_class_attrs, isclass


class Target(object):
    def __init__(self, obj):
        self.obj = obj
        self.doubled_obj = self._determine_doubled_obj()
        self.doubled_obj_type = self._determine_doubled_obj_type()
        self.attrs = self._generate_attrs()

    def is_class(self):
        return self.doubled_obj == self.doubled_obj_type

    def _determine_doubled_obj(self):
        if hasattr(self.obj, '_doubles_target'):
            return self.obj._doubles_target
        else:
            return self.obj

    def _determine_doubled_obj_type(self):
        if isclass(self.doubled_obj):
            return self.doubled_obj

        return self.doubled_obj.__class__

    def _generate_attrs(self):
        attrs = {}

        for attr in classify_class_attrs(self.doubled_obj_type):
            attrs[attr.name] = attr

        return attrs
