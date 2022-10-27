def prefix(body: list[str], prefix: str) -> str:
    if body:
        return "\n".join(prefix + line for line in body) + "\n"
    return ""


class Expr:
    def eval(self, symbols: dict[str, bool]) -> bool:
        raise NotImplementedError


class false(Expr):
    def __repr__(self):
        return f"false"

    def eval(self, symbols: dict[str, bool]) -> bool:
        return False

class true(Expr):
    def __repr__(self):
        return f"true"

    def eval(self, symbols: dict[str, bool]) -> bool:
        return True

class var_(Expr):
    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f"Var({self.name!r})"

    def eval(self, symbols: dict[str, bool]) -> bool:
        return symbols[self.name]


class neg(Expr):
    def __init__(self, value: Expr):
        self.value = value

    def __str__(self):
        first, *body = str(self.value).splitlines()
        return (
            f"Negate\n"
            f"╰─{first}\n"
            f"{prefix(body, '  ')}"
        )

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
            f"{self._name}\n"
            f"├─{first}\n"
            f"{prefix(left_body, '│ ')}"
            f"╰─{second}\n"
            f"{prefix(right_body, '  ')}"
        )


class and_(BinOp):
    _name = "And"

    def eval(self, symbols: dict[str, bool]) -> bool:
        return self.left.eval(symbols) and self.right.eval(symbols)


class iff(BinOp):
    _name = "Iff"

    def eval(self, symbols: dict[str, bool]) -> bool:
        return self.left.eval(symbols) == self.right.eval(symbols)


class implies(BinOp):
    _name = "Implies"

    def eval(self, symbols: dict[str, bool]) -> bool:
        return not self.left.eval(symbols) or self.right.eval(symbols)


class or_(BinOp):
    _name = "Or"

    def eval(self, symbols: dict[str, bool]) -> bool:
        return self.left.eval(symbols) or self.right.eval(symbols)


class xor(BinOp):
    _name = "Xor"

    def eval(self, symbols: dict[str, bool]) -> bool:
        return self.left.eval(symbols) != self.right.eval(symbols)
