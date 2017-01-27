.. highlight:: dynsem

.. _dynsemreference:

==================
Language reference
==================

This page is a syntax-oriented language reference for DynSem.

.. todo:: This page is work-in-progress and many parts of the language are not yet documented.

-----------------
Modules
-----------------

.. describe:: module

      module

      imports

      signature

      rules

.. _dynsem_reference_signatures:

-----------------
Signature section
-----------------

.. describe:: signature

  The signatures section of a DynSem module provides definitions for program abstract syntax and for additional entities used in the specification of a language's dynamic semantics.

  sorts
    Define sorts of program and value terms, separated by white space. For example:

    .. code-block:: dynsem

        sorts Exprs Stmts

    A number of sorts are built-in sorts in DynSem:

      String
        strings as values or program terms

      Int
        integers.

      Float
        decimals

      Bool
        booleans. Literals of sort Bool are `true` and `false`

      List(S)
        for lists of some sort `S`. `S` can be any sort

      Map(S1, S2)
        for associative arrays where keys are of sort `S1` and values are of sort `S2`

      (S1 * S2 * ... * Sn)
        for tuples of arbitrary arity. `S1`, `S2`, ... can be any sort.

  sort aliases
    Declare sort synonyms. Sort aliases are useful to define shorthands for composed sorts such as for Maps and Lists. For example:

    .. code-block:: dynsem

      sort aliases
        Env = Map(String, Value)
        SciNum = (Float * Int)

    declares `Env` as a sort alias for `Map(String, Value)`. Wherever the sort `Map(String, Value)` is used, the alias `Env` can be used instead. The example also declares `SciNum` as a sort alias for the pair of a `Float` and an `Int`.

    .. note:: sort-aliases are only syntactic sugar for their aliased sorts and sorts can therefore not be distinguished based on name. For example if two sort aliases `Env1` and `Env2` are defined for `Map(String, Value)` they all become equal and there is no type difference between `Env1` and `Env2`. One can now see `Env1 = Env2 = Map(String, Value)`.

  variables
    Defines variable prefix schemes. Variable schemes take the form `ID = S` and express the expectation that all variables prefixed with ID are of the sort S. A variable is part of the scheme X if it's name begins with X and is either followed only by numbers and/or apostrophes, or is followed by _ followed by any valid identifier. For example given the scheme:

      .. code-block:: dynsem

        variables
          v : Value

      the following are valid variable names: **v1**, **v2**, **v'**, **v'''**, **v1'**, **v_foo**.

      .. note:: Variable schemes can be useful in combination with [implicit reductions][1] to concisely express the expected sort.

  components
    Define semantic components. A semantic component has a label and a term type. All uses of the component will have a term of that type. All semantic components must be declared before use:

    .. code-block:: dynsem

      components
        E : Env
        H : Heap

    declares the components *E* and *H* of types *Env* and *Heap*, respectively. The declared components can now be used in arrow declarations and rules. Each semantic component declaration implicitly introduces a variable scheme for the component name and type. The example above introduces variable schemes:

    .. code-block:: dynsem

      variables
        E : Env
        H : Heap

    for ease of use.

  constructors
    Define constructors for program and value terms. There are two constructor variants:

      regular constructors
        Define regular constructors. Definitions take the form `NAME: {SORT "*"}* -> SORT`, where `NAME` is the name of the constructor, followed by the sorts of the children of the constructor, and where the last `SORT` is the sort of the constructor. Example:

        .. code-block:: dynsem

          constructors
            Plus: Exprs * Exprs -> Exprs

      implicit constructors
        Define unary constructors which can be implicitly constructed/deconstructed in pattern matches and term constructions. For example, the constructor:

        .. code-block:: dynsem

          constructors
            OkV: V -> O {implicit}

        declares the **OkV** unary constructor. In term constructions where a term of sort **O** is expected but a term *t* of sort **V** is provided, the constructor **OkV** is automatically constructed to surround term *t* to become `Ok(t)`. In pattern matches where a term of sort **O** is provided but a term of sort **V** is expected, a pattern match for the term **OkV** is automatically inserted.

  arrows
    Declare named reduction relations. Relations in DynSem have to be declared before they are used to define reductions over them. Declarations take the form `S1 -ID-> S2`. Such a declaration makes the relation `-ID->` (where ID is the relation name) available to reduce terms of sort `S1` (input sort) to terms of sort `S2` (output sort). For example, the relation declaration:

      .. code-block:: dynsem

          arrows
            RO* |- Exprs :: RW-IN* -eval-> Values :: RW-IN*

    declares relation **eval** to relate terms of the **Exprs** sort to terms of the **Values** sort. The declared relation has read-only components **RO*** and read-write components **RW***. Component declarations are optional but they are obeyed. Components associated with arrows are determined by merging the declaration components with those gathered from use sites of the arrows.

    Multiple relations with the same name may be declared as long as their input sorts are different. Relations cannot be distinguished by their output sort; it is invalid to define two relations with the same input sort, same name but different output sorts.

    .. note:: It is valid to have multiple identical arrow declarations.

    The name-part of the relation declaration may be omitted, such that the following is legal:

    .. code-block:: dynsem

          arrows
            Exprs --> Values

      meta-functions
        Define singleton reductions:

        .. code-block:: dynsem

          arrows
            concat(String, String) --> String

        which can be read as "define meta-function **concat** which reduces two terms of sort **String** to a term of sort **String**".

  native operators
    These are natively defined (in Java) operators.
    .. error:: Not documented

  native datatypes
    These define datatypes implemented natively (in Java) which can be used inside DynSem specifications.
    .. error:: Not documented

