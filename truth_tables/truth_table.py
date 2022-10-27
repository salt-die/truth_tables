from itertools import product
from pathlib import Path

import lark

def _create_table(expressions, *rows):
    BOX_CHARS = '┌┬┐', '├┼┤', '└┴┘'
    HORIZONTAL = '─'

    lengths = tuple(map(len, expressions))

    # Pad the length of items in each column
    rows = [[f'{item:^{length}}' for item, length in zip(row, lengths)] for row in rows]
    rows.insert(0, list(expressions))

    # Make separators
    horizontals = tuple(HORIZONTAL * (length + 2) for length in lengths)
    top, title, bottom = (f'{l}{m.join(horizontals)}{r}' for l, m, r in BOX_CHARS)

    table = [f'│ {" │ ".join(row)} │' for row in rows]
    table.insert(0, top)
    table.insert(2, title)
    table.append(bottom)
    table = '\n'.join(table)
    return table

@lark.v_args(inline=True)
class _AST_Transformer(lark.Transformer):
    from ._ast import false, true, var_, neg, and_, iff, implies, or_, xor

    def __init__(self):
        self.vars = {}

    def var(self, name):
        name = str(name)
        if name not in self.vars:
            self.vars[name] = self.var_(name)
        return self.vars[name]

_GRAMMAR = (Path(__file__).parent / "grammar.lark").read_text()
_TRANSFORMER = _AST_Transformer()
_PARSER = lark.Lark(_GRAMMAR, parser="lalr", start="exp", transformer=_TRANSFORMER)


class TruthTable:
    def __init__(self, *props, binary=False):
        self.props = props
        self.binary = binary
        self.exprs = tuple(_PARSER.parse(prop) for prop in self.props)
        self.vars = tuple(sorted(_TRANSFORMER.vars))
        _TRANSFORMER.vars.clear()

        table = []
        for values in product((False, True), repeat=len(self.vars)):
            symbols = dict(zip(self.vars, values))
            results = (expr.eval(symbols) for expr in self.exprs)
            table.append((*values, *results))
        self.table = tuple(table)

    def __repr__(self):
        return f"{type(self).__name__}({', '.join(repr(prop) for prop in self.props)}, binary={self.binary})"

    def __str__(self):
        translate = '01' if self.binary else 'FT'
        values = ((translate[i] for i in row) for row in self.table)
        return _create_table(self.vars + self.props, *values)

    @property
    def ast(self):
        """Returns the abstract syntax tree of each proposition as a pretty string.
        """
        return '\n\n'.join(map(str, self.exprs))

    def __eq__(self, other):
        return self.vars == other.vars and self.table == other.table
