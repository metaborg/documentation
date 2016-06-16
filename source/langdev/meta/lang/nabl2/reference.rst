Language Reference
==================

.. highlight:: nabl2

Modules
-------
               
NaBL2 specifications are written in a file with the ``.nabl2``
extension. These files have the following form::
 
   module [ModuleId]

   [Section*]

Module identifiers are defined as ``Id ( "/" Id)*``, one or more
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
     
Type signatures
---------------
               
Type signatures specify the types that are used in the
specification. A type signature section has the form::

  type signatures

    [TypeSignature*]

A type signature has the form ``Id "(" {TypeSort ","}* ")"``. A type
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

Labels must upper-case letters, i.e. match ``[A-Z]``. The ``labels``
and ``order`` directives can appear zero or more times, the
``well-formedness`` can appear at most once.

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

.. todo:: This part of the documentation is still being written.
 





          
 
.. code-block:: sdf3

   Section = [
     type signatures [TypeSignature*]
   ]
           
   TypeSignature = ...
   
.. code-block:: sdf3

   Section = [
     resolution parameters
       labels [{Label ","}*]
       order [{Label[ < ]Label ","}*]
       well-formedness [LabelRegex]
   ]

   Label      = [a-zA-Z]
   
   LabelRegex = Label
   LabelRegex = [[LabelRegex]*]
   LabelRegex = [[LabelRegex] . [LabelRegex]]
   LabelRegex = [[LabelRegex] & [LabelRegex]]
   LabelRegex = [[LabelRegex] | [LabelRegex]]
   LabelRegex = [([LabelRegex])]

.. code-block:: sdf3

   Section = [
     constraint-generation rules
       [Rule*]
   ]

   Rule = [
     init \[\[ [Pattern] \]\] :=
       [Constraint] [New?].
   ]
   Rule = [
     [RuleId] \[\[ [Pattern] ^ ([{Scope ","}*]) : [Type] \]\] :=
       [Constraint] [New?].
   ]

   Constraint = [[RuleId] \[\[ [Var] ^ ([{Scope ","}*]) : [Type] \]\]]
   
   New = [, new [{Scope ","}*]]
   
   Pattern = ...
   Type = ...

.. code-block:: sdf3

   Constraint = [[Constraint], [Constraint]]
   Constraint = [([Constraint])]

   Constraint = [[X] == [X]]
   Constraint = [[X] != [X]]

   Constraint = [[X] <- [X]]
   Constraint = [[X] -> [X]]
   Constraint = [[X] -[Label|[-]]-> [X]]
   Constraint = [[X] =[Label|[=]]=> [X]]
   Constraint = [[X] <=[Label|[=]]= [X]]

   Constraint = [[X] <! [X]]
   Constraint = [[X] <? [X]]

