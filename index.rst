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
   :caption: Language Development

   Getting Started <source/langdev/start>
   Manual <source/langdev/manual/index>
   Meta-Languages <source/langdev/meta/lang/index>
   Meta-Libraries <source/langdev/meta/libraries/index>

.. toctree::
   :maxdepth: 2
   :caption: Core API

   Getting Started <source/core/start>
   Manual <source/core/manual/index>
   API Reference <http://www.metaborg.org/projects/spoofax-api/en/latest/>

.. toctree::
   :maxdepth: 2
   :caption: Development

   Maven <source/dev/maven>
   Build <source/dev/build>
   Develop <source/dev/dev>
   Contribute <source/dev/contribute>
   Internals <source/dev/internals/index>

.. toctree::
   :maxdepth: 2
   :caption: Releases

   Release Notes <source/release/note/index>
   Migration Guides <source/release/migrate/index>
