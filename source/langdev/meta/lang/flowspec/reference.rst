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

Terms can be constructed terms from either the abstract syntax tree or a user-defined algebraic data type. Tuples are built-in, as are sets and maps. The latter two have special construction and comprehension syntax. 

.. code-block:: doc-lex

  term = ctor-id "(" {term ","}* ")"
       | "(" {term ","}* ")"
       | "{" {term ","}* "}"
       | "{" term "|" {term ","}* "}"
       | "{" {(term "|->" term) ","}* "}"
       | "{" term "|->" term "|" {(term "|->" term) ","}* "}"

Pattern matching is done with patterns for constructed terms and tuples. Parts can also be bound to a variable or ignored with a wildcard. 

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
------------

.. code-block:: doc-cf-[

  control-flow rules

    [control-flow-rule*]

The first step of analysis in FlowSpec is to define the control-flow through a program. This connection is established with rules that match patterns of abstract syntax and providing the control-flow of that pattern. 

Rules
^^^^^

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
^^^^^^^^^^

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

Data Flow
---------

Data-flow analysis in FlowSpec is based on named *properties*. Data-flow properties are defined in a property definition section, their rules are defined in a property rules section. Properties have an associated lattices, whose operations take care of merging data at merge points in the control-flow. 

.. code-block:: doc-cf-[

  properties

    [property-definition*]

.. code-block:: doc-cf-[

  property rules

    [property-rule*]

Definitions
^^^^^^^^^^^

A property definition consists only of the property name, with a lowercase start and otherwise camelcase for multiple words. The lattice looks like a type expression but uses a lattice name. This lattice instance is used internally for the data-flow computation. 

.. code-block:: doc-lex

    property-definition = name ":" lattice


Rules
^^^^^

A property rule consists of the name of the property, a pattern within round brackets and an expression after the equals sign. The pattern is matches a control-flow graph node by its originating AST, and another control-flow graph node before or after it by name. The expression describes the effect of the matched control-flow graph node, in terms of a change to the value from the adjacent control-flow graph node matched. All rules of a property need to propagate the information in the same way, either forward or backward.

Each property needs to have at least one rule with the *start* or *end* pattern. This is pattern matches the extremal node of a control-flow graph and defines the initial value there. With set-based analyses this is usually the empty set, as usually nothing is known at that point. The extremal node needs to match the direction of the rules, with *start* for a forward analysis and *end* of a backward analysis. 

.. code-block:: doc-lex

    property-rule = name "(" prop-pattern ")" "=" expr
    prop-pattern = name "->" pattern
                 | pattern "->" name
                 | pattern "." "start"
                 | pattern "." "end"

Lattices
--------

Lattices definitions are defined in their own section. 

.. code-block:: doc-cf-[

  lattices

    [lattice-definition*]

Each lattice definition consists of a name and a number of components: the underlying type, the least-upper-bound or join operation between two lattice values (the less-than-or-equal comparison is derived from this operation), the top value and the bottom value. The type is usually defined by the user in another section as an algebraic data type, and operated on with pattern matching. 

.. code-block:: doc-cf-[

    [name] where
      type = [type]
      lub([name], [name]) = [expr]
      top = [expr]
      bottom = [expr]

Types
-----

Algebraic data types can be defined in a types block. 

.. code-block:: doc-cf-[

  types

    [type-definition*]

Each type has a name and one or more option preceded by a vertical bar. Each option has a constructor and zero or more arguments in round brackets. 

.. code-block:: doc-cf-[

    [name] =
      [("|" ctor-id "(" {type ","}* ")")+]

Expressions
-----------

Expressions consist of:

  1. integer operations (addition, subtraction, multiplication, division, modulo, negate, comparison)
  2. boolean operations (and, or, not)
  3. set/map operations (comprehension, union, intersection, set/map minus, containment/lookup)
  4. value construction (integers, boolean, strings, terms, sets, maps)
  5. pattern matching
  6. references (variables matched in a pattern, top or bottom of a lattice)
  7. function application (user defined or lattice operation (leq, lub))
  8. property lookup in property rule right-hand sides (looks like single argument function application)

Functions
---------

Functions are defined in their own section. 

.. code-block:: doc-cf-[

  functions

    [function-definition*]

A function definition consists of a name, typed arguments and a function body expression. 

.. code-block:: doc-cf-[

    [name]([{(name ":" type) ","}+]) =
      [expr]
