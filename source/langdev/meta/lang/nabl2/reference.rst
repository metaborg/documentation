Language Reference
==================

.. highlight:: nabl2

Modules
-------
               
NaBL2 specifications are written in a file with the ``.nabl2``
extension. These files have the following form::
 
   module [ModuleId]

   [Section*]

Module identifiers are defined as ``ID ( "/" ID)*``, one or more
identifiers, separated by forward slashes. Sections define imports,
type signatures, name resolution parameters, and constraint generation
rules.
   
An import sections can be used to import other modules, or
e.g. Stratego signatures, and has the following form::

   imports

     [ModuleId*]
 
In the case of an import, the last identifier can also a wildcard
(hyphen), e.g. ``signatures/-``, which will import all modules in that
directory.
     
Auxiliary definitions
---------------------

In this reference we will use the following auxiliary definitions::

  ID         = [a-Z][a-Z0-9\_]* "'"?

  Var        = ID

  Scope      = ID
  Occurrence = Namespace? "{" Term ("@" Var)?  "}"
             | Var
  Label      = [A-Z]

  Type       = ID "(" {Type ","}* ")"
             | "[" {Type ","}* "|" Type "]"
             | "[" {Type ","}* "]"
             | "(" {Type ","}* ")"
             | "\"" [^\"]* "\""
             | Scope
             | Occurrence
             | Var

Type signatures
---------------
               
Type signatures specify the types that are used in the
specification. A type signature section has the form::

  type signatures

    [TypeSignature*]

A type signature has the form ``ID "(" {TypeSort ","}* ")"``. A type
sort can be ``type``, ``occurence``, a list ``"List(" TypeSort ")"``,
or a tuple ``"(" {TypeSort ","}* ")"``.

Name resolution parameters
--------------------------
 
Resolution parameters describe the labels, label ordering, and path
well-formedness that are used to interpret the scope graph. The
section for resolution parameters has the form::

  name-resolution parameters

    labels [{Label ","}*]
    order [{Label "<" Label ","}*]
    well-formedness [WF]

The ``labels`` and ``order`` directives can appear zero or more times,
the ``well-formedness`` can appear at most once.

The well-formedness regular expressions has the following form (in
order of priority)::

  WF = Label      // label
     | WF "*"     // zero-or-more matches
     | WF "." WF  // concatenated matches
     | WF "&" WF  // match both
     | WF "|" WF  // match at least one 
     | "(" WF ")"

.. warning:: Resolution parameters spread over multiple files will not
             work be merged correctly. Multiple sections in a single
             file are correctly merged.

Constraint generation rules
---------------------------

The section for constraint generation rules has the following form::

  constraint-generation rules

    [Rule*]

Rules are syntax directed -- they match on the abstract syntax of the
language -- and can optionally be named. Rules can take parameters and
pass parameters to recursive calls. There is a special form for
initialization rules, that does not take any import
parameters. Constraint generation will start by applying an
initialization rule.

Constraint generation rules have the following form::

  <ID?> [[ <Pattern> ^ (<{Scope ","}*>) ]] :=
    <Constraint>.

  <ID?> [[ <Pattern> ^ (<{Scope ","}*>) : <Type> ]] :=
    <Constraint>.

The first is for untyped program constructs, the second for
typed. Similarly, the form of initialization rules is::

  init [[ <Pattern> ]] :=
    <Constraint>.

  init [[ <Pattern> : <Type> ]] :=
    <Constraint>.

A rule can create of new scopes, by specifying the new scopes at the
end of the constraint, as in ``[Constraint], new [{Scope ","}*]``.
    
Constraint overview
-------------------

A quick overview of the available constraints::

  true                                // true
  false                               // untrue
  [Constraint], [Constraint]          // conjunction

  [Type] == [Type]                    // equality
  [Type] != [Type]                    // inequality
  
  [Occurrence] <- [Scope]             // declaration
  [Occurrence] -> [Scope]             // reference
  [Scope] -[Label|"-"]-> [Scope]      // direct edge
  [Occurrence] =[Label|"="]=> [Scope] // associated scope
  [Occurrence] <=[Label|"="]= [Scope] // named edge

  [Type] <! [Type]                    // Subtype declaration
  [Type] <? [Type]                    // Subtype check


