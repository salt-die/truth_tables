from .q import q

def prefix(body, prefix):
    """Yields each line of `body` prefixed with `prefix`.
    """
    for line in body:
        yield prefix + line


class Expr(q):
    pass


class Op(Expr):
    op = lambda: None


class UnOp(Op):
    expr

    def __str__(self):
        first, *body = str(self.expr).splitlines()
        return '\n'.join(
            (
                f"{type(self).__name__}",
                f'╰─{first}',
                *prefix(body, '  '),
            )
        )

    def __call__(self, **var_values):
        return type(self).op(self.expr(**var_values))


class BinOp(Op):
    left, right

    def __str__(self):
        first, *left_body = str(self.left).splitlines()
        second, *right_body = str(self.right).splitlines()
        return '\n'.join(
            (
                f"{type(self).__name__}",
                f'├─{first}',
                *prefix(left_body, '│ '),
                f'╰─{second}',
                *prefix(right_body, '  '),
            )
        )

    def __call__(self, **var_values):
        return type(self).op(self.left(**var_values), self.right(**var_values))


class Var(Expr):
    name

    def __call__(self, **var_values):
        return var_values[self.name]


class Const(Expr):
    value

    def __call__(self, **var_values):
        return self.value
