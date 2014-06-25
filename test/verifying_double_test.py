import re

from doubles.verifying_doubles.verifying_double import VerifyingDouble


class TestRepr(object):
    def test_displays_correct_class_name(self):
        subject = VerifyingDouble('foo')

        pattern = re.compile(r"<VerifyingDouble of 'foo' object at 0x[0-9a-f]{9}>")

        assert pattern.match(repr(subject))
