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
        super().__init__(__auto_attrs__=[])

    def __missing__(self, key):
        if key.startswith('__'):
            raise KeyError(key)

        self['__auto_attrs__'].append(key)


class qMeta(type):
    def __prepare__(name, bases):
        return AutoDict()

    def __new__(meta, name, bases, methods):
        if attrs := methods.pop('__auto_attrs__'):
            init_header = f'def __init__(self, { ", ".join(attrs)}):\n'
            init_body = '\n'.join(f'    self.{name}={name}' for name in attrs)
            exec(init_header + init_body, methods)

        repr_header = 'def __repr__(self):\n'
        repr_body = '    return f"{{type(self).__name__}}({})"'.format(', '.join(f'{name}={{self.{name}!r}}' for name in attrs))
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
