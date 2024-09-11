# truth_tables

Create pretty-printed truth tables and abstract syntax trees from boolean expressions! Installation is as easy as `pip install truth_tables`.

Example usage:

```py
>>> from truth_tables import TruthTable
>>> my_table = TruthTable('p or q', '~p -> q', 'T and ~T')
>>> print(my_table)
┌───┬───┬────────┬─────────┬──────────┐
│ p │ q │ p or q │ ~p -> q │ T and ~T │
├───┼───┼────────┼─────────┼──────────┤
│ F │ F │   F    │    F    │    F     │
│ F │ T │   T    │    T    │    F     │
│ T │ F │   T    │    T    │    F     │
│ T │ T │   T    │    T    │    F     │
└───┴───┴────────┴─────────┴──────────┘
>>> print(my_table.ast)
Or
├─Variable('p')
╰─Variable('q')

Implies
├─Negate
│ ╰─Variable('p')
╰─Variable('q')

And
├─LiteralTrue
╰─Negate
  ╰─LiteralTrue

>>> my_table = TruthTable('~((p xor (q and ~r) or q) and ~(p <-> r))')
>>> print(my_table)
┌───┬───┬───┬───────────────────────────────────────────┐
│ p | q | r | ~((p xor (q and ~r) or q) and ~(p <-> r)) │
├───┼───┼───┼───────────────────────────────────────────┤
│ F | F | F |                     T                     │
│ F | F | T |                     T                     │
│ F | T | F |                     T                     │
│ F | T | T |                     F                     │
│ T | F | F |                     F                     │
│ T | F | T |                     T                     │
│ T | T | F |                     F                     │
│ T | T | T |                     T                     │
└───┴───┴───┴───────────────────────────────────────────┘
```

Two `TruthTables` are equal if they have the same variables and the same truth values (not necessarily the same propositions).

```py
>>> TruthTable('p -> q') == TruthTable('~p or q')
True
```

## Notes on the Parser

- The parser will accept symbolic or english names for boolean operators:
  | operator  | symbolic | english   |
  | :-------: | :------: | :-------: |
  | `Not`     | `~`      | `not`     |
  | `And`     | `&`      | `and`     |
  | `Or`      | `\|`     | `or`      |
  | `Implies` | `->`     | `implies` |
  | `Iff`     | `<->`    | `iff`     |
  | `Xor`     | `^`      | `xor`     |

- `Not` has greater precendence than `And` and `And` has greater precedence than `Or`, `Implies`, `Iff`, and `Xor`.
- `T` and `F` are parsed as boolean literals.
- Other than the english operator names and boolean literals, variable names may be any sequence of word characters that don't start with a digit.
