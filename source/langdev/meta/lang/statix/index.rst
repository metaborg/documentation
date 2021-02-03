.. _statix-index:

=======================================
Static Semantics Definition with Statix
=======================================

Programs that are syntactically well-formed are not necessarily valid programs. 
Programming languages typically impose additional *context-sensitive* requirements on programs that cannot be captured in a syntax definition. 
Languages use names to identify reusable units that can be invoked at multiple parts in a program. 
In addition, statically typed languages require that expressions are consistently typed.
The Statix language supports the specification of name binding and type checking rules of a language.
The rules of the static semantics are written as logic rules, and solved using a constraint-based approach, and uses scope graphs for name resolution.

.. note::

  The documentation in this section is currently very incomplete.
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

.. toctree::
   :maxdepth: 2
   :numbered: 3
   :caption: Table of Contents
   
   usage
   reference
   stratego-api
   signature-generator
   nabl2-migration
