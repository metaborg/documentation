.. highlight:: dynsem

.. _dynsemreference:

==================
Language reference
==================

This page is a syntax-oriented language reference for DynSem.

-----------------
Modules
-----------------


.. describe:: module

      module
        .. error:: Not described yet

      imports
        .. error:: Not described yet

      signature
        .. error:: Not described yet

      rules
        .. error:: Not described yet

-----------------
Signature section
-----------------

.. describe:: signature

  The signatures section of a DynSem module provides definitions for program abstract syntax and for additional entities used in the specification of a language's dynamic semantics.

      sorts
        Define sorts of program and value terms, separated by white space. For example:

          `sorts Exprs Stmts`

        A number of sorts are built-in sorts in DynSem:

          String
            for strings as values or program terms

          Int
            for integers

            .. note:: there is no implicit assumption regarding range of values

          Bool
            for boolean terms. Literals of sort Bool are `true` and `false`

          List(S)
            for lists of some sort `S`. `S` can be any sort

          Map(S1, S2)
            for associative arrays where keys are of sort `S1` and values are of sort `S2`

      sort aliases
        Declare sort synonyms. Sort aliases are useful to define shorthands for composed sorts such as for Maps and Lists. For example:

          `sort aliases Env = Map(String, Value)`

        declares `Env` as a sort alias for `Map(String, Value)`. Wherever the sort `Map(String, Value)` is used, the alias `Env` can be used instead.

        .. note:: sort-aliases are only syntactic sugar for their aliased sorts and sorts can therefore not be distinguished based on name. For example if two sort aliases `Env1` and `Env2` are defined for `Map(String, Value)` they all become equal and there is no type difference between `Env1` and `Env2`. One can now see `Env1 = Env2 = Map(String, Value)`.

      variables
        Defines variable prefix schemes. Variable schemes take the form `ID = S` and express the expectation that all variables prefixed with ID are of the sort S. A variable is part of the scheme X if it's name begins with X and is either followed only by numbers and/or apostrophes, or is followed by _ followed by any valid identifier. For example given the scheme:

          `variables v : Value`

        the following are valid variable names: **v1**, **v2**, **v'**, **v'''**, **v1'**, **v_foo**.

        .. note:: Variable schemes can be useful in combination with [implicit reductions][1] to concisely express the expected sort.

      constructors
        Define constructors for program and value terms. There are two constructor variants:

          regular constructors
            Define regular constructors. Definitions take the form `NAME: {SORT "*"}* -> SORT`, where `NAME` is the name of the constructor, followed by the sorts of the children of the constructor, and where the last `SORT` is the sort of the constructor. Example:

              `constructors Plus: Exprs * Exprs -> Exprs`

          implicit constructors
            Define unary constructors which can be implicitly constructed/deconstructed in pattern matches and term constructions. For example, the constructor:

              `constructors OkV: V -> O {implicit}`

            declares the **OkV** unary constructor. In term constructions where a term of sort **O** is expected but a term *t* of sort **V** is provided, the constructor **OkV** is automatically constructed to surround term *t* to become `Ok(t)`. In pattern matches where a term of sort **O** is provided but a term of sort **V** is expected, a pattern match for the term **OkV** is automatically inserted.

          meta-functions
            Define constructors and implicitly define a reduction arrows for those constructors. Constructors defined in this way are not of a particular sort and therefore cannot be nested in other constructors. Meta-function constructors can be useful to encapsulate semantic definitions which can be reused. Syntactically the difference between regular constructor and meta-function declarations is in the double arrow at the end of the declaration:

              `constructors concat: String * String --> String`

            which can be read as "define meta-function **concat** with two arguments of sort **String** which reduces to a term of sort **String**"

      arrows
        Declare named reduction relations. Relations in DynSem have to be declared before they are used to define reductions over them. Declarations take the form `S1 -ID-> S2`. Such a declaration makes the relation `-ID->` (where ID is the relation name) available to reduce terms of sort `S1` (input sort) to terms of sort `S2` (output sort). For example, the relation declaration:

              `arrows Exprs -eval-> Values`

        declares relation **eval** to relate terms of the **Exprs** sort to terms of the **Values** sort.

        Multiple relations with the same name may be declared as long as their input sorts are different. Relations cannot be distinguished by their output sort; it is invalid to define two relations with the same input sort, same name but different output sorts.

        .. note:: It is valid to have multiple identical arrow declarations.

        The name-part of the relation declaration may be omitted, such that:

              `arrows Exprs --> Values`

        is a synonym for:

              `arrows Exprs -default-> Values`

        This reduction arrow can be referred to with or without mentioning it's name.

      native operators
        These are natively defined (in Java) operators.
        .. error:: Not described yet

      native datatypes
        These define datatypes implemented natively (in Java) which can be used inside DynSem specifications.
        .. error:: Not described yet

-------------
Rules section
-------------

.. describe:: rules
  The rules section of a DynSem module provides inductive definitions for reduction relations for program terms.

~~~~~~~~~~~~~~~~~~~
Semantic components
~~~~~~~~~~~~~~~~~~~



1. Implicit propagation of read-only semantic components
2. Implicit propagation of read-write semantic components
