import re

from doubles import Double


class TestDouble(object):
    def test_can_be_unnamed(self):
        subject = Double()

        pattern = re.compile(r'<Double object at 0x[0-9a-f]{9}>')

        assert pattern.match(repr(subject))

    def test_can_be_named(self):
        subject = Double('foo')

        pattern = re.compile(r"<Double of 'foo' object at 0x[0-9a-f]{9}>")

        assert pattern.match(repr(subject))
