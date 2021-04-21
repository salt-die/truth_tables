"""`q` for `q`uick class definitions!  In the spirit of cluegen, but with no need of annotations.

class Point(q):
    x, y

This is all you need to get the __init__ and __repr__ one expects.
No support for default values here, for a more complete version check https://github.com/salt-die/Snippets/blob/master/q.py
"""
from collections import defaultdict
from .utils import LRU


class AutoDict(dict):
    def __init__(self):
        super().__init__(__fields__={})  # Using a dict as an ordered-set

    def __missing__(self, key):
        if key.startswith('__'):
            raise KeyError(key)

        self['__fields__'][key] = None


class qMeta(type):
    def __prepare__(name, bases):
        return AutoDict()

    def __new__(meta, name, bases, methods):
        attrs = {}
        for base in bases:
            attrs |= getattr(base, '__fields__', {})
        attrs |= methods['__fields__']

        if attrs:
            init_header = f'def __init__(self, { ", ".join(attrs)}):\n'
            init_body = '\n'.join(f'    self.{attr}={attr}' for attr in attrs)
            exec(init_header + init_body, methods)

        repr_header = 'def __repr__(self):\n'
        args = ', '.join(f'{{self.{attr}!r}}' for attr in attrs)
        repr_body = f'    return f"{name}({args})"'
        exec(repr_header + repr_body, methods)

        return super().__new__(meta, name, bases, methods)


class qCached(qMeta):
    """Memoize instances of qCached type.
    """
    _class_to_cache = defaultdict(LRU)

    def __call__(cls, arg):
        cache = qCached._class_to_cache[cls]

        if arg not in cache:
            cache[arg] = super().__call__(arg)

        return cache[arg]


class q(metaclass=qMeta):
    pass
