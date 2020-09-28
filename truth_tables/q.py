"""`q` for `q`uick class definitions!  In the spirit of cluegen, but with no need of annotations.

class Point(q):
    x, y

This is all you need to get the __init__ and __repr__ one expects.
No support for default values here, for a more complete version check https://github.com/salt-die/Snippets/blob/master/q.py
"""
from collections import defaultdict
from .utils import LRU


NO_DEFAULT = object()


class AutoDict(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        super().__setitem__('__auto_attrs__', [])

    def __missing__(self, key):
        if key.startswith('__'):
            raise KeyError(key)

        self['__auto_attrs__'].append(key)


class qMeta(type):
    def __prepare__(name, bases):
        return AutoDict()


class qCached(qMeta):
    """Memoize instances of qDatum type"""
    _instances = defaultdict(LRU)

    def __call__(cls, *args, **kwargs):
        lookup = *args, *sorted(kwargs.items())
        cls_dict = qCached._instances[cls]

        if lookup not in cls_dict:
            cls_dict[lookup] = super().__call__(*args, **kwargs)

        return cls_dict[lookup]


class q(metaclass=qMeta):
    def __init_subclass__(cls):
        attrs = [attr for c in reversed(cls.__mro__) for attr in getattr(c, '__auto_attrs__', [])]

        args = (', ' if attrs else '') + ', '.join(attrs)

        init_header = f'def __init__(self{args}):\n'
        init_body = '\n'.join(f'    self.{name}={name}' for name in attrs) if attrs else '    pass'

        repr_header = 'def __repr__(self):\n'
        repr_body = '    return f"{{type(self).__name__}}({})"'.format(', '.join(f'{name}={{self.{name}}}' for name in attrs if name != 'func'))

        loc = {}
        exec(init_header + init_body, loc)
        exec(repr_header + repr_body, loc)
        cls.__init__ = loc['__init__']
        cls.__repr__ = loc['__repr__']
