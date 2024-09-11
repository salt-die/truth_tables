# truth_tables

Create pretty-printed truth tables and abstract syntax trees from boolean expressions!

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

The parser will accept symbolic or english names for boolean operators:

```text
┌──────────┬──────────┬─────────┐
│ operator │ symbolic │ english │
├──────────┼──────────┼─────────┤
│   Not    │    ~     │   not   │
│   And    │    &     │   and   │
│    Or    │    |     │   or    │
│ Implies  │    ->    │ implies │
│   Iff    │   <->    │   iff   │
│   Xor    │    ^     │   xor   │
└──────────┴──────────┴─────────┘
```

`And` has greater precedence than `Or`, `Implies`, `Iff`, and `Xor`.
