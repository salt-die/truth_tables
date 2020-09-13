Generate truth tables and abstract syntax trees from boolean expressions!

Example usage:
```py
>>> from truth_tables import TruthTable
>>> my_table = TruthTable('p or q', '~p -> q', 'T and ~T')
>>> my_table.display()
┌───┬───┬────────┬─────────┬──────────┐
│ p │ q │ p or q │ ~p -> q │ T and ~T │
├───┼───┼────────┼─────────┼──────────┤
│ F │ F │   F    │    F    │    F     │
│ F │ T │   T    │    T    │    F     │
│ T │ F │   T    │    T    │    F     │
│ T │ T │   T    │    T    │    F     │
└───┴───┴────────┴─────────┴──────────┘
>>> my_table.show_ast()
BinOp(op='or')
 ├─Var(name='p')
 ╰─Var(name='q')

BinOp(op='->')
 ├─UnOp(op='~')
 │  ╰─Var(name='p')
 ╰─Var(name='q')

BinOp(op='and')
 ├─Const(value=True)
 ╰─UnOp(op='~')
    ╰─Const(value=True)
>>> my_table = TruthTable('~((p xor (q and ~r) or q) and ~(p <-> r))')
>>> my_table.display(binary=True)
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

Also included is the function `tt(*props)` which is just short for `TruthTable(*props).display()`:
```py
>>> from truth_tables import tt
>>> tt('wet and puddles -> rained')
┌─────────┬────────┬─────┬───────────────────────────┐
│ puddles │ rained │ wet │ wet and puddles -> rained │
├─────────┼────────┼─────┼───────────────────────────┤
│    F    │   F    │  F  │             T             │
│    F    │   F    │  T  │             T             │
│    F    │   T    │  F  │             T             │
│    F    │   T    │  T  │             T             │
│    T    │   F    │  F  │             T             │
│    T    │   F    │  T  │             F             │
│    T    │   T    │  F  │             T             │
│    T    │   T    │  T  │             T             │
└─────────┴────────┴─────┴───────────────────────────┘
```

If one wants to know if two expressions are equivalent, one can just compare the TruthTables with `==`.  (Two TruthTables are
equal if they have the same variables and the same truth values.)