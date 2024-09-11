"""A truth table for boolean logic expressions."""

from itertools import product
from typing import Self

import lark

from ._ast import GRAMMAR, AST_Transformer


def _pretty_printed_table(expressions: list[str], table: tuple[tuple[str, ...]]) -> str:
    """Return a pretty-printed truth table."""
    widths = [len(expression) for expression in expressions]
    padded_rows = [
        [f"{'FT'[value]:^{width}}" for value, width in zip(row, widths)]
        for row in table
    ]
    lines = ["─" * (width + 2) for width in widths]
    table = []
    table.append(f"┌{"┬".join(lines)}┐")
    table.append(f"│ {" | ".join(expressions)} │")
    table.append(f"├{"┼".join(lines)}┤")
    table.extend(f"│ {" | ".join(row)} │" for row in padded_rows)
    table.append(f"└{"┴".join(lines)}┘")
    return "\n".join(table)


class TruthTable:
    r"""
    A truth table for boolean logic expressions.

    Parameters
    ----------
    \*propositions : tuple[str, ...]
        The truth table's propositions.

    Attributes
    ----------
    propositions : tuple[str, ...]
        The truth table's propositions.
    vars : tuple[str, ...]
        A sorted tuple of the variables of all propositions.
    ast : str
        A string representation of the ast of each proposition.

    Methods
    -------
    __str__()
        Return the truth table as a pretty-printed table.
    __eq__()
        Return whether two truth tables are equal.
    """

    def __init__(self, *propositions: str) -> None:
        transformer = AST_Transformer()
        parser = lark.Lark(GRAMMAR, parser="lalr", start="exp", transformer=transformer)
        expressions = [parser.parse(prop) for prop in propositions]

        self.vars: tuple[str, ...] = tuple(sorted(transformer.vars))
        """A sorted tuple of the variables of all propositions."""

        table = []
        for values in product((False, True), repeat=len(self.vars)):
            symbols = dict(zip(self.vars, values))
            results = (expr.eval(symbols) for expr in expressions)
            table.append((*values, *results))

        self._table: tuple[tuple[bool, ...], ...] = tuple(table)
        """The truth table's table of truth values."""
        self._str: str = _pretty_printed_table(self.vars + propositions, table)
        """The truth table as a pretty-printed table."""
        self.propositions: tuple[str, ...] = propositions
        """The truth table's propositions."""
        self.ast: str = "\n".join(str(expression) for expression in expressions)
        """A string representation of the ast of each proposition."""

    def __repr__(self) -> str:
        """Return a string representation of a TruthTable."""
        return (
            f"{type(self).__name__}"
            f"({', '.join(repr(prop) for prop in self.propositions)})"
        )

    def __str__(self) -> str:
        """Return the truth table as a pretty-printed table."""
        return self._str

    def __eq__(self, other: Self) -> bool:
        """
        Return whether two truth tables are equal.

        Two truth tables are equal if they have the same variables and the same truth
        values. The propositions may differ.
        """
        return self.vars == other.vars and self._table == other._table
