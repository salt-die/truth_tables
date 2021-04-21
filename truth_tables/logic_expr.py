from .expr_base import Const, UnOp, BinOp

TRUE = Const(True)
FALSE = Const(False)


class Negate(UnOp):
    op = lambda p : not p


class And(BinOp):
    op = lambda p, q: p and q


class Or(BinOp):
    op = lambda p, q: p or q


class Implies(BinOp):
    op = lambda p, q: not p or q


class Iff(BinOp):
    op = lambda p, q: p == q


class Xor(BinOp):
    op = lambda p, q: p != q
