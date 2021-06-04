.. _concurrent-migration:

==================================
Migrating to the Concurrent Solver
==================================

.. role:: statix(code)
   :language: statix
   :class: highlight

Enabling the Concurrent Solver
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In order to enable the concurrent solver, either one of the following approaches
can be taken.

For a Language
--------------

To enable the concurrent solver for a language, set the ``language.statix.concurrent``
property in the ``metaborg.yaml`` file to ``true``. This ensures that the
concurrent solver is used for all sources in the language.

*Example*

.. code-block:: yaml

   id: org.example:mylang:0.1.0-SNAPSHOT
   name: mylang
   language:
     statix:
       concurrent: true

For an Example Project
----------------------

To enable the concurrent solver for a particular project only, set the
``runtime.statix.concurrent`` property in the ``metaborg.yaml`` file to a list
that contains all names of the languages for which you want to use the
concurrent solver. The name of the language should correspond to the ``name``
property in the ``metaborg.yaml`` of the language definition project.

*Example*

.. code-block:: yaml

   id: org.example:mylang.example:0.1.0-SNAPSHOT
   runtime:
     statix:
       concurrent:
       - mylang

.. warning::

   Please be aware that changes in the ``metaborg.yaml`` file may require a
   restart of Eclipse.

.. note::

   The concurrent solver can only be used in ``multifile`` mode.

Indirect Type Declaration
^^^^^^^^^^^^^^^^^^^^^^^^^

Type checking with the concurrent solver might result in
deadlock when type-checkers have mutual dependencies on their declarations.
This problem can be solved by adding an intermediate declaration that splits
the part of the declaration data that is filtered on (usually the declaration
*name*), and the part that is processed further by the querying unit (usually
the *type*). This pattern is best explained with an example.

*Example.* Suppose you have the following specification to model type declarations.

.. code-block:: statix

  signature
    relations
      type : ID -> TYPE

  rules
    declareType : scope * ID * TYPE
    resolveType : scope * ID -> TYPE

    declareType(s, x, T) :-
      !type[x, T] in s.

    resolveType(s, x) = T :-
      query type
        filter P* I* and { x' :- x' == x }
            in s |-> [(_, (_, T))].

This specification needs to be changed in the following:

.. code-block:: statix

  signature
    relations
      type   : ID -> scope
      typeOf : TYPE

  rules
    declareType : scope * ID * TYPE
    resolveType : scope * ID -> TYPE

    declareType(s, x, T) :-
      !type[x, withType(T)] in s.

    resolveType(s, x) = typeOf(T) :-
      query type
        filter P* I* and { x' :- x' == x }
            in s |-> [(_, (_, T))].

  rules
    withType : TYPE -> scope
    typeOf   : scope -> TYPE

    withType(T) = s :-
      new s, !typeOf[T] in s.

    typeOf(s) = T :-
      query typeOf filter e in s |-> [(_, T)].

We now discuss the changes one-by-one. First, the signature of relation ``type``
is be changed to ``ID -> scope``. In this scope, we store the type using the
newly introduced ``typeOf`` relation. This relation only carries a single ``TYPE``
term. In this way, the original term is still indirectly present in the outer
declaration.

The ``withType`` and ``typeOf`` rules allow to convert between these representations.
The ``withType`` rule creates a scope with a ``typeOf`` declaration that contains
the type.  In the adapted ``declareType`` rule, this constraint is used to
convert the ``T`` argument to the representation that the ``type`` relation accepts.
Likewise, the ``typeOf`` rule queries the ``typeOf`` declaration to extract the
type from a scope. This rule is used in the ``resolveType`` rule to convert
back to the term representation of a type.

Performing this change should resolve potential deadlocks when executing your
specifications. Because the signatures of the rules in the original specification
did not change, and the new specification should have identical semantics,
the remainder of the specification should not be affected.

Using new Solver Features
^^^^^^^^^^^^^^^^^^^^^^^^^

The concurrent solver also comes with some new features that were not present in
the traditional solver. This sections explains these features, and shows how to
use them.

Grouping
--------

.. warning::

	 Not yet written

Libraries
---------

.. warning::

	 Not yet written
