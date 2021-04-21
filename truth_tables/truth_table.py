from itertools import product
from .table_maker import table_maker
from .parser_lexer import LogicLexer, LogicParser


LEXER = LogicLexer()
PARSER = LogicParser()


class TruthTable:
    def __init__(self, *props, binary=False):
        self.props = props
        self.binary = binary

        self.exprs = exprs = tuple(PARSER.parse(LEXER.tokenize(prop)) for prop in self.props)
        self.vars = vars_ = tuple(sorted(PARSER.vars))
        PARSER.vars = set()

        table = []
        for values in product((False, True), repeat=len(vars_)):
            vars_values = dict(zip(vars_, values))
            results = (expr(**vars_values) for expr in self.exprs)
            table.append((*values, *results))
        self.table = tuple(table)

    def __repr__(self):
        props = "', '".join(self.props)
        return f"{type(self).__name__}('{props}')"

    def __str__(self):
        translate = '01' if self.binary else 'FT'
        values = ((translate[i] for i in row) for row in self.table)
        return table_maker(self.vars + self.props, *values)

    @property
    def ast(self):
        """Returns the abstract syntax tree of each proposition as a pretty string.
        """
        return '\n\n'.join(map(str, self.exprs))

    def __iter__(self):
        """An iterator over the propositions of the TruthTable.
        """
        return iter(self.props)

    def __eq__(self, other):
        return self.vars == other.vars and self.table == other.table
