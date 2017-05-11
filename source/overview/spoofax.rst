.. _spoofax:

.. - What is it?
.. - What can you use it for?
.. - When do you need it?
.. - What has been done with it already?
.. - Where can I get it?
.. - How do I use it?

====================================
The Spoofax Language Workbench
====================================

Spoofax is a platform for developing textual (domain-specific) programming languages. 
The platform provides the following ingredients:

* Meta-languages for high-level declarative language definition. 
* An interactive environment for developing languages using these meta-languages
* Code generators that produces parsers, type checkers, compilers, interpreters, and other tools from language definitions
* Generation of full-featured Eclipse editor plugins from language definitions 
* Generation of full-featured IntelliJ editor plugins from language definitions (experimental)
* An API for programmatically combining the components of a language implementation

With Spoofax you can focus on the essence of language definition and ignore irrelevant implementation details.


Software Languages
------------------

Spoofax supports the development of _textual_ languages, but does not otherwise restrict what kind of language you develop. Spoofax can be used to develop

- programming languages
- domain-specific languages
- configuration languages
- data description languages
- data modeling languages
- web programming 

Creating Full-Featured Editors
-------------------------------------

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

* Semantic editor services

  - Name checking
  - Type checking
  - Inline error messages
  - Reference resolution: navigate to declaration

* Builders invoked from configurable menu

  - Code generation
  - Transformations
  - Refactoring

* Deployment

  - Eclipse plugin
  - IntelliJ plugin (experimental)



Testing
-----------

* Testing language definitions


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

