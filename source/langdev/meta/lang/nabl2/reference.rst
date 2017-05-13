==================
Language Reference
==================

.. role:: doc-lex(code)
   :language: doc-lex
   :class: highlight

.. role:: doc-cf(code)
   :language: doc-cf
   :class: highlight

This section gives a systematic overview of the NaBL2 language.

Lexical matters
---------------

Identifiers
^^^^^^^^^^^

Most identifiers in NaBL2 fall into one of two categories, which we
will refer to as:

* *Lowercase identifiers*, that start with a lowercase character, and
  must match the regular expression :doc-lex:`[a-z][a-zA-Z0-9\_]*`.
* *Uppercase identifiers*, that start with an uppercase character, and
  must match the regular expression :doc-lex:`[A-Z][a-zA-Z0-9\_]*`.

Comments
^^^^^^^^

Comments in NaBL2 follow the C-style:

* ``// ... single line ...`` for single-line comments
* ``/* ... multiple lines ... */`` for multi-line comments

Multi-line comments can be nested, and run until the end of the file
when the closing ``*/`` is omitted.


Modules
-------

.. code-block:: doc-cf

   module \[module-id]

     \[section*]
 
NaBL2 specifications are organized in modules. A module is identified
by a module identifier. Module identifiers consist of one or more
names seperated by slashes, as in :doc-lex:`{name "/"}+`. The names
must match the regular expression
:doc-lex:`[a-zA-Z0-9\_][a-zA-Z0-9\_\.\-]*`.

Every module is defined in its own file, with the extensions
``.nabl2``. The module name and the file paths must coincide.

   *Example.* An empty module ``analysis/main``, defined in a file
   :file:`.../analysis/main.nabl2`.

   .. code-block:: nabl2

      module analysis/main

      // work on this

Modules consist of sections for imports, signatures, and rule
definitions. The rest of this section describes imports, and
subsequents sections deal with signatures and rules.

Imports
^^^^^^^
 
.. code-block:: doc-cf

  imports

    \[module-ref*]

A module can import definitions from other modules be importing the
other module. Imports are specified in an ``imports`` section, which
lists the modules being imported. A module reference can be:

* A module identifier, which imports a single module with that name.
* A wildcard, which imports all modules with a given prefix. A
  wildcard is like a module identifier, but with a dash as the last
  part, as in :doc-lex:`{name "/"}+ "/-"`.

A wildcard import does not work recursively. For example,
``analysis/-`` would imports ``analysis/functions``, and
``analysis/classes``, but not ``analysis/lets/recursive``.

   *Example.* A main module importing several submodules.

   .. code-block:: nabl2

      module main

      imports

         builtins
         functions/-
         classes/-
         types

Signatures
----------

.. code-block:: doc-cf

  signatures

    \[signature*]

Signatures contain definitions and parameters used in the
specification. In the rest of this section, signatures for terms, name
binding, functions and relations, and constraint rules are described.

Term sorts and constructors
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: doc-cf

   sorts

     \[sort-id*]

   constructors

     \[ctor-def*]

Terms in NaBL2 are multi-sorted, and are defined in the ``sorts`` and
``constructors`` signatures.

The ``sorts`` signature lists the sorts that are available. Sort are
identified by uppercase identifiers.

   *Example.* Module declaring one sort ``Type``.

   .. code-block:: nabl2

      module example

      signature

        sorts Type

Constructors are defined in a ``constructors`` signature, and
identified by uppercase identifiers.  Constructor definitions are
written as follows:

* *Nullary constructors* are defined using :doc-lex:`ctor-id ":" sort-id`.
* *N-ary constructors* are defined using :doc-lex:`ctor-id ":"
  {sort-ref "*"}+ "->" sort-id`.

Sort references can refer to sorts defined in the signature, or to
several builtin sorts. One can refer to the following sorts:

* *User-defined sorts* using its :doc-lex:`sort-id`.
* *Tuples* using :doc-lex:`"(" {sort-ref "*"}* ")"`.
* *Lists* using :doc-lex:`"list(" sort-ref ")"`.
* *Maps* using :doc-lex:`"map(" sort-ref "," sort-ref ")"`.
* Generic *terms* using the :doc-lex:`"term"` keyword. The term sort
  contains all possible terms, and can be seen as a supertype of all
  other sorts.
* *Strings* using the :doc-lex:`"string"` keyword.
* *Scopes* using the :doc-lex:`"scope"` keyword.
* *Occurrences* using the :doc-lex:`"occurrence"` keyword.
* Sort *variables* are written using lowercase identifiers.

   For example, a module specifying the types for a language with
   numbers, functions, and records identified by scopes, might look
   like this:
   
   .. code-block:: nabl2

      module example

      signature

         sorts Type

         constructors
           NumT : Type
           FunT : Type * Type -> Type
           RecT : scope -> Type

