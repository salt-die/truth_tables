
from types import FunctionType
from typing import Literal
from .cluegen import Datum, CachedDatum
from .utils import prefix


class Expr(Datum):
    pass


class Op(Expr):
    op, func


class UnOp(Op):
    expr

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
    left, right

    def __str__(self):
        first, *left_body = str(self.left).splitlines()
        second, *right_body = str(self.right).splitlines()
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
        return self.func(self.left(**var_values), self.right(**var_values))


class Var(Expr, metaclass=CachedDatum):
    name

    def __call__(self, **var_values):
        return var_values[self.name]


class Const(Expr, metaclass=CachedDatum):
    value

    def __call__(self, **var_values):
        return self.value