-------------
Rules section
-------------

.. describe:: rules

  The rules section of a DynSem module is used to specify inductive definitions for reduction relations of program terms. A rule follows the following scheme:

  .. code-block:: dynsem

    RO* |- PAT :: RW-IN* --> T :: RW-OUT*
    where
      PREM+.

  For example:

  .. code-block:: dynsem

    E |- Box(e) :: H h --> BoxV(addr) :: H h''
    where
      E |- e :: H h --> v :: H h';
      E |- allocate(v) :: H h' --> addr :: H h''.

  ``PAT`` is a pattern match on the input term of the rule. If the pattern match succeeds the rule applies to the term and the variables in the pattern ``PAT`` are bound in the scope of the rule. ``RO*`` and ``RW-IN*`` are optional comma-separated lists of input semantic components, read-only and read-write, respectively. ``PREM+`` is a semicolon-separated list of premises that the rule uses to compute the result term ``T``. ``RW-OUT*`` is an optional comma-separated list of the read-write semantic components that are outputed from the rule.

  premises
    Premises are constructs in a rule used by a rule to reduce the input term to the output term.

    relation premises
      Relation premises apply a reduction of a term to a resulting term. They take the form:

      .. code-block:: dynsem

        RO* |- T :: RW-IN* --> PAT :: RW-OUT*

      ``RO*`` is an optional comma-separated list of read-only semantic components that are propagated into the target relation. ``T`` is a term construction that builds the input term for the target reduction. Examples of valid term constructions are: variable reference, constructor application, list construction. ``RW-IN*`` is an optional comma-separated list of read-write semantic components that are propagated into the target relation. The elements of ``RO*`` and ``RW-IN*``, and ``T`` are all term constructions, i.e. may not contain match symbols or unbound variables. ``PAT`` is a match pattern  applied to the term resulting after the application of the arrow ``-->`` to the term ``T``. ``RW-OUT*`` is an optional comma-separated list of match patterns applied to the read-write semantic components emitted by the applied relation.

      A concrete example of a relation premise is:

      .. code-block:: dynsem

        E |- e :: H h --> v :: H h'

      where the term which variable ``e`` binds to is reduced over the relation ``-->`` to a term which is variable ``v`` is bound to. The term ``E`` is a read-only component passed into the reduction. Terms ``h` and ``h'`` pass and match the read-write semantic component of type ``H``.

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
        }.

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
        }.

      where there are two cases for ``fs``, one handling a non-empty list and the other handling an empty list. An example of the ``otherwise`` case is:

      .. code-block:: dynsem

        Ifz(NumV(ci), e1, e2) --> v
        where
          case ci of {
            0 =>
              e1 --> v
            otherwise =>
              e2 --> v
          }.

    where the ``otherwise`` case is handled if none of patterns of the other cases match. A rule may only have one ``otherwise`` case and it must be the last case.

.. _dynsem_reference_configfile:

------------------
Configuration file
------------------

.. describe:: dynsem.properties

  The *dynsem.properties* file specifies configuration parameters for the DynSem interpreter and interpreter generator. Such a file is required for every  project from which a DynSem-based interpreter will be derived.


    source.language = SIMPL
      Name of the language. May be any valid Java identifier

    source.version = 0.1
      Version of the language/semantics. Any valid version, e.g. 1.2.3 is permitted.

    source.mimetype = application/x-simpl
      (optional) mime type for files of this language

    source.table = target/metaborg/sdf.tbl
      (optional) path to parse table for programs in the language.

    source.startsymbol = Prog
      Start symbol for parsing programs of this language.

    source.initconstructor.name = Program
      Constructor name of the term where program reduction begins.

    source.initconstructor.arity = 1
      Arity of the reduction entry-point constructor.

    interpreter.fullbacktracking = false
      (optional) Enable full backtracking support in the interpreter. If full backtracking is disabled, once the interpreter descends into a reduction premise it is committed to successfully applying one of the rules for that reduction. If full backtracking is enable, the interpreter treats the inability to apply successfully apply a reduction as a regular failure of a pattern match and bails out of the currently evaluated rule to attempt others. In this case, currently evaluated rules are peeled off until a succeeding alternative is found, or the top-level rule is peeled off and the interpreter halts.

    interpreter.safecomponents = false
      (optional) Enables safe semantic components operations. When enabled all semantic component operations that write or yield a `null` semantic component will cause the interpreter to halt immediately.

    interpreter.termcaching = false
      (optional) Enables inline caching of terms and pattern matching results. This can be make a performance difference for programs which are longer running or contain loops. Caching is disabled by default.

    interpreter.vmargs =
      (optional) Customize arguments passed to the JVM. For example setting this option to -ea will enable assertions in the running JVM. The arguments passed should not be surrounded by quotes.

    project.path = ../simpl.interpreter/
      Path to the interpreter project. The path must be eithe relative to the language project or absolute.

    project.groupid = org.metaborg
      Maven Group Identifier for the interpreter project.

    project.artifactid = simpl.interpreter
      Maven Artifact Identifier for the interpreter project.

    project.create = true
      (optional) Enable generation of an interpreter project and associated launch configuration. Defaults to false. When enabled, during generation of the interpreter a project will also be generated including all required directories. A pom.xml file will also be created. The project will not be automatically imported in the Eclipse workspace. The generator will also create a launch configuration which can be used in Eclipse.

    project.clean = true
      (optional) Enable cleaning of the target project before writing files. Defaults to false.

    project.javapackage = simpl.interpreter.generated
      (optional) Package to contain all generated Java classes. Defaults to GROUPID.ARTIFACTID.interpreter.generated.

    project.nativepackage = simpl.interpreter.natives
      Package name for manually implemented interpreter nodes

    project.preprocessor = org.metaborg.lang.sl.interpreter.natives.DesugarTransformer
      (optional) Fully qualified class name of a custom program pre-processor. The pre-processor will be invoked on the program AST prior to evaluation. Default to the identity transformation. See `IdentityTransformer`_ for an example.

    project.ruleregistry = org.metaborg.lang.sl.interpreter.natives.SLRuleRegistry
      (optional) Fully qualified class name of a manually implemented rule registry.

    project.javapath = src/main/java
      (optional) Path relative to the interpreter project where Java code will reside.

    project.specpath = src/main/resources/specification.aterm
      (optional) Path in interpreter project for the DynSem specification file.

    project.tablepath     = src/main/resources/parsetable.tbl
      (optional) Path in interpreter project for parse table


.. _IdentityTransformer:  https://github.com/metaborg/dynsem/blob/master/org.metaborg.meta.lang.dynsem.interpreter/src/main/java/org/metaborg/meta/lang/dynsem/interpreter/terms/ITermTransformer.java#L16
