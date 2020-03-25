```eval_rst
.. highlight:: str
```

# 5. Rewriting Strategies

## 5.1. Limitations of Term Rewriting

In [Chapter 4][1] we saw how term rewriting can be used to implement transformations on programs represented by means of terms. Term rewriting involves exhaustively applying rules to subterms until no more rules apply. This requires a _strategy_ for selecting the order in which subterms are rewritten. The `innermost` strategy introduced in [Chapter 4][1] applies rules automatically throughout a term from inner to outer terms, starting with the leaves. The nice thing about term rewriting is that there is no need to define traversals over the syntax tree; the rules express basic transformation steps and the strategy takes care of applying it everywhere. However, the complete normalization approach of rewriting turns out not to be adequate for program transformation, because rewrite systems for programming languages will often be non-terminating and/or non-confluent. In general, it is not desirable to apply all rules at the same time or to apply all rules under all circumstances.

Consider for example, the following extension of `prop-dnf-rules` with distribution rules to achieve conjunctive normal forms:

    module prop-cnf
    imports prop-dnf-rules
    rules
      E : Or(And(x, y), z) -> And(Or(x, z), Or(y, z))
      E : Or(z, And(x, y)) -> And(Or(z, x), Or(z, y))
    strategies
      main = io-wrap(cnf)
      cnf  = innermost(E)

This rewrite system is non-terminating because after applying one of the and-over-or distribution rules, the or-over-and distribution rules introduced here can be applied, and vice versa.

       And(Or(Atom("p"),Atom("q")), Atom("r"))
    ->
       Or(And(Atom("p"), Atom("r")), And(Atom("q"), Atom("r")))
    ->
       And(Or(Atom("p"), And(Atom("q"), Atom("r"))),
           Or(Atom("r"), And(Atom("q"), Atom("r"))))
    ->
       ...

There are a number of solutions to this problem. We'll first discuss a couple of solutions within pure rewriting, and then show how programmable rewriting strategies can overcome the problems of these solutions.

### 5.1.1. Attempt 1: Remodularization

The non-termination of `prop-cnf` is due to the fact that the and-over-or and or-over-and distribution rules interfere with each other. This can be prevented by refactoring the module structure such that the two sets of rules are not present in the same rewrite system. For example, we could split module `prop-dnf-rules` into `prop-simplify` and `prop-dnf2` as follows:

    module prop-simplify
    imports prop-eval-rules
    rules
      E : Impl(x, y) -> Or(Not(x), y)
      E : Eq(x, y)   -> And(Impl(x, y), Impl(y, x))

      E : Not(Not(x)) -> x

      E : Not(And(x, y)) -> Or(Not(x), Not(y))
      E : Not(Or(x, y))  -> And(Not(x), Not(y))

&nbsp;

    module prop-dnf2
    imports prop-simplify
    rules
      E : And(Or(x, y), z) -> Or(And(x, z), And(y, z))
      E : And(z, Or(x, y)) -> Or(And(z, x), And(z, y))
    strategies
      main = io-wrap(dnf)
      dnf  = innermost(E)

Now we can reuse the rules from `prop-simplify` without the and-over-or distribution rules to create a `prop-cnf2` for normalizing to conjunctive normal form:

    module prop-cnf2
    imports prop-simplify
    rules
      E : Or(And(x, y), z) -> And(Or(x, z), Or(y, z))
      E : Or(z, And(x, y)) -> And(Or(z, x), Or(z, y))
    strategies
      main = io-wrap(cnf)
      cnf  = innermost(E)

Although this solves the non-termination problem, it is not an ideal solution. In the first place it is not possible to apply the two transformations in the same program. In the second place, extrapolating the approach to fine-grained selection of rules might require definition of a single rule per module.

### 5.1.2. Attempt 2: Functionalization

Another common solution to this kind of problem is to introduce additional constructors that achieve normalization under a restricted set of rules. That is, the original set of rules `p1 -> p2` is transformed into rules of the form `f(p_1) -> p_2'`, where `f` is some new constructor symbol and the right-hand side of the rule also contains such new constructors. In this style of programming, constructors such as `f` are called _functions_ and are distinguished from constructors. Normal forms over such rewrite systems are assumed to be free of these _function_ symbols; otherwise the function would have an incomplete definition.

