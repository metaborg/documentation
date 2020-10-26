==================
Language Reference
==================

.. role:: doc-lex(code)
   :language: doc-lex
   :class: highlight

.. role:: statix(code)
   :language: statix
   :class: highlight

This section gives a systematic overview of the Statix language.
Statix specifications are organized in modules, consisting of signatures and predicate rules.

Lexical matters
---------------

Identifiers
^^^^^^^^^^^

.. code-block:: doc-lex

   id    = [A-Za-z][a-zA-Z0-9\_]*
   lc-id = [a-z][a-zA-Z0-9\_]*
   uc-id = [A-Z][a-zA-Z0-9\_]*

Most identifiers in Statix fall into one of the following categories:

* *Identifiers*, that start with a character, and must match the
  regular expression :doc-lex:`[A-Za-z][a-zA-Z0-9\_]*`.
* *Lowercase identifiers*, that start with a lowercase character, and
  must match the regular expression :doc-lex:`[a-z][a-zA-Z0-9\_]*`.
* *Uppercase identifiers*, that start with an uppercase character, and
  must match the regular expression :doc-lex:`[A-Z][a-zA-Z0-9\_]*`.

Comments
^^^^^^^^

Comments in Statix follow the C-style:

* ``// ... single line ...`` for single-line comments
* ``/* ... multiple lines ... */`` for multi-line comments

Multi-line comments can be nested, and run until the end of the file
when the closing ``*/`` is omitted.

Terms
-----

