=====================
NaBL2 Migration Guide
=====================

.. role:: nabl2(code)
   :language: nabl2
   :class: highlight

.. role:: statix(code)
   :language: statix
   :class: highlight

Terms
^^^^^

All sorts and constructors must be explicitly defined in Statix in
:statix:`sorts` and :statix:`constructors` signatures. Sorts in Statix
are mostly similar to terms in NaBL2. Notable differences:

* There is no catch-all sort :nabl2:`term` in Statix.
* There are not sort variables in Statix.
* List sorts in Statix are written as :statix:`list(X)` for some sort `X`.

Statix signatures for language syntax can be generated from SDF3
definitions with the :doc:`signature generator <signature-generator>`.

Signature
---------

Name Resolution
^^^^^^^^^^^^^^^

Name resolution in NaBL2 haevily relies on occurrences and their
unique identity. In Statix, the notion of a stand-alone reference is
replaced by the notion of a query. Therefore, the use of occurrences
is now discouraged in favour of regular terms, relations, and and
predicates for the different namespaces.

.. code-block:: nabl2

   signature 

     namespaces
       Var

     name resolution
       labels P
       well-formedness P*
       order D < P

.. code-block:: statix

   signature

     relations
       var : string * TYPE

     name-resolution
       labels P

   rules

     declareVar : string * TYPE * scope

     declareVar(x, T, s) :-
       !var[x, T] in s.

     resolveVar : scope * string -> TYPE

     resolveVar(s, x) = T :-
     {x'}
       query var
         filter P* and { x' :- x' == x}
         min $ < P and true
         in s |-> [(_, (x, T))],
       @x.ref := x'.

Things to note:

* Each namespace gets its own relation, and set of predicates to
  declare and resolve in that namespace (``declareXXX`` and
  ``resolveXXX``).
* The regular expression and order on labels is not global anymore,
  but part of the query in the ``resolveXXX`` rules.
* If a declaration should have a type associated with it, it is now
  part of the relation. The fact that it appears after the arrow
  ``->`` indicates that each declaration has a single type.
* The end-of-path label, called ``D`` in NaBL2, now has a special
  symbol ``$``, instead of the reserved name.

Functions
^^^^^^^^^

NaBL2 functions can be translated to Statix predicates in a
straight-forward manner. Note that if the function was used
overloaded,it is necessary to defined different predicates for the
different argument types.

Relations
^^^^^^^^^

Relations as they exist in NaBL2 are not supported in Statix.

Rules
-----

NaBL2 constraint generation rules must be translated to Statix
predicates and corresponding rules. Predicates in Statix are explcitly
typed, and a predicate has to be defined for each sort for which
constraint generation rules are defined.

Here are some example rules for expressions in NaBL2:

.. code-block:: nabl2

   [[ Let(binds, body) ^ (s) : T ]] :=
     new s_rec, s_rec -P-> s,
     Map1[[ binds ^ (s) ]],
     [[ body ^ (s) : T ]].
 
   [[ Bind(x, e) ^ (s, s_let) ]] :-
     [[ e ^ (s) : T ]],
     Var{x} <- s_let,
     Var{x} : T.

In Statix these would be encoded as:

.. code-block:: statix

   typeOfExp : scope * Exp -> TYPE

   typeOfExp(s, e@Let(binds, body)) = T :-
   {s_rec}
     new s_rec, s_rec -P-> s,
     bindsOk(s, binds, s_let),
     T == typeOfExp(s_rec, body),
     @e.type := T.


   bindOk : scope * Bind * scope
   bindsOk maps bindOk(*, list(*))

   bindOk(s, Bind(x, e), s_let) :-
     declareVar(x, typeOfExp(s, e), s_let).

