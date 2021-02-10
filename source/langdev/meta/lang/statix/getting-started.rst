.. _statix-getting-started:

===============
Getting Started
===============

.. note::

   Generate a language project that uses Statix by following :ref:`this guide<langdev-getting-started>` and selecting ``Statix`` for ``Analysis type``.

The best way to get started on Statix is to use the the lectures from the TU Delft compiler construction course.
These lectures explain the concepts that are used in Statix, and discuss scope graph patterns and Statix rules for several language features.
In particular, these are the relevant lectures:

- `Type Checking and Type Constraints <https://tudelft-cs4200-2020.github.io/lectures/2020/09/17/lecture4/>`_
  introduces type checking concepts and the basics of Statix specifications.
- `Name Binding and Name Resolution <https://tudelft-cs4200-2020.github.io/lectures/2020/09/24/lecture5/>`_
  introduces scope graphs in depth, discusses many name binding patterns in terms of scope graphs and queries,
  and shows example Statix rules for many of these patterns.
- `Constraint Semantics and Constraint Resolution <https://tudelft-cs4200-2020.github.io/lectures/2020/10/01/lecture6/>`_
  Discusses in the semantics of Statix and some of the algorithms that are used in its implementation.

The lecture pages also link to other presentations and tutorials on Statix and scope graphs.

Example projects using Statix can be found in `this reposity <https://github.com/metaborg/nabl/tree/master/statix.integrationtest/>`_.
The `STLCrec<https://github.com/metaborg/nabl/tree/master/statix.integrationtest/lang.stlcrec>`_ project is the simplest, and shows a simply-typed lambda calculus extended with structural records.
The `Units<https://github.com/metaborg/nabl/tree/master/statix.integrationtest/lang.units>`_ project contains definitions for a language that supports various module and package features.
The `FGJ<https://github.com/metaborg/nabl/tree/master/statix.integrationtest/lang.fgj>`_ project shows a more advanced specification for Featherweight Generic Java, showing scopes as types, complex scope graph patterns, and lazy-substitution-based generics.

