=====================
The Spoofax Language Workbench
=====================

.. image:: code/spoofax/graphics/logos/Spoofax.svg

Spoofax is a language workbench for developing textual domain-specific languages
with full-featured Eclipsee and IntelliJ editor plugins.

Meta-Languages
=======


With the Spoofax language workbench, you can write the grammar of your
language using the high-level SDF grammar formalism. Based on this
grammar, basic editor services such as syntax highlighting and code
folding are automatically provided. Using high-level descriptor
languages, these services can be customized. More sophisticated
services such as error marking and content completion can be specified
using rewrite rules in the Stratego language.

Language definitions in Spoofax are constructed using the following meta-languages:

    - The :doc:`source/langdev/meta/lang/sdf3` syntax definition formalism
    - The :doc:`source/langdev/meta/lang/stratego/index` transformation language
    - The :doc:`source/langdev/meta/lang/nabl` name binding language
    - The :doc:`source/langdev/meta/lang/dynsem/index` dynamic semantics language
    

Full Table of Contents
======================

.. toctree::
   :maxdepth: 3
   :caption: Overview
   source/overview/introduction
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

   Getting Started <source/dev/start>
   Maven <source/dev/maven>
   Build <source/dev/build>
   Develop <source/dev/dev>
   Contribute <source/dev/contribute>
   Release <source/dev/release>
   Internals <source/dev/internals/index>

.. toctree::
   :maxdepth: 3
   :caption: Releases

   source/release/note/index
   source/release/migrate/index

