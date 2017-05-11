.. _dynsemrules:

===============
Reduction rules
===============

Reduction rules are the principal DynSem mechanism to specify relations (reductions) from program terms to values. Defining rules consists of declaring them as **arrows** and then giving them implementations as rules.

.. _dynsemarrowsignatures:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Signatures of arrows, components and meta-functions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. describe:: components

  Define semantic components. A semantic component has a label and a term type. All uses of the component will have a term of that type. All semantic components must be declared before use:

  .. code-block:: dynsem

    signature
      components
        E : Env
        H : Heap

  declares the components *E* and *H* of types *Env* and *Heap*, respectively. The declared components can now be used in arrow declarations and rules. Each semantic component declaration implicitly introduces a variable scheme for the component name and type. The example above implicitly introduces the following variable schemes:

  .. code-block:: dynsem

    signature
      variables
        E : Env
        H : Heap

  for ease of use.


.. describe:: arrows

    Declare named reduction relations. Relations in DynSem have to be declared before they are used to define reductions over them. Declarations take the form `S1 -ID-> S2`. Such a declaration makes the relation `-ID->` (where ID is the relation name) available to reduce terms of sort `S1` (input sort) to terms of sort `S2` (output sort). For example, the relation declaration:

      .. code-block:: dynsem

          signature
            arrows
              RO* |- Exprs :: RW-IN* -eval-> Values :: RW-IN*

    declares relation **eval** to relate terms of the **Exprs** sort to terms of the **Values** sort. The declared relation has read-only components **RO*** and read-write components **RW***. Component declarations are optional but they are obeyed. Components associated with arrows are determined by merging the declaration components with those gathered from use sites of the arrows.

    Multiple relations with the same name may be declared as long as their input sorts are different. Relations cannot be distinguished by their output sort; it is invalid to define two relations with the same input sort, same name but different output sorts.

    .. note:: It is valid to have multiple identical arrow declarations.

    The name-part of the relation declaration may be omitted, such that the following is legal:

    .. code-block:: dynsem

          signature
            arrows
              Exprs --> Values

.. describe:: meta-functions

      Define singleton reductions:

      .. code-block:: dynsem

        signature
          arrows
            concat(String, String) --> String

      which can be read as "define meta-function **concat** which reduces two terms of sort **String** to a term of sort **String**". Semantic components may be declared on meta-functions identically to arrow declarations.

.. describe:: native operators

    These are natively defined (in Java) operators.

    .. error:: Not documented

~~~~~
Rules
~~~~~

The rules section of a DynSem module is used to specify inductive definitions for reduction relations of program terms. A rule follows the following scheme:

.. code-block:: dynsem

  RO* |- PAT :: RW-IN* --> T :: RW-OUT*
  where
    PREM+

For example:

.. code-block:: dynsem

  E |- Box(e) :: H h --> BoxV(addr) :: H h''
  where
    E |- e :: H h --> v :: H h';
    E |- allocate(v) :: H h' --> addr :: H h''

where ``PAT`` is a pattern match on the input term of the rule. If the pattern match succeeds the rule applies to the term and the variables in the pattern ``PAT`` are bound in the scope of the rule. ``RO*`` and ``RW-IN*`` are optional comma-separated lists of input semantic components, read-only and read-write, respectively. ``PREM+`` is a semicolon-separated list of premises that the rule uses to compute the result term ``T``. ``RW-OUT*`` is an optional comma-separated list of the read-write semantic components that are outputed from the rule.

