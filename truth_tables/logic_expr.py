from functools import partial
from .expr_base import Const, UnOp, BinOp


__all__ = 'TRUE', 'FALSE', 'Negate', 'And', 'Or', 'Implies', 'Iff', 'Xor'

TRUE = Const(True)
FALSE = Const(False)

Negate = partial(UnOp, '~', lambda p: not p)

And = partial(BinOp, 'and', lambda p, q: p and q)
Or = partial(BinOp, 'or', lambda p, q: p or q)
Implies = partial(BinOp, '->', lambda p, q: not p or q)
Iff = partial(BinOp, '<->', lambda p, q: p == q)
Xor = partial(BinOp, 'xor', lambda p, q: p != q)
