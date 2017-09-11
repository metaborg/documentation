.. _spoofax:

.. - What is it?
.. - What can you use it for?
.. - When do you need it?
.. - What has been done with it already?
.. - Where can I get it?
.. - How do I use it?

==============================
The Spoofax Language Workbench
==============================

.. toctree::
   :hidden:
   :maxdepth: 2

   The Spoofax Language Workbench <self>
   Examples <source/overview/examples.rst>
   Publications <source/overview/publications.rst>

.. toctree::
   :hidden:
   :maxdepth: 2
   :caption: Tutorials

   Installing Spoofax <source/install>
   Creating a Language Project <source/langdev/start>
   Using the API <source/core/start>
   Getting Support <source/support>

.. toctree::
   :hidden:
   :maxdepth: 2
   :caption: Reference Manual

   source/langdev/meta/lang/tour/index
   source/langdev/meta/lang/aterm/index
   Syntax Definition with SDF3 <source/langdev/meta/lang/sdf3/index>
   Static Semantics with NaBL2 <source/langdev/meta/lang/nabl2/index>
   Transformation with Stratego <source/langdev/meta/lang/stratego/index>
   Dynamic Semantics with DynSem <source/langdev/meta/lang/dynsem/index>
   Editor Services with ESV <source/langdev/meta/lang/esv>

   Language Testing with SPT <source/langdev/meta/lang/spt/index>
   Building Languages <source/langdev/manual/index>
   Programmatic API <source/core/manual/index>
   Developing Spoofax <source/dev/index>

.. toctree::
   :hidden:
   :maxdepth: 2
   :caption: Releases

   Latest Stable Release <source/release/stable>
   Development Release <source/release/development>
   Release Archive <source/release/note/index>
   Migration Guides <source/release/migrate/index>

.. toctree::
   :hidden:
   :maxdepth: 2
   :caption: Contributions

   Contributions <source/overview/contributions.rst>

Spoofax is a platform for developing textual (domain-specific) programming languages.
The platform provides the following ingredients:

- Meta-languages for high-level declarative language definition
- An interactive environment for developing languages using these meta-languages
- Code generators that produces parsers, type checkers, compilers, interpreters, and other tools from language definitions
- Generation of full-featured Eclipse editor plugins from language definitions
- Generation of full-featured IntelliJ editor plugins from language definitions (experimental)
- An API for programmatically combining the components of a language implementation

With Spoofax you can focus on the essence of language definition and ignore irrelevant implementation details.

Developing Software Languages
-----------------------------

Spoofax supports the development of *textual* languages, but does not otherwise restrict what kind of language you develop. Spoofax has been used to develop the following kinds of languages:

Programming languages
   Languages for programming computers. Implement an existing programming language to create an IDE and other tools for it, or design a new programming language.

Domain-specific languages
  Languages that capture the understanding of a domain with linguistic abstractions. Design a DSL for your domain with a compiler that generates code that would be tedious and error prone to produce manually.

Scripting languages
  Languages with a special run-time environment and interpreter

Work-flow languages
  Languages for scheduling actions such as building the components of a software system

Configuration languages
  Languages for configuring software and other systems

Data description languages
  Languages for formatting data

Data modeling languages
  Languages for describing data schemas

Web programming languages
  Languages for programming web clients or servers

Creating Full-Featured Editors
------------------------------

From a language definition Spoofax generates full-featured Eclipse and IntelliJ editor plugins, as well as a command-line interface. Generated editors support the following features:

* Syntactic editor services

  - Syntax highlighting
  - Syntax checking
  - Parse error recovery
  - Outline view
  - Syntactic code completion
  - Formatting

* Semantic editor services

  - Name checking
  - Type checking
  - Inline error markers
  - Reference resolution: navigate to declaration

* Builders: custom operations for invoking

  - Code generation
  - Interpreter
  - Transformations
  - Refactorings

Declare Your Language
---------------------

We design Spoofax according to the following guiding principles:

Separation of concerns
  Separate specification from implementation. Separate language-specific aspects from language-independent aspects. Separate definition of separate aspects (e.g. separate syntax definition and static semantics definition)

Single source
  Instead of repeating a language aspect in many different implementation components, we aim to generate many different artifacts from a single source.

Declarative language definition
  Language designers should focus on what distinguishes their language and should not be distracted by writing boilerplate for recurring implementation details. Rather than confronting each language designer with these implementation details, we factor them out into language-independent abstractions and corresponding implementations.


Following these guidelines, Spoofax provides the following high-level, declarative meta-languages:

SDF3
  The SDF3 Syntax Definition Formalism allows language designers to focus on the structure of programs rather than on debugging parser implementations by means of the following features: support for the full class of context-free grammars by means of generalized LR parsing, integration of lexical and context-free syntax through scannerless parsing, safe and complete disambiguation using priority and associativity declarations, an automatic mapping from parse trees to abstract syntax trees through integrated constructor declarations, automatic generation of formatters based on template productions, syntactic completion proposals in editors.

NaBL2
  The NaBL2 'Name Binding Language' supports the definition of the static semantics of languages including name binding and type analysis. NaBL2 rules define a mapping from abstract syntax trees to name and type constraints. The generated constraints are solved by a language-independent solver and produce error messages to display in an editor and a symbol table for the analyzed abstract syntax tree for use in further processing. Name analysis in NaBL2 is based on scope graphs, a language-independent model for name resolution and scoping.

Stratego
  The Stratego transformation language supports the definition of transformations of abstract syntax terms using rewrite rules and programmable rewriting strategies. Strategies enable concise definition of traversals over trees. Stratego is used to define desugarings, transformations, optimizations, and code generation (translation to another language).

DynSem
  The DynSem Dynamic Semantics specification language supports the definition of the execution behavior of programs by means of reduction rules that are typically used to define *natural semantics* or *big-step operational semantics*. DynSem specifications are compiled to interpreters targeting the Truffle/Graal stack.

SPT
  The SPT testing language supports the definition of tests for all aspects of a language definition.

ESV
  The ESV editor services language is used to configure language definitions.

A Platform for Language Engineering
-----------------------------------

Spoofax is a platform for language engineers. That is, it provides full support for software engineering of language implementations.

Agile Language Development
  An important feature of Spoofax is its support for agile language development. The development of a language definition and testing that language definition in the generated IDE for the language under development is done in the *same* Eclipse instance. This enables a quick turn-around time between language development and language testing.

IDE generation
  Spoofax generates a full fledged editor plugin from a language definition.

API
  Spoofax does not only provide an IDE for interactively developing and using languages, it also provides a programmatic interface that enables embedding languages and their implementations directly in application code or to invoke language components from build systems or the command line.

Bootstrapped Language Workbench
  Spoofax has been bootstrapped. That is, Spoofax is used for the definition of its own meta-languages and the workbench is the composition of plugins generated for these meta-languages.

Continuous integration
  The Spoofax sources are continuously built on a buildfarm at TU Delft, which reports build errors to Spoofax developers and provides a complete build for various platforms of the latest version.

Open source
  Spoofax is open source and available under the Apache 2.0 license. The sources are maintained in the `MetaBorg <https://github.com/metaborg>`_ github organization; pull requests are welcome.

A Platform for Research
-----------------------

Spoofax is a platform for language engineering research.
Due to its modular architecture it is easy to extend the workbench with new experimental meta-languages and tools.
For example, the current (May 2017) version comes with a new experimental parser generator in addition to the old SDF2 parser generator, and it provides a new NaBL2 static semantics specification language next to the old NaBL/TS solution.