To illustrate the approach we adapt the DNF rules by introducing the function symbols `Dnf` and `DnfR`. (We ignore the evaluation rules in this example.)

    module prop-dnf3
    imports libstrategolib prop
    signature
      constructors
        Dnf  : Prop -> Prop
        DnfR : Prop -> Prop
    rules
      E : Dnf(Atom(x))    -> Atom(x)
      E : Dnf(Not(x))     -> DnfR(Not(Dnf(x)))
      E : Dnf(And(x, y))  -> DnfR(And(Dnf(x), Dnf(y)))
      E : Dnf(Or(x, y))   -> Or(Dnf(x), Dnf(y))
      E : Dnf(Impl(x, y)) -> Dnf(Or(Not(x), y))
      E : Dnf(Eq(x, y))   -> Dnf(And(Impl(x, y), Impl(y, x)))

      E : DnfR(Not(Not(x)))      -> x
      E : DnfR(Not(And(x, y)))   -> Or(Dnf(Not(x)), Dnf(Not(y)))
      E : DnfR(Not(Or(x, y)))    -> Dnf(And(Not(x), Not(y)))
      D : DnfR(Not(x))           -> Not(x)

      E : DnfR(And(Or(x, y), z)) -> Or(Dnf(And(x, z)), Dnf(And(y, z)))
      E : DnfR(And(z, Or(x, y))) -> Or(Dnf(And(z, x)), Dnf(And(z, y)))
      D : DnfR(And(x, y))        -> And(x, y)
    strategies
      main = io-wrap(dnf)
      dnf  = innermost(E <+ D)

The `Dnf` function mimics the innermost normalization strategy by recursively traversing terms. The auxiliary transformation function `DnfR` is used to encode the distribution and negation rules. The `D` rules are _default_ rules that are only applied if none of the `E` rules apply, as specified by the strategy expression `E <\+ D`.

In order to compute the disjunctive normal form of a term, we have to _apply_ the `Dnf` function to it, as illustrated in the following application of the `prop-dnf3` program:

    $ cat test1.dnf
    Dnf(And(Impl(Atom("r"),And(Atom("p"),Atom("q"))),ATom("p")))

    $ ./prop-dnf3 -i test1.dnf
    Or(And(Not(Atom("r")),Dnf(Dnf(ATom("p")))),
       And(And(Atom("p"),Atom("q")),Dnf(Dnf(ATom("p")))))

For conjunctive normal form we can create a similar definition, which can now co-exist with the definition of DNF. Indeed, we could then simultaneously rewrite one subterm to DNF and the other to CNF.

    E : DC(x) -> (Dnf(x), Cnf(x))

In the solution above, the original rules have been completely intertwined with the `Dnf` transformation. The rules for negation cannot be reused in the definition of normalization to conjunctive normal form. For each new transformation a new traversal function and new transformation functions have to be defined. Many additional rules had to be added to traverse the term to find the places to apply the rules. In the modular solution we had 5 basic rules and 2 additional rules for DNF and 2 rules for CNF, 9 in total. In the functionalized version we needed 13 rules _for each transformation_, that is 26 rules in total.

## 5.2. Programmable Rewriting Strategies

In general, there are two problems with the functional approach to encoding the control over the application of rewrite rules, when comparing it to the original term rewriting approach: traversal overhead and loss of separation of rules and strategies.

In the first place, the functional encoding incurs a large _overhead_ due to the explicit specification of _traversal_. In pure term rewriting, the strategy takes care of traversing the term in search of subterms to rewrite. In the functional approach traversal is spelled out in the definition of the function, requiring the specification of many additional rules. A traversal rule needs to be defined for each constructor in the signature and for each transformation. The overhead for transformation systems for real languages can be inferred from the number of constructors for some typical languages:

    language : constructors
    Tiger    : 65
    C        : 140
    Java     : 140
    COBOL    : 300 - 1200

In the second place, rewrite rules and the strategy that defines their application are completely _intertwined_. Another advantage of pure term rewriting is the separation of the specification of the rules and the strategy that controls their application. Intertwining these specifications makes it more difficult to _understand_ the specification, since rules cannot be distinguished from the transformation they are part of. Furthermore, intertwining makes it impossible to _reuse_ the rules in a different transformation.

Stratego introduced the paradigm of _programmable rewriting strategies with generic traversals_, a unifying solution in which application of rules can be carefully controlled, while incurring minimal traversal overhead and preserving separation of rules and strategies.

The following are the design criteria for strategies in Stratego:

* **Separation of rules and strategy**: Basic transformation rules can be defined separately from the strategy that applies them, such that they can be understood independently.

* **Rule selection**: A transformation can select the necessary set of rules from a collection (library) of rules.

* **Control**: A transformation can exercise complete control over the application of rules. This control may be fine-grained or course-grained depending on the application.

* **No traversal overhead**: Transformations can be defined without overhead for the definition of traversals.

* **Reuse of rules**: Rules can be reused in different transformations.

* **Reuse of traversal schemas**: Traversal schemas can be defined generically and reused in different transformations.


## 5.3. Idioms of Strategic Rewriting