Name binding
^^^^^^^^^^^^

Two signatures are relevant for name binding. One describes
namespaces, that are used for occurrences, and one describes the
parameters for name resolution.

Namespaces
""""""""""

.. code-block:: doc-cf

   namespaces

     \[namespace-def*]

Namespaces are defined in the ``namespaces`` signature. Namespaces are
identified by uppercase identifiers. A namespace definition has the
following form: :doc-lex:`namespace-id (":" sort-ref)?
properties?`. The optional :doc-lex:`":" sort-ref` indicates the sort
used for the types of occurrences in this namespace.

Other properties of occurrences in this namespace, are specified as a
block of the form :doc-lex:`"{" {(prop-id ":" sort-ref) ","}*
"}"`. Properties are identified by lowercase identifiers, and ``type``
is a reserved property keyword that cannot be used.

   The following example defines three namespaces: 1) for modules,
   without a type or properties, 2) for classes, which has a property
   to record the body of the class, and 3) for variables, which has a
   type property, of sort ``Type``. For completeness the sort
   declaration for ``Type`` is shown as well.

   .. code-block:: nabl2

      module example

      signature

        sorts Type
      
        namespaces
          Module
          Class { body : term }
          Var : Type

Name resolution
"""""""""""""""

.. code-block:: doc-cf

   name resolution
     labels
       \[label-id*]
     order
       \[{label-order ","}*]
     well-formedness
       \[label-regexp]

Name resolution parameters are specified in a ``name-resolution``
signature. Note that this block can only be specified once per
project.

Edge labels are specified using the ``labels`` keyword, followed by a
list of uppercase label identifiers. The label ``"D"`` is reserved and
signifies a declaration in the same scope.

The specificity order on labels is specified using the ``order``
keyword, and a comma-separated list of :doc-lex:`label-ref "<"
label-ref` pairs. Label references refer to a label identifier, or the
special label ``D``.

Finally, the well-formedness predicate for paths is specified as a
regular expression over edge labels, after the ``well-formedness``
keyword. The regular expression has the following syntax:

* A *literal* label using its :doc-lex:`label-id`.
* *Empty* sequence using :doc-lex:`"e"`.
* *Concatenation* with :doc-lex:`regexp regexp`.
* *Optional* (zero or one) with :doc-lex:`regexp "?"`.
* *Closure* (zero or more) with :doc-lex:`regexp "*"`.
* *Non-empty* (one or more) with :doc-lex:`regexp "+"`.
* Logical *or* with :doc-lex:`regexp "|" regexp`.
* Logical *and* with :doc-lex:`regexp "&" regexp`.
* *Empty* language using :doc-lex:`"0"`, i.e., this will not match on
  anything.
* Parenthesis, written as :doc-lex:`"(" regexp ")"` , can be used to
  group complex expressions.

   The following example shows the default parameters, that are used
   if no parameters are specified:
  
   .. code-block:: nabl2
   
      name resolution
        labels
          P I
   
        order
          D < P,
          D < I,
          I < P
   
        well-formedness
          P* I*
 
Functions and relations
^^^^^^^^^^^^^^^^^^^^^^^

Functions
"""""""""

.. code-block:: doc-cf

   functions

Relations
"""""""""

.. code-block:: doc-cf

   relations

     \[( relation-option* relation-id (":" sort-ref "*" sort-ref)? "{" {variance-pattern ","}* "}" )*]

.. code-block:: doc-lex

    relation-option = "reflexive" | "irreflexive"
                    | "symmetric" | "anti-symmetric"
                    | "transitive" | "anti-transitive"
 
    variance-pattern = ctor-id "(" {variance ","}* ")"
                     | "[" variance  "]"
                     | "(" {variance ","}* ")"

    variance = "="
             | "+"relation-id?
             | "-"relation-id?

Rules
^^^^^

.. code-block:: doc-cf

   constraint generator

     \[rule-def*]

The type signatures for constraint generation rules are defined in a
``constraint generator`` signature. Rule signatures describe the sort
being matched, the sorts of any parameters, and optionally the sort of
the type. A rule signature is written as :doc-lex:`rule-id? "[["
sort-ref "^" "(" {sort-ref ","}* ")" (":" sort-ref)?  "]]"`. Rules are
identified by uppercase identifiers.

   The following example shows a module that defines a default rule
   for expressions, and rules for recursive and parallel bindings. The
   rule for expressions has one scope parameter, and expressions are
   assigned a type of sort ``Type``. The bind rules are named, and
   match on the same AST sort ``Bind``. They take two scope
   parameters, and do not assign any type to the bind construct.

   .. code-block:: nabl2

      module example

      signature

        constraint generator
          [[ Expr ^ (scope) : Type ]]
          BindPar[[ Bind ^ (scope, scope) ]]
          BindRec[[ Bind ^ (scope, scope) ]]

