from .expr_base import Const, UnOp, BinOp

TRUE = Const(True)
FALSE = Const(False)


class Negate(UnOp):
    op = lambda p : not p

# We must resist the urge to do this:
# from .q import qMeta

# binops= {
#     'And'    : lambda p, q: p and q,
#     'Or'     : lambda p, q: p or q,
#     'Implies': lambda p, q: not p or q,
#     'Iff'    : lambda p, q: p == q,
#     'Xor'    : lambda p, q: p != q,
# }

# for name, op in binops.items():
#     globals()[name] = qMeta(name, (BinOp, ), {'op': op, '__fields__': {}})

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
