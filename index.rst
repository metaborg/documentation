==============================
The Spoofax Language Workbench
==============================

.. image:: code/spoofax/graphics/logos/Spoofax.svg

The Spoofax Language Workbench supports the definition of all aspects
of textual languages using high-level, declarative meta-languages, including

- The SDF3 syntax definition formalism
- The NaBL name binding language
- The Stratego transformation language
- The DynSem dynamic semantics specification language
- The ESV editor services configuration language

From a language definition using these meta-languages, Spoofax
generates full-featured Eclipse and IntelliJ editor plugins, as well
as a command-line interface. The generated editors include syntax
highlighting, syntax checking, parse error recovery, error markers for
syntactic and semantic errors, and custom operations, such as invoking
an interpreter or compiler.


Quick Start
==============

- Language Development

  - :doc:`Getting Started <source/langdev/start>`
  - Manual

    - :doc:`source/langdev/manual/env/intellij/index`
    - :doc:`source/langdev/manual/env/shell/index`
    - :doc:`source/langdev/manual/config`

  - Meta-Languages

    - :doc:`source/langdev/meta/lang/sdf3`
    - :doc:`source/langdev/meta/lang/stratego/index`
    - :doc:`source/langdev/meta/lang/nabl`
    - :doc:`source/langdev/meta/lang/dynsem/index`

- Core API

  - :doc:`Getting Started <source/core/start>`
  - :doc:`source/core/manual/concepts`
  - :doc:`source/core/manual/service`
  - :doc:`source/core/manual/extend`
  - :doc:`source/core/api`

- Development

  - :doc:`source/dev/maven`
  - :doc:`source/dev/build`
  - :doc:`source/dev/dev`
  - Internals

    - :doc:`source/dev/internals/intellij/index`

- Releases

  - :doc:`nightly <source/release/note/nightly>`
  - :doc:`2.0.0 (08-07-2016) <source/release/note/2.0.0>`
  - :doc:`2.0.0-beta1 (07-04-2016) <source/release/note/2.0.0-beta1>`
  - :doc:`1.5.0 (18-12-2015) <source/release/note/1.5.0>`
  - :doc:`1.4.0 (06-03-2015) <source/release/note/1.4.0>`
  - :doc:`1.3.1 (09-12-2014) <source/release/note/1.3.1>`
  - :doc:`1.3.0 (12-11-2014) <source/release/note/1.3.0>`
  - :doc:`1.2.0 (13-08-2014) <source/release/note/1.2.0>`
  - :doc:`1.1.0 (25-03-2013) <source/release/note/1.1.0>`
  - :doc:`1.0.2 (15-02-2012) <source/release/note/1.0.2>`
  - :doc:`1.0.0 (28-12-2011) <source/release/note/1.0.0>`

- Migration

  - :doc:`2.0.0 <source/release/migrate/2.0.0>`


Full Table of Contents
======================

.. toctree::
   :maxdepth: 3

   source/overview/support

.. toctree::
   :maxdepth: 3
   :caption: Language Development

   Getting Started <source/langdev/start>
   Guides <source/langdev/guide/index>
   Manual <source/langdev/manual/index>
   Meta-Languages <source/langdev/meta/lang/index>
   Meta-Libraries <source/langdev/meta/lib/index>
   Examples <source/langdev/example/index>

.. toctree::
   :maxdepth: 3
   :caption: Core API

   Getting Started <source/core/start>
   Guides <source/core/guide/index>
   Manual <source/core/manual/index>
   Examples <source/core/example/index>
   API Reference <source/core/api>

.. toctree::
   :maxdepth: 3
   :caption: Development

   Maven <source/dev/maven>
   Build <source/dev/build>
   Develop <source/dev/dev>
   Contribute <source/dev/contribute>
   Internals <source/dev/internals/index>

.. toctree::
   :maxdepth: 3
   :caption: Releases

   source/release/note/index
   source/release/migrate/index
