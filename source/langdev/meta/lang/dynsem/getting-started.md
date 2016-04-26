```eval_rst
.. highlight:: ds
```

# Getting started

This is just a placeholder.

```DynSem
module trans/semantics/sl

imports
  trans/semantics/functions
  trans/semantics/statements
  trans/semantics/expressions
  trans/semantics/objects
  trans/semantics/builtins

signature
  arrows
    Program -init-> V


rules // loading and init

  ProgramDesug(fdefs, e) -init-> v
  where
    fdefs :: C C({}), E {} -load-> _ :: C C(E), E';
    e :: C C(E), E' --> v :: C _, E _.
```


```Stratego
module identity
imports list-cons
strategies
  main = id
```
