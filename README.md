Generate truth tables and abstract syntax trees from boolean expressions!

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
├─Var('p')
╰─Var('q')

Implies
├─Negate
│ ╰─Var('p')
╰─Var('q')

And
├─Const(True)
╰─Negate
  ╰─Const(True)
>>> my_table = TruthTable('~((p xor (q and ~r) or q) and ~(p <-> r))', binary=True)
>>> print(my_table)
┌───┬───┬───┬───────────────────────────────────────────┐
│ p │ q │ r │ ~((p xor (q and ~r) or q) and ~(p <-> r)) │
├───┼───┼───┼───────────────────────────────────────────┤
│ 0 │ 0 │ 0 │                     1                     │
│ 0 │ 0 │ 1 │                     1                     │
│ 0 │ 1 │ 0 │                     1                     │
│ 0 │ 1 │ 1 │                     0                     │
│ 1 │ 0 │ 0 │                     0                     │
│ 1 │ 0 │ 1 │                     1                     │
│ 1 │ 1 │ 0 │                     0                     │
│ 1 │ 1 │ 1 │                     1                     │
└───┴───┴───┴───────────────────────────────────────────┘
```
Two `TruthTables` are equal if they have the same variables and the same truth values (not necessarily the same propositions).

```py
>>> TruthTable('p -> q') == TruthTable('~p or q')
True
```

The parser will accept symbolic or english names for boolean operators:
```
┌──────────┬──────────┬─────────┬──────────────┐
│ operator │ symbolic │ english │ alternatives │
├──────────┼──────────┼─────────┼──────────────┤
│   Not    │    ~     │   not   │              │
│   And    │    &     │   and   │              │
│    Or    │    |     │   or    │              │
│ Implies  │    ->    │ implies │     then     │
│   Iff    │   <->    │   iff   │              │
│   Xor    │    ^     │   xor   │              │
└──────────┴──────────┴─────────┴──────────────┘
```

Precedence is `Not`, `()`, `And`, then everything else.