In the next chapters we will examine the language constructs that Stratego provides for programming with strategies, starting with the low-level actions of building and matching terms. To get a feeling for the purpose of these constructs, we first look at a couple of typical idioms of strategic rewriting.

### 5.3.1. Cascading Transformations

The basic idiom of program transformation achieved with term rewriting is that of _cascading transformations_. Instead of applying a single complex transformation algorithm to a program, a number of small, independent transformations are applied in combination throughout a program or program unit to achieve the desired effect. Although each individual transformation step achieves little, the cumulative effect can be significant, since each transformation feeds on the results of the ones that came before it.

One common cascading of transformations is accomplished by exhaustively applying rewrite rules to a subject term. In Stratego the definition of a cascading normalization strategy with respect to rules `R1`, ... ,`Rn` can be formalized using the `innermost` strategy that we saw before:

    simplify = innermost(R1 <+ ... <+ Rn)

The argument strategy of `innermost` is a _selection_ of rules. By giving _different_ names to rules, we can control the selection used in each transformation. There can be multiple applications of `innermost` to different sets of rules, such that different transformations can co-exist in the same module without interference. Thus, it is now possible to develop a large library of transformation rules that can be called upon when necessary, without having to compose a rewrite system by cutting and pasting. For example, the following module defines the normalization of proposition formulae to both disjunctive and to conjunctive normal form:

    module prop-laws
    imports libstrategolib prop
    rules

      DefI : Impl(x, y) -> Or(Not(x), y)
      DefE : Eq(x, y)   -> And(Impl(x, y), Impl(y, x))

      DN   : Not(Not(x)) -> x

      DMA  : Not(And(x, y)) -> Or(Not(x), Not(y))
      DMO  : Not(Or(x, y))  -> And(Not(x), Not(y))

      DAOL : And(Or(x, y), z) -> Or(And(x, z), And(y, z))
      DAOR : And(z, Or(x, y)) -> Or(And(z, x), And(z, y))

      DOAL : Or(And(x, y), z) -> And(Or(x, z), Or(y, z))
      DOAR : Or(z, And(x, y)) -> And(Or(z, x), Or(z, y))

    strategies

      dnf = innermost(DefI <+ DefE <+ DAOL <+ DAOR <+ DN <+ DMA <+ DMO)
      cnf = innermost(DefI <+ DefE <+ DOAL <+ DOAR <+ DN <+ DMA <+ DMO)

      main-dnf = io-wrap(dnf)
      main-cnf = io-wrap(cnf)

The rules are named, and for each strategy different selections from the ruleset are made.

The module even defines two main strategies, which allows us to use one module for deriving multiple programs. Using the `--main` option of `strc` we declare which strategy to invoke as main strategy in a particular program. Using the `-o` option we can give a different name to each derived program.

    $ strc -i prop-laws.str -la stratego-lib --main main-dnf -o prop-dnf4

### 5.3.2. One-pass Traversals

Cascading transformations can be defined with other strategies as well, and these strategies need not be exhaustive, but can be simpler _one-pass traversals_. For example, constant folding of Boolean expressions only requires a simple one-pass bottom-up traversal. This can be achieved using the `bottomup` strategy according the the following scheme:

    simplify = bottomup(repeat(R1 <+ ... <+ Rn))

The `bottomup` strategy applies its argument strategy to each subterm in a bottom-to-top traversal. The `repeat` strategy applies its argument strategy repeatedly to a term.

Module `prop-eval2` defines the evaluation rules for Boolean expressions and a strategy for applying them using this approach:

    module prop-eval2
    imports libstrategolib prop
    rules
      Eval : Not(True())      -> False()
      Eval : Not(False())     -> True()
      Eval : And(True(), x)   -> x
      Eval : And(x, True())   -> x
      Eval : And(False(), x)  -> False()
      Eval : And(x, False())  -> False()
      Eval : Or(True(), x)    -> True()
      Eval : Or(x, True())    -> True()
      Eval : Or(False(), x)   -> x
      Eval : Or(x, False())   -> x
      Eval : Impl(True(), x)  -> x
      Eval : Impl(x, True())  -> True()
      Eval : Impl(False(), x) -> True()
      Eval : Eq(False(), x)   -> Not(x)
      Eval : Eq(x, False())   -> Not(x)
      Eval : Eq(True(), x)    -> x
      Eval : Eq(x, True())    -> x
    strategies
      main = io-wrap(eval)
      eval = bottomup(repeat(Eval))

The strategy `eval` applies these rules in a bottom-up traversal over a term, using the `bottomup(s)` strategy. At each sub-term, the rules are applied repeatedly until no more rule applies using the `repeat(s)` strategy. This is sufficient for the `Eval` rules, since the rules never construct a term with subterms that can be rewritten.

