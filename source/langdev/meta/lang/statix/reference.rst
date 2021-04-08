.. _statix-reference:

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

.. warning::

   This section is currently incomplete. The information that is there is up-to-date, but many constructs are not yet documented.

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
names separated by slashes, as in :doc-lex:`{name "/"}+`. The names
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

*Example.* A test using the predicate ``concat`` imported from a named module.

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

.. code-block:: doc-cf-[

  [signature] = ...
            | "sorts" [sort-decl*]

  [sort-decl] = [uc-id]
            | [uc-id] "=" [sort]

  [sort] = "string"
       | "int"
       | "list" "(" [sort] ")"
       | "(" [{sort "*" }*] ")"
       | "scope"
       | "occurrence"
       | "path"
       | "label"
       | "astId"
       | [uc-id]

Statix uses algebraic data types to validate term well-formedness. First,
Statix has several built-in scalar data types, such as ``int``, ``string``
and ``scope``. In addition, Statix also has two built-in composite data
types: tuples and lists. Next to the built-in sorts, custom syntactic
categories can be defined by adding a name to a ``sorts`` subsection of
the ``signatures`` section.

*Example.* Declaration of a custom sort ``Exp`` and a sort alias for
identifiers.

.. code-block:: statix

  signature
    sorts
      Exp
      ID = string

Constructors
""""""""""""

.. code-block:: doc-cf-[

   [signature] = ...
             | "constructors" [cons-decl*]

   [cons-decl] = [uc-id] ":" [uc-id]
             | [uc-id] ":" [{sort "*"}*] "->" [uc-id]

In order to construct or match actual data terms, constructors for these terms
need to be declared. Constructors without arguments are declared by stating the
constructor name and its sort, separated by a colon. For constructors with
arguments, the argument sorts are separated by an asterisk, followed by an
arrow operator and the target sort.

*Example.* Declaration of various constructors for the ``Exp`` sort.

.. code-block:: statix

  signature
    sorts
      ID = string
      Exp

    constructors
      True : Exp
      Var  : ID -> Exp
      Plus : Exp * Exp -> Exp

The example above states three constructors for the ``Exp`` sort. The ``True``
constructor has no arguments, the ``Var`` constructor has a single name as
argument, while the ``Plus`` constructor takes two subexpressions as arguments.

Name binding
^^^^^^^^^^^^

Relations
"""""""""

.. code-block:: doc-cf-[

   [signature] = ...
             | "relations" [rel-decl*]

   [rel-decl] = [uc-id] ":" [{sort "*"}*]
            | [uc-id] ":" [{sort "*"}*] "->" [sort]

In Statix, relations associate data with a scope. All used relations and the
type of their data must be declared in the ``relations`` section. Each
relation declaration consist of the name of the relation and the arguments
it accepts.

Relation declarations come in two flavors. There is a _predicative_ variant and
a _functional_ variant. The functional variant has the last two arguments
separated with a ``->``, which indicates that the relation is intended to map
the first terms to the last term (as in the regular notion of functions).

Apart from intended semantics, the difference between the variants has to do
with the formulation of the predicates of queries. Please refer to the
`Queries`_ section for more information on querying relations. Otherwise, both
ways of declaring relations are equivalent. In fact, during compilation, the
functional variant is normalized to the predicate variant.

*Example.* Declaration of a predicative relation ``this`` and a functional
relation ``var``.

.. code-block:: Statix

  signature
    sorts
      TYPE
      ID = string

    relations
      this : TYPE
      var  : ID -> TYPE

Namespaces
""""""""""

.. warning::

	 Usage of namespaces is strongly discouraged and will be removed or revised in a future version of Statix.

Name resolution
"""""""""""""""

.. warning::

	 Usage of namespaces is strongly discouraged and will be removed or revised in a future version of Statix.

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
optimistically selected and the solver backtracks when the rule does
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
patterns, where neither is more general than the other. These rules
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
therefore comes last, as it matches any arguments. The first rule is
more specific than the second because of the left-to-right nature of
the ordering.

Non-linear patterns
"""""""""""""""""""

Non-linear patterns are patterns in which at least one pattern variable
occurs multiple times. Such patterns only match on terms that have
equal subterms at the positions where such a variable occurs.

*Example.* An ``xor`` predicate that computes a logical exclusive or,
with its last argument the result.

.. code-block:: statix

   xor: Bool * Bool * Bool

   xor(B, B, b) :- b == False().
   xor(_, _, b) :- b == True().

In the example above, the first rule for ``xor`` has a non-linear
pattern, because the variable ``B`` occurs both at the first and at the
second position. In this way, the first rule only matches on equal input
terms (either ``True(), True(), b`` or ``False(), False(), b``).

Regarding the ordering of rules by specificity, it holds that an occurrence
of a variable that is seen earlier is regarded as more specific than a
free variable. Therefore, the first rule of ``xor`` takes precedence
over the second rule. Bound variables are as specific as concrete constructors.

Ordering rules with non-linear patterns
"""""""""""""""""""""""""""""""""""""""

Careful attention to rule order needs to be paid when non-linear patterns and
concrete constructor patterns are mixed. For example, consider a ``subtype``
predicate with rules for record types and equal types:

.. code-block:: statix

  subtype: TYPE * TYPE

  subtype(REC(s_rec1), REC(s_rec2)) :- /* omitted */.
  subtype(T, T).

In this example, equal record types match on both rules. Because of the left
to right nature of the rule application, the first rule will be chosen,
because for the first argument, the ``REC`` constructor is regarded as
more specific than the (at that position free) ``T`` variable.

If that behavior is not desired, an explicit rule for the intersection of
the domains of the pair of rules in question needs to be added. This rule
is more specific than both of the other rules, and is therefore selected
for any matching input. For example, consider this augmented ``subtype``
predicate with an additional rule for equal record types:

.. code-block:: statix

  subtype: TYPE * TYPE

  subtype(REC(s_rec), REC(s_rec)).
  subtype(REC(s_rec1), REC(s_rec2)) :- /* omitted */.
  subtype(T, T).

In this example, we added a rule that declares that a record type is a subtype
of itself. This rule ensures that equal record types are regarded as subtypes
without verifying additional constraints. So, while it seems that the first and
the third rules are equivalent, and the first one superfluous, this is not the
case because the rule ordering will choose the second rule when the behavior of
the third rule is desired.

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

.. _constraints_queries:
Queries
"""""""

Occurrences
"""""""""""

Arithmetic
^^^^^^^^^^
