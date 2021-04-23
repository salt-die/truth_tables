from string import whitespace
from sly import Lexer, Parser
from .expr_base import Var
from .logic_expr import TRUE, FALSE, Negate, And, Or, Iff, Implies, Xor


class LogicLexer(Lexer):
    tokens = { NOT, AND, OR, IMPLIES, IFF, XOR, T, F, NAME}
    ignore = whitespace
    literals = { '(', ')' }

    NOT = r'(not)|\~'
    AND = r'(and)|\&'
    OR = r'(or)|\|'
    IMPLIES = r'(implies)|(then)|(->)'
    IFF = r'(iff)|(<->)'
    XOR = r'(xor)|\^'

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
        ('left', OR, IMPLIES, IFF, XOR),
        ('left', AND),
        ('left', '(', ')'),
        ('right', NOT)
    )

    def __init__(self):
        self.vars = set()

    @_('expr')
    def statement(self, p):
        return p.expr

    @_('NOT expr')
    def expr(self, p):
        return Negate(p.expr)

    @_('"(" expr ")"')
    def expr(self, p):
        return p.expr

    @_('expr AND expr')
    def expr(self, p):
        return And(p.expr0, p.expr1)

    @_('expr OR expr')
    def expr(self, p):
        return Or(p.expr0, p.expr1)

    @_('expr IMPLIES expr')
    def expr(self, p):
        return Implies(p.expr0, p.expr1)

    @_('expr IFF expr')
    def expr(self, p):
        return Iff(p.expr0, p.expr1)

    @_('expr XOR expr')
    def expr(self, p):
        return Xor(p.expr0, p.expr1)

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
