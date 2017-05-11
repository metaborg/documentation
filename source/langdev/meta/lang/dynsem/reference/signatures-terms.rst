.. _dynsemtermsignatures:

===============
Term signatures
===============

The **signature** section of a DynSem module provides definitions for program terms and for additional entities used in the specification of a language's dynamic semantics. We discuss here the subsections of **signature** which deal with representation of terms.

.. note:: For a discussion of **signature** subsections dealing with operational concepts see :ref:`dynsemarrowsignatures`.


.. describe:: sorts

    Define sorts of program and value terms, separated by white space. For example:

    .. code-block:: dynsem

        sorts Exprs Stmts

    DynSem has a number of built-in sorts and operations on them: ``String``, ``Int``, ``List``, etc. For a complete list and description of operations available see :ref:`dynsembuiltins`.

.. describe:: constructors

  Define constructors for program and value terms. There are two constructor variants:

    regular constructors
      Define regular constructors. Definitions take the form `NAME: {SORT "*"}* -> SORT`, where `NAME` is the name of the constructor, followed by the sorts of the children of the constructor, and where the last `SORT` is the sort of the constructor. Example:

      .. code-block:: dynsem

        constructors
          Plus: Exprs * Exprs -> Exprs

    implicit constructors
      Define unary constructors which can be implicitly constructed/deconstructed in pattern matches and term constructions. For example, the constructor:

      .. code-block:: dynsem

        constructors
          OkV: V -> O {implicit}

      declares the **OkV** unary constructor. In term constructions where a term of sort **O** is expected but a term *t* of sort **V** is provided, the constructor **OkV** is automatically constructed to surround term *t* to become `Ok(t)`. In pattern matches where a term of sort **O** is provided but a term of sort **V** is expected, a pattern match for the term **OkV** is automatically inserted.

.. describe:: sort aliases

    Declare sort synonyms. Sort aliases are useful to define shorthands for composed sorts such as for Maps and Lists. For example:

    .. code-block:: dynsem

      sort aliases
        Env = Map(String, Value)
        SciNum = (Float * Int)

    declares `Env` as a sort alias for `Map(String, Value)`. Wherever the sort `Map(String, Value)` is used, the alias `Env` can be used instead. The example also declares `SciNum` as a sort alias for the pair of a `Float` and an `Int`.

    .. note:: sort-aliases are only syntactic sugar for their aliased sorts and sorts can therefore not be distinguished based on name. For example if two sort aliases `Env1` and `Env2` are defined for `Map(String, Value)` they all become equal and there is no type difference between `Env1` and `Env2`. One can now see `Env1 = Env2 = Map(String, Value)`.

.. describe:: variables

    Defines variable prefix schemes. Variable schemes take the form `ID = S` and express the expectation that all variables prefixed with ID are of the sort S. A variable is part of the scheme X if it's name begins with X and is either followed only by numbers and/or apostrophes, or is followed by _ followed by any valid identifier. For example given the scheme:

      .. code-block:: dynsem

        variables
          v : Value

      the following are valid variable names: **v1**, **v2**, **v'**, **v'''**, **v1'**, **v_foo**.

      .. note:: Variable schemes can be useful in combination with `dynsem implicit reductions`_ to concisely express the expected sort.

.. describe:: native datatypes

    These define datatypes implemented natively (in Java) which can be used inside DynSem specifications.

    .. error:: Not documented
