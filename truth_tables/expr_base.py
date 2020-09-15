
from types import FunctionType
from typing import Literal
from .cluegen import Datum
from .utils import CachedType, prefix


class Expr(Datum):
    pass


class Op(Expr):
    op: str
    func: FunctionType


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


class Var(Expr, metaclass=CachedType):
    name: str

    def __call__(self, **var_values):
        return var_values[self.name]


class Const(Expr, metaclass=CachedType):
    value: Literal

    def __call__(self, **var_values):
        return self.value
