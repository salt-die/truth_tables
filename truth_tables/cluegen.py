# cluegen.py
#
# Classes generated from type clues.
#
#     https://github.com/dabeaz/cluegen
#
# Author: David Beazley (@dabeaz).
#         http://www.dabeaz.com
#
# Copyright (C) 2018-2020.
#
# Permission is granted to use, copy, and modify this code in any
# manner as long as this copyright message and disclaimer remain in
# the source code.  There is no warranty.  Try to use the code for the
# greater good.

# Modified for use with truth tables - salt-die
# We've removed the need to use annotations at all when cluegen'n a class by passing a defaultdict-like object in
# DatumMeta's __prepare__ method.
from collections import defaultdict
from types import MemberDescriptorType as MemberDescriptor
from .utils import LRU

# Collect all type clues from a class and base classes.
def all_clues(cls):
    clues = { }
    for base in reversed(cls.__mro__):
        clues.update(getattr(base, '__annotations__', { }))
    return clues

# Decorator to define methods of a class as a code generator.
def cluegen(func):
    def __get__(self, instance, cls):
        locs = { }
        code = func(cls)
        exec(code, locs)
        meth = locs[func.__name__]
        setattr(cls, func.__name__, meth)
        return meth.__get__(instance, cls)

    def __set_name__(self, cls, name):
        methods = cls.__dict__.get('_methods', list(cls._methods))
        if '_methods' not in cls.__dict__:
            cls._methods = methods
        cls._methods.append((name, self))

    return type(f'ClueGen_{func.__name__}', (), dict(__get__=__get__, __set_name__=__set_name__))()


class AnnDefaultDict(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self['__annotations__'] = {}

    def __missing__(self, key):
        if key.startswith('__') or key == 'cluegen':
            raise KeyError(key)
        self['__annotations__'][key] = None


class DatumMeta(type):
    def __prepare__(*args):
        return AnnDefaultDict()


class CachedDatum(DatumMeta):
    """Memoize instances of CachedDatum type"""
    _instances = defaultdict(LRU)

    def __call__(cls, *args, **kwargs):
        lookup = *args, *sorted(kwargs.items())
        cls_dict = CachedDatum._instances[cls]

        if lookup not in cls_dict:
            cls_dict[lookup] = super(CachedDatum, cls).__call__(*args, **kwargs)

        return cls_dict[lookup]


# Base class for defining data structures
class DatumBase:
    __slots__ = ()
    _methods = []

    @classmethod
    def __init_subclass__(cls):
        submethods = []
        for name, val in cls._methods:
            if name not in cls.__dict__:
                setattr(cls, name, val)
                submethods.append((name, val))
            elif val is cls.__dict__[name]:
                submethods.append((name, val))

        if submethods != cls._methods:
            cls._methods = submethods


class Datum(DatumBase, metaclass=DatumMeta):
    __slots__ = ()

    @cluegen
    def __init__(cls):
        clues = all_clues(cls)
        args = ', '.join(f'{name}={attr!r}' if hasattr(cls, name) and not isinstance((attr := getattr(cls, name)), MemberDescriptor) else name for name in clues)
        body = '\n'.join(f'   self.{name} = {name}' for name in clues)
        return f'def __init__(self, {args}):\n{body}\n'

    @cluegen
    def __repr__(cls):
        fmt = ', '.join(f'{name}={{self.{name}!r}}' for name in all_clues(cls) if name != 'func')
        return f'def __repr__(self):\n    return f"{{type(self).__name__}}({fmt})"'