.. code-block:: doc-lex

   term = uc-id "(" {term ","}* ")"
        | "(" {term ","}* ")"
        | "[" {term ","}* "]"
        | "[" {term ","}* "|" term "]"
        | numeral
        | string
        | id
        | "_"

    numeral = "-"? [1-9][0-9]*

    string = "\"" ([^\"\\]|"\\"[nrt\\])* "\""

Modules and Tests
-----------------

Statix specifications are organized in named modules and test
files. Modules and test files can import named modules to extend and
use the predicates from the imported modules.

Modules
^^^^^^^
 
.. code-block:: doc-cf-[

   module [module-id]

     [section*]
 
Statix specifications are organized in modules. A module is identified
by a module identifier. Module identifiers consist of one or more
names seperated by slashes, as in :doc-lex:`{name "/"}+`. The names
must match the regular expression
:doc-lex:`[a-zA-Z0-9\_][a-zA-Z0-9\_\.\-]*`.

Every module is defined in its own file, with the extensions
``.stx``. The module name and the last components of the file path
must coincide.

*Example.* An empty module ``analysis/main``, defined in a file
:file:`.../analysis/main.stx`.

.. code-block:: statix

   module analysis/main

   // work on this

Modules consist of sections for imports, signatures, and rule
definitions. The rest of this section describes imports, and
subsequents sections deal with signatures and rules.

Imports
^^^^^^^
 
.. code-block:: doc-cf-[

  imports

    [module-ref*]

A module can import definitions from other modules be importing the
other module. Imports are specified in an ``imports`` section, which
lists the modules being imported.

Imports make predicates defined in the imported module visible. The
importing module can use the imported predicates, and extend the
predicates with new rules. Imports are not transitive, and locally
defined elements (e.g., sorts or predicates) shadow imported elements
of the same kind and the same name.

*Example.* A main module importing several submodules.

.. code-block:: statix

   module main

   imports

      signatures/MyLanguage-sig

      types

Tests
^^^^^

.. code-block:: doc-cf-[

   resolve [constraint]

   [section*]
 
Apart from named modules, stand-alone test can be defined in
``.stxtest`` files. All sections that are allowed in named modules are
allowed in tests as well. This means tests can have signatures, rules,
and import named modules.

*Example.* A test using the predicate ``leq`` imported from a named module.

.. code-block:: statix

   resolve {xs} concat([1,2,3], [4,5,6], xs)

   imports

     lists

Statix tests can be executed in Eclipse with the ``Spoofax > Evaluate
> Evaluate Test`` menu action. The test output contains the values of
top-level variables in the test constraint (i.e., ``xs`` in this
example), as well as any errors from failed constraints.

Signatures
----------

.. code-block:: doc-cf-[

  signatures

    [signature*]

Terms
^^^^^

Sorts
"""""

Constructors
""""""""""""

Name binding
^^^^^^^^^^^^

Relations
"""""""""

Namespaces
""""""""""

Name resolution
"""""""""""""""

Predicates and Rules
--------------------

.. code-block:: doc-cf-[

   rules

     [rule-def*]

Predicates and their rules make up the main part of a Statix
specification.

Predicate rules
^^^^^^^^^^^^^^^

.. code-block:: doc-cf-<

   <lc-id> : <{sort " * "}*>

   <rule-name?> <lc-id>(<{term ", "}*>).
   <rule-name?> <lc-id>(<{term ", "}*>) :- <constraint>.

.. code-block:: doc-lex

   rule-name = "[" id "]"

Predicates are defined with the sorts of their arguments. Rules define
the meaning of the predicate for different cases of the
arguments. Rule patterns can be non-linear, i.e., variables can appear
multiple times, in which case the terms in those positions must be
equal.

Committed choice rule selection
"""""""""""""""""""""""""""""""

Statix has a committed-choice semantics. This means that once a rule
is selected, the solver does never backtrack on that choice. That is
different from logic languages like Prolog, where rules are
optimisitically selected and the solver backtracks when the rule does
not work out.

Committed choice evaluation has consequences for inference during
constraint solving. If a predicate has multiple rules, a rule is only
selected once the constraint arguments are sufficiently instantiated.

Rule order
""""""""""

The order in which the rules of a predicate apply is determined by the
patterns it matches on, not by the order in which the rules appear in
the specification. Most specific rules apply before more general
rules. The parameter patterns are considered from left to right when
determining this order. It is an error to have rules with overlapping
patterns, where neither is more general than the other. There rules
are marked with an error.

*Example.* An ``or`` predicate that computes a logical or, with its
 last argument the result.

.. code-block:: statix

   or : Bool * Bool * Bool

   or(True(), _, b) :- b == True().
   or(_, True(), b) :- b == True().
   or(_, _, b) :- b == False().

In the example above, the rules are considered in the order they are
presented above. Beware that changing the rule order would not change
the specifications behaviour. The last rule is the most general, and
therefore comses last, as it matches any arguments. The first rule is
more specific than the second because of the left-to-right nature of
the ordering.

Functional rules
^^^^^^^^^^^^^^^^

.. code-block:: doc-cf-<

   <lc-id> : <{sort " * "}*> -> <sort>

   <rule-name?> <lc-id>(<{term ", "}*>) = <term>.
   <rule-name?> <lc-id>(<{term ", "}*>) = <term> :- <constraint>.

Predicates can be defined in functional style as well. Functional
predicates can be understood in terms of regular predicates. For
example, the ``or`` predicate can be written in functional style as
follows:

.. code-block:: statix

   or : Bool * Bool -> Bool

   or(True(), _) = True().
   or(_, True()) = True().
   or(_, _) = False().

This form is equivalent to the definition given above, however its use
in the specification is slightly different. Function predicates are
used in term positions, where they behave as a term of the output
type.

*Example.* Rule for a functional predicate to type check
 expressions. The functional predicate ``typeOfExp`` is used in two
 term positions: as the result of a fucntional rule, and in an
 equality constraint.

.. code-block:: statix

   typeOfExp : scope * Exp -> TYPE

   typeOfExp(s, Int()) = INT().

   typeOfExp(s, IfThen(c, e)) = typeOfExp(s, e) :-
     typeOfExp(s, c) == BOOL().

Every specification with functional predicates is normalized to a form
with only regular predicates. To show the normal form of a
specification in Eclipse, use the ``Spoofax > Syntax > Format
normalized AST`` menu action.

Mapping rules
^^^^^^^^^^^^^

Constraints
-----------

Base constraints
^^^^^^^^^^^^^^^^

Term equality
^^^^^^^^^^^^^
    
Name binding
^^^^^^^^^^^^

Scope graph
"""""""""""

Queries
"""""""

Occurrences
"""""""""""

Arithmetic
^^^^^^^^^^

Misc notes
----------

Error messages
^^^^^^^^^^^^^^

Debugging
^^^^^^^^^
