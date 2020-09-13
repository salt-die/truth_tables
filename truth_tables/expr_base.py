from collections import defaultdict
from dataclasses import dataclass, field
from types import FunctionType
from typing import Literal


def prefix(body, prefix='   '):
    for line in body:
        yield prefix + line


class CachedType(type):
    """Memoize instances of CachedType"""
    _instances = defaultdict(dict)

    def __call__(cls, *args, **kwargs):
        lookup = *args, *sorted(kwargs.items())
        cls_dict = CachedType._instances[cls]

        if lookup not in cls_dict:
            cls_dict[lookup] = super(CachedType, cls).__call__(*args, **kwargs)

        return cls_dict[lookup]


class Expr:
    pass


@dataclass
class Op(Expr):
    op: str
    func: FunctionType = field(repr=False)


@dataclass
class UnOp(Op):
    """Unary Operator"""
    expr: Expr

    def __str__(self):
        first, *body = str(self.expr).splitlines()
        return '\n'.join(
            (
                f"{type(self).__name__}(op='{self.op}')",
                f' ╰─{first}',
                *prefix(body),
            )
        )

    def __call__(self, **var_values):
        return self.func(self.expr(**var_values))


@dataclass
class BinOp(Op):
    """Binary Operator"""
    l: Expr
    r: Expr

    def __str__(self):
        first, *left_body = str(self.l).splitlines()
        second, *right_body = str(self.r).splitlines()
        return '\n'.join(
            (
                f"{type(self).__name__}(op='{self.op}')",
                f' ├─{first}',
                *prefix(left_body, ' │ '),
                f' ╰─{second}',
                *prefix(right_body),
            )
        )


    def __call__(self, **var_values):
        return self.func(self.l(**var_values), self.r(**var_values))


@dataclass
class Var(Expr, metaclass=CachedType):
    name: str

    def __call__(self, **var_values):
        return var_values[self.name]


@dataclass
class Const(Expr, metaclass=CachedType):
    value: Literal

    def __call__(self, **var_values):
        return self.value
