from doubles.instance_double import InstanceDouble
from doubles.class_double import ClassDouble


class InstanceDoubleFactory(ClassDouble):
    def __init__(self, path, *values, **kwargs):
        self._path = path
        self._instances = []
        if values:
            values = list(values)
            last_value = values.pop()
            self._generator = lambda: values.pop(0) if values else last_value
        else:
            self._generator = lambda: InstanceDouble(self._path)

        super(InstanceDoubleFactory, self).__init__(path, **kwargs)

    def __call__(self, *args, **kwargs):
        instance = self._generator()
        if not self._instances or not self._instances[-1] is instance:
            self._instances.append(instance)
        return instance

    @property
    def instances(self):
        return self._instances