Another typical example of the use of one-pass traversals is _desugaring_, that is rewriting language constructs to more basic language constructs. Simple desugarings can usually be expressed using a single top-to-bottom traversal according to the scheme

    simplify = topdown(try(R1 <+ ... <+ Rn))

The `topdown` strategy applies its argument strategy to a term and then traverses the resulting term. The `try` strategy tries to apply its argument strategy once to a term.

Module `prop-desugar` defines a number of desugaring rules for Boolean expressions, defining propositional operators in terms of others. For example, rule `DefN` defines `Not` in terms of `Impl`, and rule `DefI` defines `Impl` in terms of `Or` and `Not`. So not all rules should be applied in the same transformation or non-termination would result.

    module prop-desugar
    imports prop libstrategolib

    rules

      DefN  : Not(x)     -> Impl(x, False())
      DefI  : Impl(x, y) -> Or(Not(x), y)
      DefE  : Eq(x, y)   -> And(Impl(x, y), Impl(y, x))
      DefO1 : Or(x, y)   -> Impl(Not(x), y)
      DefO2 : Or(x, y)   -> Not(And(Not(x), Not(y)))
      DefA1 : And(x, y)  -> Not(Or(Not(x), Not(y)))
      DefA2 : And(x, y)  -> Not(Impl(x, Not(y)))

      IDefI : Or(Not(x), y) -> Impl(x, y)

      IDefE : And(Impl(x, y), Impl(y, x)) -> Eq(x, y)

    strategies

      desugar =
        topdown(try(DefI <+ DefE))

      impl-nf =
        topdown(repeat(DefN <+ DefA2 <+ DefO1 <+ DefE))

      main-desugar =
        io-wrap(desugar)

      main-inf =
        io-wrap(impl-nf)

The strategies `desugar` and `impl-nf` define two different desugaring transformation based on these rules. The `desugar` strategy gets rid of the implication and equivalence operators, while the `impl-nf` strategy reduces an expression to implicative normal-form, a format in which _only_ implication (`Impl`) and `False()` are used.

A final example of a one-pass traversal is the `downup` strategy, which applies its argument transformation during a traversal on the way down, and again on the way up:

    simplify = downup(repeat(R1 <+ ... <+ Rn))

An application of this strategy is a more efficient implementation of constant folding for Boolean expressions:

    eval = downup(repeat(Eval))

This strategy reduces terms such as

    And(... big expression ..., False)

in one step (to `False()` in this case), while the `bottomup` strategy defined above would first evaluate the big expression.

### 5.3.3.  Staged Transformations

Cascading transformations apply a number of rules one after another to an entire tree. But in some cases this is not appropriate. For instance, two transformations may be inverses of one another, so that repeatedly applying one and then the other would lead to non-termination. To remedy this difficulty, Stratego supports the idiom of _staged transformation_.

In staged computation, transformations are not applied to a subject term all at once, but rather in stages. In each stage, only rules from some particular subset of the entire set of available rules are applied. In the TAMPR program transformation system this idiom is called _sequence of normal forms_, since a program tree is transformed in a sequence of steps, each of which performs a normalization with respect to a specified set of rules. In Stratego this idiom can be expressed directly according to the following scheme:

    strategies

      simplify =
          innermost(A1 <+ ... <+ Ak)
        ; innermost(B1 <+ ... <+ Bl)
        ; ...
        ; innermost(C1 <+ ... <+ Cm)

### 5.3.4. Local Transformations

In conventional program optimization, transformations are applied throughout a program. In optimizing imperative programs, for example, complex transformations are applied to entire programs. In GHC-style compilation-by-transformation, small transformation steps are applied throughout programs. Another style of transformation is a mixture of these ideas. Instead of applying a complex transformation algorithm to a program we use staged, cascading transformations to accumulate small transformation steps for large effect. However, instead of applying transformations throughout the subject program, we often wish to apply them locally, i.e., only to selected parts of the subject program. This allows us to use transformations rules that would not be beneficial if applied everywhere.

One example of a strategy which achieves such a transformation is

    strategies

      transformation =
        alltd(
          trigger-transformation
          ; innermost(A1 <+ ... <+ An)
        )

The strategy `alltd(s)` descends into a term until a subterm is encountered for which the transformation `s` succeeds. In this case the strategy `trigger-transformation` recognizes a program fragment that should be transformed. Thus, cascading transformations are applied locally to terms for which the transformation is triggered. Of course more sophisticated strategies can be used for finding application locations, as well as for applying the rules locally. Nevertheless, the key observation underlying this idiom remains: Because the transformations to be applied are local, special knowledge about the subject program at the point of application can be used. This allows the application of rules that would not be otherwise applicable.

[1]: 04-term-rewriting.md "Term Rewriting"
