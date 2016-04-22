def pluralize(word, count):
    return word if count == 1 else word + 's'


class CallCountAccumulator(object):
    def __init__(self):
        self._call_count = 0

    def set_exact(self, n):
        """Set an exact call count expectation

        :param integer n:
        """

        self._exact = n

    def set_minimum(self, n):
        """Set a minimum call count expectation

        :param integer n:
        """

        self._minimum = n

    def set_maximum(self, n):
        """Set a maximum call count expectation

        :param integer n:
        """

        self._maximum = n

    def has_too_many_calls(self):
        """Test if there have been too many calls

        :rtype boolean
        """

        if self.has_exact and self._call_count > self._exact:
            return True
        if self.has_maximum and self._call_count > self._maximum:
            return True
        return False

    def has_too_few_calls(self):
        """Test if there have not been enough calls

        :rtype boolean
        """

        if self.has_exact and self._call_count < self._exact:
            return True
        if self.has_minimum and self._call_count < self._minimum:
            return True
        return False

    def has_incorrect_call_count(self):
        """Test if there have not been a valid number of calls

        :rtype boolean
        """

        return self.has_too_few_calls() or self.has_too_many_calls()

    def has_correct_call_count(self):
        """Test if there have been a valid number of calls

        :rtype boolean
        """

        return not self.has_incorrect_call_count()

    def never(self):
        """Test if the number of expect is 0

        :rtype: boolean
        """

        return self.has_exact and self._exact == 0

    def called(self):
        """Increment the call count"""

        self._call_count += 1
        return self

    @property
    def count(self):
        """Extract the current call count

        :rtype integer
        """

        return self._call_count

    @property
    def has_minimum(self):
        """Test if self has a minimum call count set

        :rtype boolean
        """

        return getattr(self, '_minimum', None) is not None

    @property
    def has_maximum(self):
        """Test if self has a maximum call count set

        :rtype boolean
        """

        return getattr(self, '_maximum', None) is not None

    @property
    def has_exact(self):
        """Test if self has an exact call count set

        :rtype boolean
        """

        return getattr(self, '_exact', None) is not None

    def _restriction_string(self):
        """Get a string explaining the expectation currently set

        e.g `at least 5 times`, `at most 1 time`, or `2 times`

        :rtype string
        """

        if self.has_minimum:
            string = 'at least '
            value = self._minimum
        elif self.has_maximum:
            string = 'at most '
            value = self._maximum
        elif self.has_exact:
            string = ''
            value = self._exact

        return (string + '{} {}').format(
            value,
            pluralize('time', value)
        )

    def error_string(self):
        """Returns a well formed error message

        e.g at least 5 times but was called 4 times

        :rtype string
        """

        if self.has_correct_call_count():
            return ''

        return '{} instead of {} {} '.format(
            self._restriction_string(),
            self.count,
            pluralize('time', self.count)
        )
