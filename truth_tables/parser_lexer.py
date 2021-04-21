from string import whitespace
from sly import Lexer, Parser
from .expr_base import Var
from .logic_expr import TRUE, FALSE, Negate, And, Or, Iff, Implies, Xor


class LogicLexer(Lexer):
    tokens = {XOR, OR, IFF, IMPLIES, AND, T, F, NAME}
    ignore = whitespace
    literals = set('~()')

    XOR = r'xor'
    OR = r'or'
    IFF = r'<->'
    IMPLIES = r'->'
    AND = r'and'

    @_(r'T')
    def T(self, t):
        t.value = TRUE
        return t

    @_(r'F')
    def F(self, t):
        t.value = FALSE
        return t

    @_(r'[a-zA-Z_][a-zA-Z0-9_]*')
    def NAME(self, t):
        t.value = Var(t.value)
        return t


class LogicParser(Parser):
    tokens = LogicLexer.tokens

    precedence = (
        ('left', XOR, OR, IFF, IMPLIES),
        ('left', AND),
        ('left', '(', ')'),
        ('right', '~')
    )

    lookup = {
        'xor': Xor,
        'or': Or,
        '<->': Iff,
        '->': Implies,
        'and': And
    }

    def __init__(self):
        self.vars = set()

    @_('expr')
    def statement(self, p):
        return p.expr

    @_(
        'expr XOR expr',
        'expr OR expr',
        'expr IFF expr',
        'expr IMPLIES expr',
        'expr AND expr',
    )
    def expr(self, p):
        return self.lookup[p[1]](p.expr0, p.expr1)

    @_('"(" expr ")"')
    def expr(self, p):
        return p.expr

    @_('"~" expr')
    def expr(self, p):
        return Negate(p.expr)

    @_('T')
    def expr(self, p):
        return p.T

    @_('F')
    def expr(self, p):
        return p.F

    @_('NAME')
    def expr(self, p):
        self.vars.add(p.NAME.name)
        return p.NAME
