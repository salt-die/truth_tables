from abc import ABC, abstractmethod
from typing import Literal

import lark


def prefix(body: list[str], prefix: str) -> str:
    """Prefix each line in ``body`` with ``prefix``."""
    if body:
        return "\n".join(prefix + line for line in body) + "\n"
    return ""


class Expr(ABC):
    @abstractmethod
    def __str__(self):
        """Return a pretty-printed string representation of the expression as an ast."""

    @abstractmethod
    def eval(self, symbols: dict[str, bool]) -> bool:
        """Evaluate the expression given a dictionary of symbols to their values."""


class LiteralFalse(Expr):
    def __str__(self):
        return "LiteralFalse"

    def eval(self, _: dict[str, bool]) -> Literal[False]:
        return False


class LiteralTrue(Expr):
    def __str__(self):
        return "LiteralTrue"

    def eval(self, _: dict[str, bool]) -> Literal[True]:
        return True


class Variable(Expr):
    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return f"Variable({self.name!r})"

    def eval(self, symbols: dict[str, bool]) -> bool:
        return symbols[self.name]


class Negate(Expr):
    def __init__(self, value: Expr):
        self.value = value

    def __str__(self):
        first, *body = str(self.value).splitlines()
        return f"Negate\n" f"╰─{first}\n" f"{prefix(body, '  ')}"

    def eval(self, symbols: dict[str, bool]) -> bool:
        return not self.value.eval(symbols)


class BinOp(Expr):
    def __init__(self, left: Expr, right: Expr):
        self.left = left
        self.right = right

    def __str__(self):
        first, *left_body = str(self.left).splitlines()
        second, *right_body = str(self.right).splitlines()
        return (
            f"{type(self).__name__}\n"
            f"├─{first}\n"
            f"{prefix(left_body, '│ ')}"
            f"╰─{second}\n"
            f"{prefix(right_body, '  ')}"
        )


class And(BinOp):
    def eval(self, symbols: dict[str, bool]) -> bool:
        return self.left.eval(symbols) and self.right.eval(symbols)


class Iff(BinOp):
    def eval(self, symbols: dict[str, bool]) -> bool:
        return self.left.eval(symbols) == self.right.eval(symbols)


class Implies(BinOp):
    def eval(self, symbols: dict[str, bool]) -> bool:
        return not self.left.eval(symbols) or self.right.eval(symbols)


class Or(BinOp):
    def eval(self, symbols: dict[str, bool]) -> bool:
        return self.left.eval(symbols) or self.right.eval(symbols)


class Xor(BinOp):
    def eval(self, symbols: dict[str, bool]) -> bool:
        return self.left.eval(symbols) != self.right.eval(symbols)


@lark.v_args(inline=True)
class AST_Transformer(lark.Transformer):
    false = LiteralFalse
    true = LiteralTrue
    neg = Negate
    and_ = And
    iff = Iff
    implies = Implies
    or_ = Or
    xor = Xor

    def __init__(self) -> None:
        self.vars = set()

    def var(self, token: lark.lexer.Token) -> Variable:
        """
        Transform a ``var`` token into a Variable expression and add it's name to
        :attr:``vars``.
        """
        name = str(token)
        self.vars.add(name)
        return Variable(name)


GRAMMAR = r"""\
?exp: factor
    | exp ("or" | "|") factor                        -> or_
    | exp ("implies" | "->") factor                  -> implies
    | exp ("iff" | "<->") factor                     -> iff
    | exp ("xor" | "^") factor                       -> xor
?factor: term
    | factor ("and" | "&") term                      -> and_
?term: "F"                                           -> false
    | "T"                                            -> true
    | /(?!(?:or|implies|iff|xor|and|F|T))[^\W\d]\w*/ -> var
    | "(" exp ")"
    | ("not" | "~") term                             -> neg

%import common.WS
%ignore WS
"""