.. describe:: premises

  Premises are constructs in a rule used by a rule to reduce the input term to the output term.

  relation premises
    Relation premises apply a reduction of a term to a resulting term. They take the form:

    .. code-block:: dynsem

      RO* |- T :: RW-IN* --> PAT :: RW-OUT*

    ``RO*`` is an optional comma-separated list of read-only semantic components that are propagated into the target relation. ``T`` is a term construction that builds the input term for the target reduction. Examples of valid term constructions are: variable reference, constructor application, list construction. ``RW-IN*`` is an optional comma-separated list of read-write semantic components that are propagated into the target relation. The elements of ``RO*`` and ``RW-IN*``, and ``T`` are all term constructions, i.e. may not contain match symbols or unbound variables. ``PAT`` is a match pattern  applied to the term resulting after the application of the arrow ``-->`` to the term ``T``. ``RW-OUT*`` is an optional comma-separated list of match patterns applied to the read-write semantic components emitted by the applied relation.

    A concrete example of a relation premise is:

    .. code-block:: dynsem

      E |- e :: H h --> v :: H h'

    where the term which variable ``e`` holds is reduced over the relation ``-->`` to a term which is stored in variable ``v``. The term ``E`` is a read-only component passed into the reduction. Terms ``h` and ``h'`` pass and match, respectively the read-write semantic component labeled ``H``.

  term equality premise
    The term equality premise allows checks for equality of two terms. The premise takes the following form:

    .. code-block:: dynsem

      T1 == T2

    where ``T1`` and ``T2`` are the constructions of the two terms whose equality is asserted. The primary use of the equality premise is to determine whether whether two bound variables contain terms that match, but can be used for general purpose equality comparison:

    .. code-block:: dynsem

      a == b;
      l == [];
      "hello" == s1;
      i1 = 42;
      b1 == true;

  pattern-match premise
    A pattern matching premise is used to perform pattern matching on terms and to bind new variables. The syntax of a premise follows the following form:

    .. code-block:: dynsem

      T => PAT

    Where ``T`` is a term construction (e.g. variable reference or constructor application), and ``PAT`` is the pattern to match against (such as a constructor, term literal, list). All variables in ``T`` must be bound and none of the variables in ``PAT`` may be bound. Examples of valid pattern matching premises are:

    .. code-block:: dynsem

      a => b;
      a => Plus(e1, e2);
      l => [x|xs];
      b => Ifz(ec, _, _);
      x => 42;
      s => "Hello";

    The pattern matching premise can also be used to bind variables to constructed terms:

    .. code-block:: dynsem

      42 => x;
      Plus(a, b) => plusexp;
      "hello" => s1;
      ["hello","world"] => s2;

    A special ``@`` notation allows variables to be bound in nested pattern matches. For example the following premise:

    .. code-block:: dynsem

      exp => Plus(c@Num(_), e@Plus(_, _))

    both pattern matches the first and second subterms of ``Plus`` and binds variables ``c`` and ``e``. More precisely the variables ``c`` and ``e`` will be bound to ``Num`` and ``Plus`` terms, respectively.

    .. warning:: Non-linear pattern matches are not permitted. For example the following are invalid pattern match premises:

      .. code-block:: dynsem

        exp => Plus(e, e);

      because the pattern on the right hand side contains a variable that is already bound (the second occurrence of ``e`` is bound by the first occurrence). One can express the behavior intended above using the term equality premise:

      .. code-block:: dynsem

        exp => Plus(e1, e2);
        e1 == e2;

  case pattern matching premise
    The case pattern matching premise allows behavior to be associated with multiple patterns. It takes the following form:

    .. code-block:: dynsem

      case T of {
        CASE+
      }

    where ``T`` is a term construction and ``CASE+`` is a list of cases which may take one the following forms:

    .. code-block:: dynsem

      PAT =>
        PREM*

      otherwise=>
        PREM*

    The first form is for regular pattern matching cases. An example is:

    .. code-block:: dynsem

      case fs of {
        [f | fs'] =>
          f -load-> _;
          fs' -load-> _
        [] =>
      }

    where there are two cases for ``fs``, one handling a non-empty list and the other handling an empty list. An example of the ``otherwise`` case is:

    .. code-block:: dynsem

      Ifz(NumV(ci), e1, e2) --> v
      where
        case ci of {
          0 =>
            e1 --> v
          otherwise =>
            e2 --> v
        }

  where the ``otherwise`` case is handled if none of patterns of the other cases match. A rule may only have one ``otherwise`` case and it must be the last case.


~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Explication of semantic components
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Semantic components are used to carry contextual information through reduction rules. They are typically used to model variable environments and heaps, but can be used for anything. A cache store can be propagated as a semantic component for example. There are two kinds of components: read-only (RO) and read-write (RW). The two kinds differ in how they are propagated through the rules. Reduction rules which do not need a particular component can ommit mentioning it, it will automatically propagated to/through rules that need it.

We informally describe how components are implicitly propagated. Let the following (quite abstract) module:

.. code-block:: dynsem

  module myspec

  signature
    sorts
      X
      P1 P2 P3

    components
      A : X
      B : X
      C : X

    constructors
      foo1: P1
      foo2: P2
      bar: P2
      baz: P3

    arrows
      P1 --> Int
      P2 --> Int
      P3 --> Int

  rules
    C |- foo1() --> i
    where
      bar() :: C --> i :: C'

    foo2() :: B --> 99 :: B

    bar() --> baz()

    A |- baz() --> 42


Semantic components are explicated in the following phases:

1. Gather explicitly used semantic components per arrow
2. Gather inter-arrow dependencies
3. Explicate components in arrow signatures
4. Explicate components in each rule

Whenever a rule explicitly mentions a semantic component it implicitly declares that the arrow which the rule belongs to uses that component. That is the case with rule ``foo2()``: it introduces the dependency on RW component ``B`` of arrow ``P1 --> Int``. Rule ``baz()`` introduces the dependency of rule ``P3 --> Int`` on RO component ``A``. The premise of rule ``foo1()`` introduces a dependency of arrow ``P1 --> Int`` on RO component ``C``, and a dependency of arrow ``P2 --> Int`` on RW component ``C``. Note here that one arrow may use a component as RO and (implicitly) pass it to other rules as RW, and viceversa.

Looking only at explicit uses we can explicate the arrow declarations:

.. code-block:: dynsem

  signature
    ...
    arrows
      C |- P1 :: B --> Int :: B
      P2 :: C --> Int :: C
      A |- P3 --> Int
    ...

For ease of referecing, let us label each arrow with an explicit name:

.. code-block:: dynsem

  signature
    ...
    arrows
      C |- P1 :: B -e1-> Int :: B
      P2 :: C -e2-> Int :: C
      A |- P3 -e3-> Int
    ...

We gather the dependencies between arrows: ``-e1-> => -e2->``, ``-e2-> => -e3->``. Whenever an arrow ``-e1->`` depends on another arrow ``-e2->``, the former must provide the required components to the latter, at every invocation. This means that components are inherited from the arrow it depends on. Looking at inter-arrow dependencies, we can propagate the components in the arrow declarations:

.. code-block:: dynsem

  signature
    ...
    arrows
      C, A |- P1 :: B -e1-> Int :: B
      A |- P2 :: C -e2-> Int :: C
      A |- P3 -e3-> Int
    ...

After explication of components in arrow declarations is complete, we can explicate their uses in every rule, independently:

.. code-block:: dynsem

  ...
  rules
    C, A |- foo1() :: B --> i :: B
    where
      A |- bar() :: C --> i :: C'

    C, A |- foo2() :: B --> 99 :: B

    A |- bar() :: C --> baz() :: C

    A |- baz() --> 42
