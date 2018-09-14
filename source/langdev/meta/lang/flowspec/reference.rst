==================
Language Reference
==================

.. role:: doc-lex(code)
   :language: doc-lex
   :class: highlight

.. role:: flowspec(code)
   :language: flowspec
   :class: highlight

This section gives a systematic overview of the FlowSpec language.

Lexical matters
---------------

Identifiers
^^^^^^^^^^^

Most identifiers in FlowSpec fall into one of two categories, which we
will refer to as:

* *Lowercase identifiers*, that start with a lowercase character, and
  must match the regular expression :doc-lex:`[a-z][a-zA-Z0-9]*`.
* *Uppercase identifiers*, that start with an uppercase character, and
  must match the regular expression :doc-lex:`[A-Z][a-zA-Z0-9]*`.

Comments
^^^^^^^^

Comments in FlowSpec follow C-style comments:

* ``// ... single line ...`` for single-line comments
* ``/* ... multiple lines ... */`` for multi-line comments

Multi-line comments can be nested, and run until the end of the file
when the closing ``*/`` is omitted.

Terms and patterns
------------------

.. code-block:: doc-lex

  term = ctor-id "(" {term ","}* ")"
       | "(" {term ","}* ")"
       | "{" {term ","}* "}"
       | "{" term "|" {term ","}* "}"
       | "{" {(term "|->" term) ","}* "}"
       | "{" term "|->" term "|" {(term "|->" term) ","}* "}"

  pattern = ctor-id "(" {pattern ","}* ")"
          | "(" {pattern ","}* ")"
          | var-id "@" pattern
          | "_"
          | var-id

Modules
-------

.. code-block:: doc-cf-[

   module [module-id]

     [section*]

FlowSpec specifications are organized in modules. A module has a name. This name consists of one or more names separated by slashes :doc-lex:`{name "/"}+`. The names must match the regular expression :doc-lex:`[a-zA-Z0-9\_][a-zA-Z0-9\_\.\-]*`.

Every module is defined in its own file, with the extension ``.flo``. The module name and the file paths must match. 

*Example.* An empty module ``analysis/flow/control``, defined in a file
:file:`.../analysis/flow/control.flo`.

.. code-block:: nabl2

   module analysis/flow/control

   // TODO: add control-flow rules

Modules consist of sections for imports, control-flow rules, data-flow properties and rules, lattices and functions. 

Imports
^^^^^^^

.. code-block:: doc-cf-[

  imports

    [module-ref*]
    
    external
    
      [module-ref*]

A module can import definitions from other modules by importing the other module. Imports are specified in an ``imports`` section, which lists the modules being imported. A module reference can be:

* A module identifier, which imports a single module with that name.
* A wildcard, which imports all modules with a given prefix. A
  wildcard is like a module identifier, but with a dash as the last
  part, as in :doc-lex:`{name "/"}+ "/-"`.

A wildcard import does not work recursively. For example,
``analysis/-`` would imports ``analysis/functions``, and
``analysis/classes``, but not ``analysis/lets/recursive``.

External imports allow you to import module of for example Stratego, to import the signatures of the abstract syntax you wish to match on. 

*Example.* A main module importing several submodules.

.. code-block:: flowspec

   module liveness

   imports
     control

     external
       signatures/-

Control Flow
^^^^^^^^^^^^

.. code-block:: doc-cf-[

  control-flow rules

    [control-flow-rule*]

The first step of analysis in FlowSpec is to define the control-flow through a program. This connection is established with rules that match patterns of abstract syntax and providing the control-flow of that pattern. 

Rules
-----

A normal control-flow rule maps an abstract syntax pattern to a list of control-flow edges. 

.. code-block:: doc-cf-[

  cfg [pattern*] = [{cfg-edges ","}+]

These edges can start from the special ``entry`` and ``exit`` control-flow nodes that are provided to connect the pattern to the wider control-flow graph. Subtrees matched in the abstract syntax pattern are usually used directly at one side of an edge to connect their corresponding sub-control-flow graph. They can also be inserted as direct control-flow nodes using the ``node`` keyword. This is rarely used. More likely, you may want to insert the whole matched pattern as a node. The ``this`` keyword can be used for that. 

.. code-block:: doc-lex

  cfg-edges = {cfg-edge-end "->"}+

  cfg-edge-end = "entry"
               | "exit"
               | variable
               | "node" variable
               | "this"

A common case exists where you merely wish to register a pattern as a control-flow graph node. Rather than write out ``cfg [pattern] = entry -> this -> exit``, you can write ``node [pattern]`` for this. 

*Example.* Module that defines control-flow for some expressions

.. code-block:: flowspec

   module control
  
   control-flow rules
  
     node Int(_)
     cfg Add(l, r) = entry -> l -> r -> this -> exit

Root rules
----------

A root of the control-flow defines the ``start`` and ``end`` nodes of a control-flow graph. You can have multiple control-flow graphs in the same AST, but not nested ones. Each control-flow graph has a unique ``start`` and ``end`` node. A ``root`` control-flow rule introduces the ``start`` and ``end`` node. In other control-flow rules these nodes can be referred to for abrupt termination. 

.. code-block:: doc-lex

  cfg-edge-end = ...
               | "start"
               | "end"

*Example.* Module that defines control-flow for a procedure, and the return statement that goes straight to the end of the procedure. 

.. code-block:: flowspec

   module control
  
   control-flow rules
  
     cfg root Procedure(args, _, body) = start -> args -> body -> end
     cfg Return(_) = entry -> this -> end

Data Flow (under construction)
^^^^^^^^^

Data-flow analysis in FlowSpec is based on named *properties*. Data-flow properties are defined in a property definition section, their rules are defined in a property rules section. Properties have an associated lattices, whose operations take care of merging data at merge points in the control-flow. 

.. code-block:: doc-cf-[

  

Lattices (under construction)
^^^^^^^^
