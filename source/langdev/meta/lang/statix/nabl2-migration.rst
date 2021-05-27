.. _statix-nabl2-migration:

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

Name resolution in NaBL2 heavily relies on occurrences and their
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

    rules

      [[ Def(x, T) ^ (s) ]] :=
        Var{x} <- s,
        Var{x} : T.

      [[ Var(x) ^ (s) : T ]] :=
        Var{x} -> s,
        Var{x} |-> d,
        d : T.


.. code-block:: statix

   signature

     relations
       var : string * TYPE

     name-resolution
       labels P

   rules

     declareVar : scope * string * TYPE

     declareVar(s, x, T) :-
       !var[x, T] in s.

     resolveVar : scope * string -> TYPE

     resolveVar(s, x) = T :-
     {x'}
       query var
         filter P* and { x' :- x' == x}
         min $ < P and true
         in s |-> [(_, (x, T))],
       @x.ref := x'.

    rules

      stmtOk : scope * Stmt

      stmtOk(s, Def(x, T)) :-
        declareVar(s, x, T);

      typeOfExp : scope * Exp -> TYPE

      typeOfExp(s, Var(x)) = T :-
        T == resolveVar(s, x).

Things to note:

* Each namespace gets its own relation, and set of predicates to
  declare and resolve in that namespace (``declareXXX`` and
  ``resolveXXX``).
* The regular expression and order on labels is not global anymore,
  but part of the query in the ``resolveXXX`` rules.
* If a declaration should have a type associated with it, it is now
  part of the relation. The fact that it appears after the arrow
  ``->`` indicates that each declaration has a single type.  As a
  result, ``declareXXX`` combines the constraints ``XXX{...} <- s,
  XXX{...} : T``. Similarly, ``resolveXXX`` combines the constraints
  ``XXX{...} -> s, XXX{...} |-> d, d : T``.
* The end-of-path label, called ``D`` in NaBL2, now has a special
  symbol ``$``, instead of the reserved name.

Functions
^^^^^^^^^

NaBL2 functions can be translated to Statix predicates in a
straight-forward manner. Note that if the function was used
overloaded,it is necessary to defined different predicates for the
different argument types.

.. code-block:: nabl2

    signature

      functions

        plusType : (Type * Type) -> Type {
          (IntTy()  , IntTy()  ) -> IntTy(),
          (StrTy()  , _        ) -> StrTy(),
          (ListTy(a), a        ) -> ListTy(a),
          (ListTy(a), ListTy(a)) -> ListTy(a)
        }

.. code-block:: statix

    plusType : Type * Type -> Type

    plusType(IntTy()  , IntTy()  ) = IntTy().
    plusType(StrTy()  , _        ) = StrTy().
    plusType(ListTy(a), a        ) = ListTy(a).
    plusType(ListTy(a), ListTy(a)) = ListTy(a).

Relations
^^^^^^^^^

Relations as they exist in NaBL2 are not supported in Statix.

An example of a subtyping relation in NaBl2 would translate as
follows:

.. code-block:: nabl2

    signature

      relations
        reflexive, transitive, anti-symmetric sub : Type * Type {
          FunT(-sub, +sub),
          ListT(+sub)
        }

    rules

      [[ Class(x, superX, _) ^ (s) ]] :=
        ... more constraints ...,
        ClassT(x) <sub! ClassT(superX).

      [[ Def(x, T, e) ^ (s) ]] :=
        [[ e ^ (s) : T' ]],
        T1 <sub? T2.

.. code-block:: statix

   rules

     subType : TYPE * TYPE

     subType(FunT(T1, T2), FunT(U1, U2)) :-
       subType(U1, T1),
       subType(T2, T1).

     subType(ListT(T), ListT(U)) :-
       subType(T, U).

     subType(ClassT(s1), ClassT(s2)) :-
       ... check connectivity of s1 and s2 in the scope graph ...

In this case implementing the ``subType`` rule for ``ClassT`` requires
changing the encoding of class types. Instead of using names, we use
the class scope to identify the class type. This pattern is know as
_Scopes as Types_. Subtyping between class scopes can be checked by
checking if one scope is reachable from the other.

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
