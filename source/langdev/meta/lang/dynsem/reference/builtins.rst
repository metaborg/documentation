.. _dynsembuiltins:

===================
Built-in data types
===================

A number of sorts are built-in sorts in DynSem:

  String
    strings as values or program terms

  Int
    integers.

  Float
    decimals

  Bool
    booleans. Literals of sort Bool are `true` and `false`

  List(S)
    for lists of some sort `S`. `S` can be any sort

  Map(S1, S2)
    for associative arrays where keys are of sort `S1` and values are of sort `S2`

  (S1 * S2 * ... * Sn)
    for tuples of arbitrary arity. `S1`, `S2`, ... can be any sort.
