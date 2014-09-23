# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import


SIGNALS = {}


class Signal(object):
    def __init__(self, name, handler):
        self.handler = handler
        SIGNALS[name] = self

    def __call__(self, *args, **kwargs):
        return self.handler(*args, **kwargs)

    def __repr__(self):
        return "{module}.{name}".format(
            module=self.handler.__module__,
            name=self.handler.__name__
        )


def register(name, handler):
    Signal(name, handler)
