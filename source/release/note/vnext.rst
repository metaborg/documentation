=============
Spoofax vNext
=============

These are the release notes for Spoofax vNext.

See the corresponding :ref:`migration guide <vnext-migration-guide>` for migrating from Spoofax vPrev to Spoofax vNext.

Changes
-------
SDF3 — Lexical and context-free sort declarations
  In SDF3 you can now explicitly declare your sorts. Declare lexical sorts
  in a ``lexical sorts`` block, and context-free sorts in a
  ``context-free sorts`` block. Sorts declared in a kernel ``sorts`` block
  default to declaring context-free sorts until a suffix such as ``-LEX``
  is added. Note that you have to use ``sdf2table: java`` to support
  lexical sorts.

Statix — New projects use the signature generator by default
    New project that use Statix automatically have the Statix signature generator
    enabled. For this to work properly, declare your lexical and context-free
    sorts in SDF3 explicitly. See the :ref:`Statix signature generator
    <statix-signature-generator>` documentation for more information.
TypeSmart — Support for TypeSmart was removed
  We anticipate a more useable type analysis for Stratego in the form of a gradual type system.
  
  The ``metaborg.yaml`` file of a generated project used to contain
  a ``debug: typesmart: false``. This was to turn off the TypeSmart dynamic
  analysis by default. This analysis would stop any Stratego code when it tried
  to construct a tree that did not conform to the grammar of the project.
  
  To our knowledge TypeSmart was not used in any active Spoofax project. It did,
  however, slow down the build time of all Spoofax projects, because extraction
  of the grammar into a TypeSmart readable format had to be done even if the
  analysis was off for that project. These two points, and the anticipation of
  a gradual type system for Stratego, were the reasons to drop TypeSmart support.

Stratego — Combined compiled Stratego and helper code
  Compilation of Stratego and helper code written in Java (in
  ``src/main/strategies``) is now combined in a single jar file per Spoofax
  language instead of two. See the migration guide for more information on what to
  change in your Spoofax project. 

SPT — Ambiguous parse test expectation
  SPT gains support for the ``parse ambiguous`` expectation, which succeeds
  when a fragment parses successfully but with ambiguities.
  Tests with the ``parse succeeds`` expectation will now fail when the
  input parses ambiguously. To write tests for ambiguous parses, use the
  ``parse ambiguous`` expectation instead.

Overall
~~~~~~~
