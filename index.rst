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
    
:doc:`contents.rst`