NaBL2 supports higher-order rules. In those cases, the
:doc-lex:`rule-id` is extended with a list of parameters, written as
:doc-lex:`rule-id "(" {rule-id ","}* ")"`.

   For example, the rule that applies some rule, given as a parameter
   ``X``, to the elements of a list has signature ``Map1(X)[[ a ^ (b)
   ]]``. Note that we use variables ``a`` and ``b`` for the AST and
   parameter sort respectively, since the map rule is polymorphic.

Rules
-----

.. code-block:: doc-cf

   rules

     \[rule*]

The rules section of a module defines syntax directed constraint
generation rules.

Init rule
^^^^^^^^^

.. code-block:: doc-cf

   init ^ ( \<{parameter ","}*> ) \<(":" type)?> := \<{clause ","}+> .
   init ^ ( \<{parameter ","}*> ) \<(":" type)?> .

Constraint generation starts by applying the default rule to the
top-level constructor. The ``init`` rule, which must be specified
exactly once, provides the initial values to the parameters of the
default rule.

Init rules come in two variants. The first variant outputs rule
clauses. These can create new scopes, or defined constraints on
top-level declarations. If the rule has no clauses, the rule can be
closed without a clause definition. For example, ``init ^ ().`` is
shorthand for ``init ^ () := true.``

   In the example module below, the default rule takes one scope
   parameter. The init rule creates a new scope, which will be used as
   the initial value for constraint generation.

   .. code-block:: nabl2

      module example

      rules

        init ^ (s) := new s.

        [[ t ^ (s) ]].

Generation rules
^^^^^^^^^^^^^^^^

.. code-block:: doc-cf

   \<rule-id?> [[ \<pattern> ^ ( \<{parameter ","}*> ) \<(":" type)?> ]] := \<{clause ","}+> .
   \<rule-id?> [[ \<pattern> ^ ( \<{parameter ","}*> ) \<(":" type)?> ]] .

Variables not matched in the pattern, bound to parameters, or new
scopes, are automatically inferred to be unification variables.
   
.. code-block:: doc-lex

   pattern = ctor-id "(" {pattern ","}* ")"
           | "(" {pattern ","}* ")"
           | "[" {pattern ","}* "]"
           | "[" {pattern ","}* "|" pattern "]"
           | "_"
           | var-id
 
Recursive calls
"""""""""""""""


Constraints
-----------

Error messages
^^^^^^^^^^^^^^

.. code-block:: doc-lex

   clause = "true"
          | "false" message?
 
   message = "|" message-kind message-content message-position?

   message-kind     = "error" | "warning" | "note"
   message-content  = "\"" chars "\""
                    | "$[" (chars | "[" term "]")* "]"
   message-position = "@" var-id

Term equality
^^^^^^^^^^^^^
    
.. code-block:: doc-lex

   clause = term "==" term message?
          | term "!=" term message?
 
   term = ctor-id "(" {term ","}* ")"
        | "(" {term ","}* ")"
        | "[" {term ","}* "]"
        | "[" {term ","}* "|" term "]"
        | namespace-id? "{" term ("@" var-id)? "}"

Name binding
^^^^^^^^^^^^

Scope graph
"""""""""""

.. code-block:: doc-lex

   clause = occurrence "->" scope
          | occurrence "<-" scope
          | scope "-"label-id"->" scope
          | occurrence "="label-id"=>" scope
          | occurrence "<="label-id"=" scope
          | "new" var-id*

Name resolution
"""""""""""""""

.. code-block:: doc-lex

   clause = occurrence "|->" occurrence message?
          | occurrence "?="Label"=>" scope message?
          | occurrence ":" type priority? message?
          | occurrence"."prop-id ":=" term priority? message?

   priority = "!"*
 
Set
^^^

.. code-block:: doc-lex

   clause = "distinct"("/"set-proj)? set-expr message?
          | set-expr "subseteq"("/"set-proj)? set-expr message?

   set-expr = "0"
            | "(" set-expr "union"("/"set-proj)? set-expr ")"
            | "(" set-expr "isect"("/"set-proj)? set-expr ")"
            | "(" set-expr "minus"("/"set-proj)? set-expr ")"
            | "D(" scope ")"("/"namespace-id)?
            | "R(" scope ")"("/"namespace-id)?
            | "V(" scope ")"("/"namespace-id)?
            | "W(" scope ")"("/"namespace-id)?

   set-proj = "name"

Functions and relations
^^^^^^^^^^^^^^^^^^^^^^^
            
.. code-block:: doc-lex

   clause = term "<"relation-id?"!" term message?
          | term "<"relation-id?"?" term message?
          | term "is" function-ref "of" term message?

   function-ref = function-id
                | relation-id".lub"
                | relation-id".glb"

Symbolic
^^^^^^^^

.. code-block:: doc-lex

   clause = "?-" term
          | "!-" term

