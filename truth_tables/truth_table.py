from itertools import product
from .table_maker import table_maker
from .parser_lexer import LogicLexer, LogicParser


LEXER = LogicLexer()
PARSER = LogicParser()


class TruthTable:
    def __init__(self, *props):
        self.props = props

        PARSER.vars = set()
        self.exprs = exprs = tuple(PARSER.parse(LEXER.tokenize(prop)) for prop in self.props)
        self.vars = vars_ = tuple(sorted(PARSER.vars))

        table = []
        for values in product((False, True), repeat=len(vars_)):
            vars_values = dict(zip(vars_, values))
            results = (expr(**vars_values) for expr in self.exprs)
            table.append((*values, *results))
        self.table = tuple(table)

    def display(self, binary=False):
        translate = '01' if binary else 'FT'
        values = ((translate[i] for i in row) for row in self.table)
        table = table_maker(self.vars + self.props, *values)
        print(table)

    def show_ast(self):
        print(*map(str, self.exprs), sep='\n\n')

    def __iter__(self):
        return iter(self.props)

    def __repr__(self):
        return f'{type(self).__name__}({str(self.props)[1:-2]})'

    def __eq__(self, other):
        return self.vars == other.vars and self.table == other.table


def tt(*props, binary=False):
    TruthTable(*props).display(binary)
