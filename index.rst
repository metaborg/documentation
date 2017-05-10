==============================
The Spoofax Language Workbench
==============================

.. image:: source/spoofax.svg

The Spoofax Language Workbench supports the definition of all aspects of textual languages using high-level, declarative meta-languages, including:

- The SDF3 syntax definition formalism
- The NaBL name binding language
- The Stratego transformation language
- The DynSem dynamic semantics specification language
- The ESV editor services configuration language

From a language definition using these meta-languages, Spoofax generates full-featured Eclipse and IntelliJ editor plugins, as well as a command-line interface.
The generated editors include syntax highlighting, syntax checking, parse error recovery, error markers for syntactic and semantic errors, and custom operations, such as invoking an interpreter or compiler.

Table of Contents
=================

.. toctree::
   :maxdepth: 2

   Installation Guide <source/install>
   Getting Support <source/support>
   All Downloads <source/download>

.. toctree::
   :maxdepth: 2
   :caption: Reference Manual

   Spoofax Language Development <source/langdev/manual/index>
   Spoofax Core API <source/core/manual/index>

   SDF3 <source/langdev/meta/lang/sdf3>
   Stratego <source/langdev/meta/lang/stratego/index>
   NaBL <source/langdev/meta/lang/nabl>
   NaBL2 <source/langdev/meta/lang/nabl2/index>
   DynSem <source/langdev/meta/lang/dynsem/index>
   SPT <source/langdev/meta/lang/spt>

   Development <source/dev/index>

.. toctree::
   :maxdepth: 2
   :caption: Tutorials

   Getting Started - Language Development <source/langdev/start>
   Getting Started - Core API <source/core/start>

.. toctree::
   :maxdepth: 2
   :caption: Releases

   Release Notes <source/release/note/index>
   Migration Guides <source/release/migrate/index>
