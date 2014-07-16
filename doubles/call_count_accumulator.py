pluralize = lambda w, n: w if n == 1 else w + 's'


class CallCountAccumulator(object):
    def __init__(self):
        self._call_count = 0

    def set_exact(self, n):
        self._exact = n

    def set_minimum(self, n):
        self._minimum = n

    def set_maximum(self, n):
        self._maximum = n

    def has_too_many_calls(self):
        if self.has_exact and self._call_count > self._exact:
            return True
        if self.has_maximum and self._call_count > self._maximum:
            return True
        return False

    def has_too_few_calls(self):
        if self.has_exact and self._call_count < self._exact:
            return True
        if self.has_minimum and self._call_count < self._minimum:
            return True
        return False

    def has_incorrect_call_count(self):
        return self.has_too_few_calls() or self.has_too_many_calls()

    def has_correct_call_count(self):
        return not self.has_incorrect_call_count()

    def called(self):
        self._call_count += 1
        return self

    @property
    def count(self):
        return self._call_count

    @property
    def has_minimum(self):
        return getattr(self, '_minimum', None) is not None

    @property
    def has_maximum(self):
        return getattr(self, '_maximum', None) is not None

    @property
    def has_exact(self):
        return getattr(self, '_exact', None) is not None

    def error_string(self):
        if self.has_correct_call_count():
            return ''

        return '{} but was called {} {} '.format(
            self._call_count_restriction_string(),
            self.count,
            pluralize('time', self.count)
        )

    def _call_count_restriction_string(self):
        if self.has_minimum:
            string = 'at least '
            value = self._minimum
        elif self.has_maximum:
            string = 'at most '
            value = self._maximum
        elif self.has_exact:
            string = ''
            value = self._exact
        else:
            return ''

        return (string + '{} {}').format(
            value,
            pluralize('time', value)
        )
