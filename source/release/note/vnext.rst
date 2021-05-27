=============
Spoofax vNext
=============

These are the release notes for Spoofax vNext.

See the corresponding :ref:`migration guide <vnext-migration-guide>` for migrating from Spoofax vPrev to Spoofax vNext.

Changes
-------

Statix
~~~~~~
* Added ``stc-get-ast-ref`` rule to the Stratego API, which can be used to query
  ``ref`` properties.
* The Stratego primitives now issue console warnings when invalid labels or
  properties are used.
* Fixed a bug where ``stx-get-scopegraph-data`` would return unification variables instead of their values.
* Changed the default data order to ``true``, to make queries where only a label order is provided apply shadowing as expected.
* Added a menu option to execute tests with the concurrent solver
* Fixed a completeness bug in the traditional solver when executing queries in dataWf or dataLeq predicates.
