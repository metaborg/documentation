.. _spoofax:

.. - What is it?
.. - What can you use it for?
.. - When do you need it?
.. - What has been done with it already?
.. - Where can I get it?
.. - How do I use it?

==================
The Spoofax Language Workbench
==================



Language Workbench
------------------

Spoofax is a platform for developing textual (domain-specific) programming languages 

parser, type checker, compiler and/or interpreter

full-featured Eclipse editor plugins


With the Spoofax/IMP language workbench, you can write the grammar of your language using the high-level SDF grammar formalism. Based on this grammar, basic editor services such as syntax highlighting and code folding are automatically provided. Using high-level descriptor languages, these services can be customized. More sophisticated services such as error marking and content completion can be specified using rewrite rules in the Stratego language. 

A language workbench is an interactive environment for the development of (domain-specific) programming languages.


Software Languages
------------------

Spoofax supports the development of textual languages

- programming languages
- domain-specific languages
- configuration languages
- data description languages
- data modeling languages
- web programming 

Features of Spoofax Languages
-----------------------------

From a language definition using these meta-languages, Spoofax generates full-featured Eclipse and IntelliJ editor plugins, as well as a command-line interface.
The generated editors include syntax highlighting, syntax checking, parse error recovery, error markers for syntactic and semantic errors, and custom operations, such as invoking an interpreter or compiler.


what do you get when developing a language with Spoofax?

* Syntactic editor services

  - Syntax highlighting
  - Syntax checking
  - Error recovery
  - Outline view
  - Syntactic code completion
  - Formatting
  .. - Code folding

* Semantic editor services

  - Name checking
  - Type checking
  - Inline error messages
  - Reference resolution: navigate to declaration

* Builders

  - Code generation
  - Transformations
  - Refactoring


* Testing language definitions

* Deployment
  - Eclipse plugin
  - IntelliJ plugin (experimental)


invoked from configurable menu

Philosophy
----------

- declarative language definition: abstract from implementation details
- separate meta-languages for separate concerns
- generate many artifacts from single source


Declarative Meta-Languages
--------------------------

The Spoofax Language Workbench supports the definition of all aspects of textual languages using high-level, declarative meta-languages, including:

- The SDF3 syntax definition formalism
- The NaBL name binding language
- The Stratego transformation language
- The DynSem dynamic semantics specification language
- The ESV editor services configuration language




Examples

- All the Spoofax meta-languages have been bootstrapped. That is,  