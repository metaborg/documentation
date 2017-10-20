==================
Language Reference
==================

.. role:: doc-lex(code)
   :language: doc-lex
   :class: highlight

.. role:: nabl2(code)
   :language: nabl2
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

Terms and patterns
------------------

.. code-block:: doc-lex

   term = ctor-id "(" {term ","}* ")"
        | "(" {term ","}* ")"
        | "[" {term ","}* "]"
        | "[" {term ","}* "|" term "]"
        | namespace-id? "{" term ("@" var-id)? "}"

   pattern = ctor-id "(" {pattern ","}* ")"
           | "(" {pattern ","}* ")"
           | "[" {pattern ","}* "]"
           | "[" {pattern ","}* "|" pattern "]"
           | "_"
           | var-id

Modules
-------

.. code-block:: doc-cf-[

   module [module-id]

     [section*]
 
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
 
.. code-block:: doc-cf-[

  imports

    [module-ref*]

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

.. code-block:: doc-cf-[

  signatures

    [signature*]

Signatures contain definitions and parameters used in the
specification. In the rest of this section, signatures for terms, name
binding, functions and relations, and constraint rules are described.
 
Terms
^^^^^

Terms in NaBL2 are multi-sorted, and are defined in the ``sorts`` and
``constructors`` signatures.

Sorts
"""""

.. code-block:: doc-cf-[

   sorts

     [sort-id*]

*Available since version 2.3.0*
 
The ``sorts`` signature lists the sorts that are available. Sort are
identified by uppercase identifiers.

*Example.* Module declaring a single sort ``Type``.

.. code-block:: nabl2

   module example

   signature

     sorts Type

Constructors
""""""""""""

.. code-block:: doc-cf-[

   constructors

     [ctor-def*]

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

.. code-block:: doc-cf-[

   namespaces

     [namespace-def*]

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

.. code-block:: doc-cf-[

   name resolution
     labels
       [label-id*]
     order
       [{label-order ","}*]
     well-formedness
       [label-regexp]

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

.. code-block:: doc-cf-[

   functions

     [( function-id (":" sort-ref "->" sort-ref )?
        ("{" {function-case ","}* "}")? )*]

.. code-block:: doc-lex

   function-case = pattern "->" term

Functions available at constraint time are defined in a ``functions``
signature. A function is identified by a name, followed by a type and
the function cases. The cases are rewrite rules from the match in the
left, to the term on the right. The function cases need to be linear,
which all the variables mentioned in the right-hand side term have to
be bound in the left-hand side pattern.

The type is currently not checked, but can be used to document to
sorts of the elements in the function.

*Example.* A module that defines the ``left`` and ``right`` projection
functions for pairs.

.. code-block:: nabl2

   module example

   signature

     functions
       left : (Type * Type) -> Type {
         (x, y) -> x
       }
       right : (Type * Type) -> Type {
         (x, y) -> y
       }

Relations
"""""""""

.. code-block:: doc-cf-[

   relations

     [( relation-option* relation-id
        (":" sort-ref "*" sort-ref)?
        ("{" {variance-pattern ","}* "}")? )*]

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

The relations that are available are defined in a ``relations``
signature. A relation is identified by a name, possibly preceded by
properties of the relation, and followed by an optional type and
special cases for specific constructors.

The properties that are specificied are
enforced at runtime. The positive properties (``reflexive``,
``symmetric``, and ``transitive``) ensure that all pairs that were not
explicitly added to the relation are inferred. The negative properties
(``irreflexive``, ``anti-symmetric``, and ``anti-transitive``) are
checked when adding a pair to the relation, and result in an error in
the program if violated. The positive and negative properties are
mutually exclusive. For example, it is not allowed to specify both
``reflexive`` and ``irreflexive`` at the same time.

The type specified for the relation is currently not checked, but can
be used to document the sorts of the elements in the relation.

Variance patterns are used to specify general cases for certain
constructors. This can be used, for example, to add support for lists,
that are checked pair-wise.

*Example.* Module below defines a reflexive, transitive,
anti-symmetric subtype relation ``sub``, with the common variance on
function types, and covariant type lists.

.. code-block:: nabl2

   module example

   signature

     relations
        reflexive, transitive, anti-symmetric sub : Type * Type {
          FunT(-sub, +sub),
          [+sub]
        }

Rules
^^^^^

.. code-block:: doc-cf-[

   constraint generator

     [rule-def*]

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

.. code-block:: doc-cf-[

   rules

     [rule*]

The rules section of a module defines syntax-directed constraint
generation rules.

Init rule
^^^^^^^^^

.. code-block:: doc-cf-<

   init ^ ( <{parameter ","}*> ) <(":" type)?> := <{clause ","}+> .
   init ^ ( <{parameter ","}*> ) <(":" type)?> .

Constraint generation starts by applying the default rule to the
top-level constructor. The ``init`` rule, which must be specified
exactly once, provides the initial values to the parameters of the
default rule.

Init rules come in two variants. The first variant outputs rule
clauses. These can create new scopes, or defined constraints on
top-level declarations. If the rule has no clauses, the rule can be
closed without a clause definition. For example, :nabl2:`init ^ ().`
is shorthand for :nabl2:`init ^ () := true.`

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

.. code-block:: doc-cf-<

   <rule-def?> [[ <pattern> ^ ( <{parameter ","}*> ) <(":" type)?> ]] := <{clause ","}+> .
   <rule-def?> [[ <pattern> ^ ( <{parameter ","}*> ) <(":" type)?> ]] .

.. code-block:: doc-lex

   rule-def = rule-id ("(" {rule-id ","}* ")")?

Constraint generation rules are defined for the different syntactic
constructs in the object language. Rules can accept a number of
parameters and an optional type. The parameters are often used to pass
around scopes, but can be used for other parameters as well. The rule
clause consists of a comma-separated list of constraints.

Rules can be named to distinguish different versions of a rule for the
same syntactic construct. Named rules can also accept rule parameters,
which makes it possible to write higher-order rules. For example, the
:nabl2:`Map(X)[[ list(a) ^ (b) ]]` rule accepts as argument the rule
that will be applied to the elements in the list. Note that only a
single rule with a certain name can be defined per AST pattern.

Rules are distinguished by name and arity, so ``Map1`` is different
from ``Map1(X)``. There is no overloading based on the number of
parameters, or the presence or absence of a type.

All variables in the rule's clauses that are not bound in the pattern,
the parameters, the type, or a ``new`` directive, are automatically
inferred to be unification variables.

The rule form without clauses is equal to a rule that simply return
``true``. For example, :nabl2:`[[ Int(_) ^ (s) : IntT() ]].` is
shorthand for :nabl2:`[[ Int(_) ^ (s) : IntT() ]] := true.`.
   
Recursive calls
"""""""""""""""

.. code-block:: doc-lex

   clause = rule-ref "[[" var "^" "(" {var ","}* ")" (":" term)? "]]"

   rule-ref = rule-id ("(" {rule-ref ","}* ")")?
            | "default"

Recursive calls are used to invoke constraint generation for subterms
of the current term. Recursive calls can only be made on parts of the
program AST, therefore the term argument needs to be a variable that
is bound in the current match pattern.

If no rule name is specified, the default rule will be called. Rules
that are applied are selected based on the name and the term
argument. To pass the default rule as an argument to a higher-order
rule, the ``default`` keyword is used.

There is no overloading on the number of parameters or the presence or
absence of a type. Calling a rule with the wrong number of parameters
will result in errors during constraint collection.

Delegating to other rules is *only* supported if the delegate has the
same parameters and type as the rule that is delegating.

*Example.* A module defining and calling different rules.

.. code-block:: nabl2

   module example

   rules

     [[ Int(_) ^ (s) : IntT() ]].

     Map1[[ [x|xs] ^ (s) : [ty|tys] ]] :=
       [[ x ^ (s) : ty ]],        // call default rule on head
       Map1[[ xs ^ (s) : tys ]].  // recurse on tail

     Map1(X)[[ [x|xs] ^ (s) : [ty|tys] ]] :=
       X[[ x ^ (s) : ty ]],         // call rule X on head
       Map1(X)[[ xs ^ (s) : tys ]]. // recurse on tail, passing on X

The rule ``Map1`` could also be defined in terms of ``Map1(X)`` as
follows:

.. code-block:: nabl2

   module example

   rules

     Map1[[ xs ^ (s) : tys ]] :=
       Map1(default)[[ xs ^ (s) : tys ]].

Constraints
-----------

This section gives an overview of the different constraints that can
be used in clauses of constraint rules.

Base constraints & error messages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: doc-lex

   clause = "true"
          | "false" message?
 
   message = "|" message-kind message-content message-position?

   message-kind     = "error" | "warning" | "note"
   message-content  = "\"" chars "\""
                    | "$[" (chars | "[" term "]")* "]"
   message-position = "@" var-id

The two basic constraints are ``true`` and ``false``.  The constraint
``true`` is always satisfied, while ``false`` is never satisfied.

The message argument to a constraint specifies the error message that
is displayed if the constraint is not satisfied. The severity of the
error can be specified to be ``error``, ``warning`` or ``note``. The
message itself can either be a simple string, or an interpolated
string that can match terms and variables used in the rule. By default
the error will appear on the match term of the rule, but using the
``@t`` syntax the location can be changed to ``t``. The variable ``t``
needs to be bound in the AST pattern of the rule.

*Example.* Some constraints with different ways of specifying error messages.

.. code-block:: nabl2

   false | error @t1                    // generic error on whole term
   false | note "Simple note"           // specific note on whole term
   false | warning $[Consider [t2]] @t1 // formatted warning on first subterm

Term equality
^^^^^^^^^^^^^
    
.. code-block:: doc-lex

   clause = term "==" term message?
          | term "!=" term message?
 
Equality of terms is specified used equality and inequality
constraints. An equality constraint ``t1 == t2`` specifies that the
two terms need to be equal. If the terms contain variables, the solver
infers values for them using unificiation. If unification leads to any
conflicts, an error will be reported.

Inequality is specified with a constraint of the form ``t1 !=
t2``. Inequality constraints cannot always be solved if both sides
contain variables. The inequality between two variables depends on the
values that will be inferred for them. Only after a value is assigned,
will the inequality be tested. If the constraint cannot be solved,
because some variables have remained free, an error is reported as
well.

*Example.* A few constraints for term (in)equality.

.. code-block:: nabl2

   ty == FunT(ty1, ty2) | error $[Expected function type, but got [ty]]
   ty != NilT()

Name binding
^^^^^^^^^^^^

Name binding is concerned with constraints for building a scope graph,
constraints for resolving references and accessing properties of
declarations, and name sets that talk about sets of declarations or
references in the scope graph.

Occurrences
"""""""""""

.. code-block:: doc-lex

   occurrence = namespace-id? "{" term position? "}"

   position   = "@" var-id

References and declarations in the scope graph are not simply names,
but have a richer representation called an occurrence. An occurrence
consists of the name, the namespace, and a position.

The name can be any term, although usually it is a term from the
AST. Names are not restricted to strings, and can contain terms with
subterms if necessary. However, it is required that the name contains
only literals, or variables that are bound in the match pattern.

Namespaces allow us to separate different kinds of names, so that type
names do not resolve to variables or vice versa.  If there is only one
namespace in a language, it can be omitted and the default namespace
will be used.

The position is necessary to differentiate different occurrences of
the same name in the program, and is the connection between the AST
and the scope graph. The position can usually be omitted, in which
case the position of the name is taken if it is an AST term, or the
position of the match term, if the name is a literal.

*Example.* Several of occurrences, with explicit and implicit
compontents.

.. code-block:: nabl2

   Var{x}         // variable x, x must be bound in match
   {y}            // no namespace, y must be bound in match
   Type{a}        // type a, a must e bound in match
   Var{"this" @c} // this variable with explicit position
   Var{This()}    // this variable using a constructor instead of a string
   Type{"Object"} // literal type occurrence

Scope graph
"""""""""""

.. code-block:: doc-lex

   clause = occurrence "->" scope
          | occurrence "<-" scope
          | scope "-"label-id"->" scope
          | occurrence "="label-id"=>" scope
          | occurrence "<="label-id"=" scope
          | "new" var-id*

Scope graph constraints construct a scope graph. Names in the graph
are represented by occurrences. Scopes in the graph are abstract, but
can be created using the :nabl2:`new` directive. Rules usually receive
scope parameters that allows them to extend and connect to the
surrounding scope graph.

*Example.* Rules that build a scope graph.

.. code-block:: nabl2

   [[ Module(x,imps,defs) ^ (s) ]] :=
     Mod{x} <- s,                       // module declaration
     new ms,                            // new scope for the module
     Mod{x} ===> ms,                    // associate module scope with the declaration
     Map2[[ imps ^ (ms, s) ]],          // recurse on imports
     Map1[[ defs ^ (ms) ]].             // recurse on statements

   [[ Import(x) ^ (ms, s) ]] :=
     Mod{x} -> s,                       // module reference
     Mod{x} <=== ms.                    // import in the module scope

   [[ TypeDef(x,_) ^ (s) ]] :=
     Type{x} <- s.                      // type declaration

   [[ TypeRef(x) ^ (s) ]] :=
     Type{x} -> s.                      // type reference

   [[ VarDef(x, t) ^ (s) ]] :=
     Var{x} <- s,                       // variable declaration
     [[ t ^ (s) ]].                     // recurse on type annotation

   [[ VarRef(x) ^ (s) ]] :=
     Var{x} -> s.                       // variable reference

Name resolution
"""""""""""""""

.. code-block:: doc-lex

   clause = occurrence "|->" occurrence message?
          | occurrence "?="Label"=>" scope message?
          | occurrence ":" type priority? message?
          | occurrence"."prop-id ":=" term priority? message?

   priority = "!"*
 
*Example.* Rules that build a scope graph.

.. code-block:: nabl2

   [[ TypeDef(x,t) ^ (s) ]] :=
     Type{x} <- s,                      // type declaration
     Type{x} : t !.                     // semantics type of the type declaration

   [[ TypeRef(x) ^ (s) : ty ]] :=
     Type{x} -> s.                      // type reference
     Type{x} |-> d,                     // resolve reference
     d : ty.                            // semantic type of the resolved declaration

   [[ VarDef(x, t) ^ (s) ]] :=
     Var{x} <- s,                       // variable declaration
     [[ t ^ (s) : ty ]],                // recurse on type annotation
     Var{x} : ty !,                     // type of the variable declaration
     [[ t ^ (s) ]].                     // recurse on type annotation

   [[ VarRef(x) ^ (s) : ty ]] :=
     Var{x} -> s,                       // variable reference
     Var{x} |-> d,                      // resolve variable reference
     d : ty.                            // type of resolved declaration

.. _name-sets:

Name sets
"""""""""

.. code-block:: doc-lex

   name-set = "D(" scope ")"("/"namespace-id)?
            | "R(" scope ")"("/"namespace-id)?
            | "V(" scope ")"("/"namespace-id)?
            | "W(" scope ")"("/"namespace-id)?

   set-proj = "name"

   message-position = "@NAMES"

Name sets are set expressions (see :ref:`sets`) that are based on the
scope graph. They can be used in set constraints to test for
properties such as duplicate names, shadowing, or complete coverage.

The expression :nabl2:`D(s)` represents the set of all declarations in
scope ``s``, and similarly :nabl2:`R(s)` refers to all references in
scope ``s``. The set of all visible declarations in ``s`` is
represented by :nabl2:`V(s)`, and the set of all reachable
declarations in ``s`` is represented by :nabl2:`W(s)`. The difference
between visible and reachable declarations is that de former takes the
label order into account to do shadowing, while the latter only
considers path well-formedness but does not shadow.

All the name sets can also be restricted to declarations or references
in a particular namespace by appending a forward-slash and the
namespace. For example, all variable declarations in scope ``s`` would
be represented by :nabl2:`D(s)/Var`.

Name sets support the ``name`` set projection that makes it possible
to compare occurrences by name only, ignoring the namespace and
position.

When using set constraints on name sets, there are some options to
relate the error messages to the elements in the set, instead of the
term where the constraint was created. First, the position in the
message can be set to :nabl2:`@NAMES`. This makes error messages
appear on the names in the set. For example, :nabl2:`distinct/name
D(s)/Var | error @NAMES` will report errors on all the names that are
duplicate. If you want to refer to the name in the error message, use
the :nabl2:`NAME` keyword. For example, in the message :nabl2:`error
$[Duplicate name [NAME]] @NAMES`, the keyword will be replaced by the correct name.

.. _sets:

Sets
^^^^

.. code-block:: doc-lex

   clause = "distinct"("/"set-proj)? set-expr message?
          | set-expr "subseteq"("/"set-proj)? set-expr message?
          | set-expr "seteq"("/"set-proj)? set-expr message?

   set-expr = "0"
            | "(" set-expr "union" set-expr ")"
            | "(" set-expr "isect"("/"set-proj)? set-expr ")"
            | "(" set-expr "minus"("/"set-proj)? set-expr ")"
            | name-set

Set constraints are used to test for distinct elements in a set, or
subset relations between sets. Set expressions allow the usual set
operations such as union and intersection.

The constraint :nabl2:`distinct S` check whether any elements in the
set ``S`` appears multiple times. Note that this works because the
sets behave like multisets, so every element has a count associated
with it as well. If the set ``S`` supports projections, it is possible
to test whether the set contains any duplicates after
projection. Which projections are available depends on the sets
involved. For example, when working with sets of occurrences (see :ref:`name-sets`), the
``name`` projection can be used.

Constraints :nabl2:`S1 subseteq S2` and :nabl2:`S1 seteq S2` test
whether ``S1`` is a subset of ``S2``, or if the sets are equal,
respectively. Both constraints also support projections, written as
:nabl2:`S1 subseteq/proj S2` and :nabl2:`S1 seteq/proj S2`.

The basic set expressions that are supported are ``0`` for the empty
set, :nabl2:`(S1 union S2)` for set union, :nabl2:`(S1 isect S2)` for
intersection, and :nabl2:`(S1 minus S2)` for set difference. Set
intersection and difference can also be performed under projection,
written as :nabl2:`(S1 isect/proj S2)` and :nabl2:`(S1 minus/proj S2)`.
This means the comparison to check if elements from the two sets
match is done after projecting the elements. However, the resulting
set will still contain the original elements, not the projections.For
example, this can be used to compute sets of occurrences where a
comparison by name is necessary.

*Example.* Set constraints over name sets.

.. code-block:: nabl2

   distinct/name D(s)/Var // variable names in s must be unique

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

