```eval_rst
.. highlight:: str
```

# 9. Traversal Strategies

In [Chapter 5][1] we saw a number of idioms of strategic rewriting, which all involved _tree traversal_. In the previous chapters we saw how strategies can be used to control transformations and how rules can be broken down into the primitive actions match, build and scope. The missing ingredient are combinators for defining traversals.

There are many ways to traverse a tree. For example, a bottom-up traversal, visits the subterms of a node before it visits the node itself, while a top-down traversal visits nodes before it visits children. One-pass traversals traverse the tree one time, while fixed-point traversals, such as `innermost`, repeatedly traverse a term until a normal form is reached.

It is not desirable to provide built-in implementations for all traversals needed in transformations, since such a collection would necessarily be incomplete. Rather we would like to define traversals in terms of the primitive ingredients of traversal. For example, a top-down, one-pass traversal strategy will first visit a node, and then descend to the children of a node in order to _recursively_ traverse all subterms. Similarly, the bottom-up, fixed-point traversal strategy _innermost_, will first descend to the children of a node in order to _recursively_ traverse all subterms, then visit the node itself, and possibly recursively reapply the strategy.

Traversal in Stratego is based on the observation that a full term traversal is a recursive closure of a one-step descent, that is, an operation that applies a strategy to one or more direct subterms of the subject term. By separating this one-step descent operator from recursion, and making it a first-class operation, many different traversals can be defined.

In this chapter we explore the ways in which Stratego supports the definition of _traversal strategies_. We start with explicitly programmed traversals using recursive traversal rules. Next, _congruences operators_ provide a more concise notation for such data-type specific traversal rules. Finally, _generic traversal operators_ support data type independent definitions of traversals, which can be reused for any data type. Given these basic mechanisms, we conclude with an an exploration of idioms for traversal and standard traversal strategies in the Stratego Library.

In [Chapter 8][2] we saw the following definition of the `map` strategy, which applies a strategy to each element of a list:

    map(s) : [] -> []
    map(s) : [x | xs] -> [<s> x | <map(s)> xs]

The definition uses explicit recursive calls to the strategy in the right-hand side of the second rule. What `map` does is to _traverse_ the list in order to apply the argument strategy to all elements. We can use the same technique to other term structures as well.

We will explore the definition of traversals using the propositional formulae from [Chapter 5][1], where we introduced the following rewrite rules:

    module prop-rules
    imports libstrategolib prop
    rules
      DefI : Impl(x, y)       -> Or(Not(x), y)
      DefE : Eq(x, y)         -> And(Impl(x, y), Impl(y, x))
      DN   : Not(Not(x))      -> x
      DMA  : Not(And(x, y))   -> Or(Not(x), Not(y))
      DMO  : Not(Or(x, y))    -> And(Not(x), Not(y))
      DAOL : And(Or(x, y), z) -> Or(And(x, z), And(y, z))
      DAOR : And(z, Or(x, y)) -> Or(And(z, x), And(z, y))
      DOAL : Or(And(x, y), z) -> And(Or(x, z), Or(y, z))
      DOAR : Or(z, And(x, y)) -> And(Or(z, x), Or(z, y))

In [Chapter 5][1] we saw how a functional style of rewriting could be encoded using extra constructors. In Stratego we can achieve a similar approach by using rule names, instead of extra constructors. Thus, one way to achieve normalization to disjunctive normal form, is the use of an explicitly programmed traversal, implemented using recursive rules, similarly to the `map` example above:

    module prop-dnf4
    imports libstrategolib prop-rules
    strategies
      main = io-wrap(dnf)
    rules
      dnf : True()     ->          True()
      dnf : False()    ->          False()
      dnf : Atom(x)    ->          Atom(x)
      dnf : Not(x)     -> <dnfred> Not (<dnf>x)
      dnf : And(x, y)  -> <dnfred> And (<dnf>x, <dnf>y)
      dnf : Or(x, y)   ->          Or  (<dnf>x, <dnf>y)
      dnf : Impl(x, y) -> <dnfred> Impl(<dnf>x, <dnf>y)
      dnf : Eq(x, y)   -> <dnfred> Eq  (<dnf>x, <dnf>y)
    strategies
      dnfred = try(DN <+ (DefI <+ DefE <+ DMA <+ DMO <+ DAOL <+ DAOR); dnf)

The `dnf` rules recursively apply themselves to the direct subterms and then apply `dnfred` to actually apply the rewrite rules.

We can reduce this program by abstracting over the base cases. Since there is no traversal into `True`, `False`, and `Atom`s, these rules can be be left out.

    module prop-dnf5
    imports libstrategolib prop-rules
    strategies
      main = io-wrap(dnf)
    rules
      dnft : Not(x)     -> <dnfred> Not (<dnf>x)
      dnft : And(x, y)  -> <dnfred> And (<dnf>x, <dnf>y)
      dnft : Or(x, y)   ->          Or  (<dnf>x, <dnf>y)
      dnft : Impl(x, y) -> <dnfred> Impl(<dnf>x, <dnf>y)
      dnft : Eq(x, y)   -> <dnfred> Eq  (<dnf>x, <dnf>y)
    strategies
      dnf    = try(dnft)
      dnfred = try(DN <+ (DefI <+ DefE <+ DMA <+ DMO <+ DAOL <+ DAOR); dnf)

The `dnf` strategy is now defined in terms of the `dnft` rules, which implement traversal over the constructors. By using `try(dnft)`, terms for which no traversal rule has been specified are not transformed.

We can further simplify the definition by observing that the application of `dnfred` does not necessarily have to take place in the right-hand side of the traversal rules.

    module prop-dnf6
    imports libstrategolib prop-rules
    strategies
      main = io-wrap(dnf)
    rules
      dnft : Not(x)     -> Not (<dnf>x)
      dnft : And(x, y)  -> And (<dnf>x, <dnf>y)
      dnft : Or(x, y)   -> Or  (<dnf>x, <dnf>y)
      dnft : Impl(x, y) -> Impl(<dnf>x, <dnf>y)
      dnft : Eq(x, y)   -> Eq  (<dnf>x, <dnf>y)
    strategies
      dnf    = try(dnft); dnfred
      dnfred = try(DN <+ (DefI <+ DefE <+ DMA <+ DMO <+ DAOL <+ DAOR); dnf)

In this program `dnf` first calls `dnft` to transform the subterms of the subject term, and then calls `dnfred` to apply the transformation rules (and possibly a recursive invocation of `dnf`).

The program above has two problems. First, the traversal behavior is mostly uniform, so we would like to specify that more concisely. We will address that concern below. Second, the traversal is not reusable, for example, to define a conjunctive normal form transformation. This last concern can be addressed by factoring out the recursive call to `dnf` and making it a parameter of the traversal rules.

    module prop-dnf7
    imports libstrategolib prop-rules
    strategies
      main = io-wrap(dnf)
    rules
      proptr(s) : Not(x)     -> Not (<s>x)
      proptr(s) : And(x, y)  -> And (<s>x, <s>y)
      proptr(s) : Or(x, y)   -> Or  (<s>x, <s>y)
      proptr(s) : Impl(x, y) -> Impl(<s>x, <s>y)
      proptr(s) : Eq(x, y)   -> Eq  (<s>x, <s>y)
    strategies
      dnf    = try(proptr(dnf)); dnfred
      dnfred = try(DN <+ (DefI <+ DefE <+ DMA <+ DMO <+ DAOL <+ DAOR); dnf)
      cnf    = try(proptr(cnf)); cnfred
      cnfred = try(DN <+ (DefI <+ DefE <+ DMA <+ DMO <+ DOAL <+ DOAR); cnf)

Now the traversal rules are reusable and used in two different transformations, by instantiation with a call to the particular strategy in which they are used (`dnf` or `cnf`).

But we can do better, and also make the _composition_ of this strategy reusable.

    module prop-dnf8
    imports libstrategolib prop-rules
    strategies
      main = io-wrap(dnf)
    rules
      proptr(s) : Not(x)     -> Not (<s>x)
      proptr(s) : And(x, y)  -> And (<s>x, <s>y)
      proptr(s) : Or(x, y)   -> Or  (<s>x, <s>y)
      proptr(s) : Impl(x, y) -> Impl(<s>x, <s>y)
      proptr(s) : Eq(x, y)   -> Eq  (<s>x, <s>y)
    strategies
      propbu(s) = try(proptr(propbu(s))); s
    strategies
      dnf    = propbu(dnfred)
      dnfred = try(DN <+ (DefI <+ DefE <+ DMA <+ DMO <+ DAOL <+ DAOR); dnf)
      cnf    = propbu(cnfred)
      cnfred = try(DN <+ (DefI <+ DefE <+ DMA <+ DMO <+ DOAL <+ DOAR); cnf)

That is, the `propbu(s)` strategy defines a complete bottom-up traversal over proposition terms, applying the strategy `s` to a term after transforming its subterms. The strategy is completely independent of the `dnf` and `cnf` transformations, which instantiate the strategy using the `dnfred` and `cnfred` strategies.

Come to think of it, `dnfred` and `cnfred` are somewhat useless now and can be inlined directly in the instantiation of the `propbu(s)` strategy:

    module prop-dnf9
    imports libstrategolib prop-rules
    strategies
      main = io-wrap(dnf)
    rules
      proptr(s) : Not(x)     -> Not (<s>x)
      proptr(s) : And(x, y)  -> And (<s>x, <s>y)
      proptr(s) : Or(x, y)   -> Or  (<s>x, <s>y)
      proptr(s) : Impl(x, y) -> Impl(<s>x, <s>y)
      proptr(s) : Eq(x, y)   -> Eq  (<s>x, <s>y)
    strategies
      propbu(s) = try(proptr(propbu(s))); s
    strategies
      dnf = propbu(try(DN <+ (DefI <+ DefE <+ DMA <+ DMO <+ DAOL <+ DAOR); dnf))
      cnf = propbu(try(DN <+ (DefI <+ DefE <+ DMA <+ DMO <+ DOAL <+ DOAR); cnf))

Now we have defined a _transformation independent_ traversal strategy that is _specific_ for proposition terms.

Next we consider cheaper ways for defining the traversal rules, and then ways to get completely rid of them.

## 9.1. Congruence Operators

The definition of the traversal rules above frequently occurs in the definition of transformation strategies. Congruence operators provide a convenient abbreviation of precisely this operation. A congruence operator applies a strategy to each direct subterm of a specific constructor. For each n-ary constructor c declared in a signature, there is a corresponding _congruence operator_ `c(s1 , ..., sn)`, which applies to terms of the form `c(t1 , ..., tn)` by applying the argument strategies to the corresponding argument terms. A congruence fails if the application of one the argument strategies fails or if constructor of the operator and that of the term do not match.

**Example.** For example, consider the following signature of expressions:

    module expressions
    signature
      sorts Exp
      constructors
        Int   : String -> Exp
        Var   : String -> Exp
        Plus  : Exp * Exp -> Exp
        Times : Exp * Exp -> Exp

The following Stratego Shell session applies the congruence operators `Plus` and `Times` to a term:

    stratego> import expressions
    stratego> !Plus(Int("14"),Int("3"))
    Plus(Int("14"),Int("3"))
    stratego> Plus(!Var("a"), id)
    Plus(Var("a"),Int("3"))
    stratego> Times(id, !Int("42"))
    command failed

The first application shows how a congruence transforms a specific subterm, that is the strategy applied can be different for each subterm. The second application shows that a congruence only succeeds for terms constructed with the same constructor.

The `import` at the start of the session is necessary to declare the constructors used; the definitions of congruences are derived from constructor declarations. Forgetting this import would lead to a complaint about an undeclared operator:

    stratego> !Plus(Int("14"),Int("3"))
    Plus(Int("14"),Int("3"))
    stratego> Plus(!Var("a"), id)
    operator Plus/(2,0) not defined
    command failed

**Defining Traversals with Congruences.** Now we return to our `dnf`/`cnf` example, to see how congruence operators can help in their implementation. Since congruence operators basically define a one-step traversal for a specific constructor, they capture the traversal rules defined above. That is, a traversal rule such as

    proptr(s) : And(x, y) -> And(<s>x, <s>y)

can be written by the congruence `And(s,s)`. Applying this to the `prop-dnf` program we can replace the traversal rules by congruences as follows:

    module prop-dnf10
    imports libstrategolib prop-rules
    strategies
      main = io-wrap(dnf)
    strategies
      proptr(s) = Not(s) <+ And(s, s) <+ Or(s, s) <+ Impl(s, s) <+ Eq(s, s)
      propbu(s) = try(proptr(propbu(s))); s
    strategies
      dnf = propbu(try(DN <+ (DefI <+ DefE <+ DMA <+ DMO <+ DAOL <+ DAOR); dnf))
      cnf = propbu(try(DN <+ (DefI <+ DefE <+ DMA <+ DMO <+ DOAL <+ DOAR); cnf))

Observe how the five traversal rules have been reduced to five congruences which fit on a single line.

**Traversing Tuples and Lists.** Congruences can also be applied to tuples, `(s1,s2,...,sn)`, and lists, [`s1,s2,...,sn]`. A special list congruence is `[]` which 'visits' the empty list. As an example, consider again the definition of `map(s)` using recursive traversal rules:

    map(s) : [] -> []
    map(s) : [x | xs] -> [<s> x | <map(s)> xs]

Using list congruences we can define this strategy as:

    map(s) = [] <+ [s | map(s)]

The `[]` congruence matches an empty list. The [`s | map(s)]` congruence matches a non-empty list, and applies `s` to the head of the list and `map(s)` to the tail. Thus, `map(s)` applies `s` to each element of a list:

    stratego> import libstratego-lib
    stratego> ![1,2,3]
    [1,2,3]
    stratego> map(inc)
    [2,3,4]

Note that `map(s)` only succeeds if `s` succeeds for each element of the list. The `fetch` and `filter` strategies are variations on `map` that use the failure of `s` to list elements.

    fetch(s) = [s | id] <+ [id | fetch(s)]

The `fetch` strategy traverses a list _until_ it finds a element for which `s` succeeds and then stops. That element is the only one that is transformed.

    filter(s) = [] + ([s | filter(s)] <+ ?[ |<id>]; filter(s))

The `filter` strategy applies `s` to each element of a list, but only keeps the elements for which it succeeds.

    stratego> import libstratego-lib
    stratego> even = where(<eq>(<mod>(<id>,2),0))
    stratego> ![1,2,3,4,5,6,7,8]
    [1,2,3,4,5,6,7,8]
    stratego> filter(even)
    [2,4,6,8]

**Format Checking.** Another application of congruences is in the definition of format checkers. A format checker describes a subset of a term language using a recursive pattern. This can be used to verify input or output of a transformation, and for documentation purposes. Format checkers defined with congruences can check subsets of signatures or regular tree grammars. For example, the subset of terms of a signature in a some normal form.

As an example, consider checking the output of the `dnf` and `cnf` transformations.

    conj(s) = And(conj(s), conj(s)) <+ s
    disj(s) = Or (disj(s), disj(s)) <+ s

    // Conjunctive normal form
    conj-nf = conj(disj(Not(Atom(id)) <+ Atom(id)))

    // Disjunctive normal form
    disj-nf = disj(conj(Not(Atom(id)) <+ Atom(id)))

The strategies `conj(s)` and `disj(s)` check that the subject term is a conjunct or a disjunct, respectively, with terms satisfying `s` at the leaves. The strategies `conj-nf` and `disj-nf` check that the subject term is in conjunctive or disjunctive normal form, respectively.

Using congruence operators we constructed a generic, i.e. transformation independent, bottom-up traversal for proposition terms. The same can be done for other data types. However, since the sets of constructors of abstract syntax trees of typical programming languages can be quite large, this may still amount to quite a bit of work that is not reusable _across_ data types; even though a strategy such as _bottom-up traversal_, is basically data-type independent. Thus, Stratego provides generic traversal by means of several _generic one-step descent operators_. The operator `all`, applies a strategy to all direct subterms. The operator `one`, applies a strategy to one direct subterm, and the operator `some`, applies a strategy to as many direct subterms as possible, and at least one.


### 9.1.1. Visiting All Subterms

The `all(s)` strategy transforms a constructor application by applying the parameter strategy `s` to each direct subterm. An application of `all(s)` fails if the application to one of the subterms fails. The following example shows how `all` (1) applies to any term, and (2) applies its argument strategy uniformly to all direct subterms. That is, it is not possible to do something special for a particular subterm (that's what congruences are for).

    stratego> !Plus(Int("14"),Int("3"))
    Plus(Int("14"),Int("3"))
    stratego> all(!Var("a"))
    Plus(Var("a"),Var("a"))
    stratego> !Times(Var("b"),Int("3"))
    Times(Var("b"),Int("3"))
    stratego> all(!Var("z"))
    Times(Var("z"),Var("z"))

The `all(s)` operator is really the ultimate replacement for the traversal rules that we saw above. Instead of specifying a rule or congruence for each constructor, the single application of the `all` operator takes care of traversing all constructors. Thus, we can replace the `propbu` strategy by a completely generic definition of bottom-up traversal. Consider again the last definition of `propbu`:

    proptr(s) = Not(s) <+ And(s, s) <+ Or(s, s) <+ Impl(s, s) <+ Eq(s, s)
    propbu(s) = proptr(propbu(s)); s

The role of `proptr(s)` in this definition can be replaced by `all(s)`, since that achieves exactly the same, namely applying `s` to the direct subterms of constructors:

    propbu(s) = all(propbu(s)); s

However, the strategy now is completely generic, i.e. independent of the particular structure it is applied to. In the Stratego Library this strategy is called `bottomup(s)`, and defined as follows:

    bottomup(s) = all(bottomup(s)); s

It first recursively transforms the subterms of the subject term and then applies `s` to the result. Using this definition, the normalization of propositions now reduces to the following module, which is only concerned with the selection and composition of rewrite rules:

    module prop-dnf11
    imports libstrategolib prop-rules
    strategies
      main = io-wrap(dnf)
    strategies
      dnf = bottomup(try(DN <+ (DefI <+ DefE <+ DMA <+ DMO <+ DAOL <+ DAOR); dnf))
      cnf = bottomup(try(DN <+ (DefI <+ DefE <+ DMA <+ DMO <+ DOAL <+ DOAR); cnf))

In fact, these definitions still contain a reusable pattern. With a little squinting we see that the definitions match the following pattern:

    dnf = bottomup(try(dnf-rules; dnf))
    cnf = bottomup(try(cnf-rules; cnf))

In which we can recognize the definition of _innermost_ reduction, which the Stratego Library defines as:

    innermost(s) = bottomup(try(s; innermost(s)))

The `innermost` strategy performs a bottom-up traversal of a term. After transforming the subterms of a term it tries to apply the transformation `s`. If successful the result is recursively transformed with an application of `innermost`. This brings us to the final form for the proposition normalizations:

    module prop-dnf12
    imports libstrategolib prop-rules
    strategies
      main = io-wrap(dnf)
    strategies
      dnf = innermost(DN <+ DefI <+ DefE <+ DMA <+ DMO <+ DAOL <+ DAOR)
      cnf = innermost(DN <+ DefI <+ DefE <+ DMA <+ DMO <+ DOAL <+ DOAR)

Different transformations can be achieved by using a selection of rules and a strategy, which is generic, yet defined in Stratego itself using strategy combinators.


### 9.1.2. Visiting One Subterm

The `one(s)` strategy transforms a constructor application by applying the parameter strategy `s` to exactly one direct subterm. An application of `one(s)` fails if the application to all of the subterms fails. The following Stratego Shell session illustrates the behavior of the combinator:

    stratego> !Plus(Int("14"),Int("3"))
    Plus(Int("14"),Int("3"))
    stratego> one(!Var("a"))
    Plus(Var("a"),Int("3"))
    stratego> one(\ Int(x) -> Int(<addS>(x,"1")) \ )
    Plus(Var("a"),Int("4"))
    stratego> one(?Plus(_,_))
    command failed

A frequently used application of `one` is the `oncetd(s)` traversal, which performs a left to right depth first search/transformation that stops as soon as `s` has been successfully applied.

    oncetd(s) = s <+ one(oncetd(s))

Thus, `s` is first applied to the root of the subject term. If that fails, its direct subterms are searched one by one (from left to right), with a recursive call to `oncetd(s)`.

An application of `oncetd` is the `contains(|t)` strategy, which checks whether the subject term contains a subterm that is equal to `t`.

    contains(|t) = oncetd(?t)

Through the depth first search of `oncetd`, either an occurrence of `t` is found, or all subterms are verified to be unequal to `t`.

Here are some other one-pass traversals using the `one` combinator:

    oncebu(s)  = one(oncebu(s)) <+ s
    spinetd(s) = s; try(one(spinetd(s)))
    spinebu(s) = try(one(spinebu(s))); s

Exercise: figure out what these strategies do.

Here are some fixe-point traversals, i.e., traversals that apply their argument transformation exhaustively to the subject term.

    reduce(s)     = repeat(rec x(one(x) + s))
    outermost(s)  = repeat(oncetd(s))
    innermostI(s) = repeat(oncebu(s))

The difference is the subterm selection strategy. Exercise: create rewrite rules and terms that demonstrate the differences between these strategies.


### 9.1.3. Visiting Some Subterms

The `some(s)` strategy transforms a constructor application by applying the parameter strategy `s` to as many direct subterms as possible and at least one. An application of `some(s)` fails if the application to all of the subterms fails.

Some one-pass traversals based on `some`:

    sometd(s) = s <+ some(sometd(s))
    somebu(s) = some(somebu(s)) <+ s

A fixed-point traversal with `some`:

    reduce-par(s) = repeat(rec x(some(x) + s))


## 9.2. Idioms and Library Strategies for Traversal

Above we have seen the basic mechanisms for defining traversals in Stratego: custom traversal rules, data-type specific congruence operators, and generic traversal operators. Term traversals can be categorized into classes according to how much of the term they traverse and to which parts of the term they modify. We will consider a number of idioms and standard strategies from the Stratego Library that are useful in the definition of traversals.

One class of traversal strategies performs a _full traversal_, that is visits and transforms every subterm of the subject term. We already saw the `bottomup` strategy defined as

    bottomup(s) = all(bottomup(s)); s

It first visits the subterms of the subject term, recursively transforming _its_ subterms, and then applies the transformation `s` to the result.

A related strategy is `topdown`, which is defined as

    topdown(s) = s; all(topdown(s))

It _first_ transforms the subject therm and _then_ visits the subterms of the result.

A combination of `topdown` and `bottomup` is `downup`, defined as

    downup(s) = s; all(downup(s)); s

It applies `s` on the way down the tree, and again on the way up. A variation is `downup(2,0)`

    downup(s1, s2) = s1; all(downup(s1, s2)); s2

which applies one strategy on the way down and another on the way up.

Since the parameter strategy is applied at every subterm, these traversals only succeed if it succeeds everywhere. Therefore, these traversals are typically applied in combination with `try` or `repeat`.

    topdown(try(R1 <+ R2 <+ ...))

This has the effect that the rules are tried at each subterm. If none of the rules apply the term is left as it was and traversal continues with its subterms.

**Choosing a Strategy.** The strategy to be used for a particular transformation depends on the rules and the goal to be achieved.

For example, a constant folding transformation for proposition formulae can be defined as a bottom-up traversal that tries to apply one of the truth-rules `T` at each subterm:

    T : And(True(), x) -> x
    T : And(x, True()) -> x
    T : And(False(), x) -> False()
    T : And(x, False()) -> False()
    T : Or(True(), x) -> True()
    T : Or(x, True()) -> True()
    T : Or(False(), x) -> x
    T : Or(x, False()) -> x
    T : Not(False()) -> True()
    T : Not(True()) -> False()

    eval = bottomup(try(T))

Bottomup is the strategy of choice here because it evaluates subterms before attempting to rewrite a term. An evaluation strategy using `topdown`

    eval2 = topdown(try(T)) // bad strategy

does not work as well, since it attempts to rewrite terms before their subterms have been reduced, thus missing rewriting opportunities. The following Stratego Shell session illustrates this:

    stratego> !And(True(), Not(Or(False(), True())))
    And(True,Not(Or(False,True)))
    stratego> eval
    False
    stratego> !And(True(), Not(Or(False(), True())))
    And(True,Not(Or(False,True)))
    stratego> eval2
    Not(True)

Exercise: find other terms that show the difference between these strategies.

On the other hand, a desugaring transformation for propositions, which defines implication and equivalence in terms of other connectives is best defined as a `topdown` traversal which tries to apply one of the rules `DefI` or `DefE` at every subterm.

    DefI : Impl(x, y) -> Or(Not(x), y)
    DefE : Eq(x, y) -> And(Impl(x, y), Impl(y, x))

    desugar = topdown(try(DefI <+ DefE))

Since `DefE` rewrites `Eq` terms to terms involving `Impl`, a strategy with `bottomup` does not work.

    desugar2 = bottomup(try(DefI <+ DefE))   // bad strategy

Since the subterms of a node are traversed _before_ the node itself is visited, this transformation misses the desugaring of the implications (`Impl`) originating from the application of the `DefE` rule. The following Shell session illustrates this:

    stratego> !Eq(Atom("p"), Atom("q"))
    Eq(Atom("p"),Atom("q"))
    stratego> desugar
    And(Or(Not(Atom("p")),Atom("q")),Or(Not(Atom("q")),Atom("p")))
    stratego> !Eq(Atom("p"), Atom("q"))
    Eq(Atom("p"),Atom("q"))
    stratego> desugar2
    And(Impl(Atom("p"),Atom("q")),Impl(Atom("q"),Atom("p")))

**Repeated Application.** In case one rule produces a term to which another desugaring rule can be applied, the desugaring strategy should repeat the application of rules to each subterm. Consider the following rules and strategy for desugaring propositional formulae to implicative normal form (using only implication and `False`).

    DefT  : True() -> Impl(False(), False())
    DefN  : Not(x) -> Impl(x, False())
    DefA2 : And(x, y) -> Not(Impl(x, Not(y)))
    DefO1 : Or(x, y) -> Impl(Not(x), y)
    DefE  : Eq(x, y) -> And(Impl(x, y), Impl(y, x))

    impl-nf = topdown(repeat(DefT <+ DefN <+ DefA2 <+ DefO1 <+ DefE))

Application of the rules with `try` instead of `repeat`

    impl-nf2 = topdown(try(DefT <+ DefN <+ DefA2 <+ DefO1 <+ DefE))  // bad strategy

is not sufficient, as shown by the following Shell session:

    stratego> !And(Atom("p"),Atom("q"))
    And(Atom("p"),Atom("q"))
    stratego> impl-nf
    Impl(Impl(Atom("p"),Impl(Atom("q"),False)),False)
    stratego> !And(Atom("p"),Atom("q"))
    And(Atom("p"),Atom("q"))
    stratego> impl-nf2
    Not(Impl(Atom("p"),Impl(Atom("q"),False)))

Note that the `Not` is not desugared with `impl-nf2`.

**Paramorphism.** A variation on bottomup is a traversal that also provides the original term as well as the term in which the direct subterms have been transformed. (Also known as a paramorphism?)

    bottomup-para(s) = <s>(<id>, <all(bottomup-para(s))>)

This is most useful in a bottom-up traversal; the original term is always available in a top-down traversal.

Exercise: give an example application of this strategy

### 9.2.1. Cascading Transformations

Cascading transformations are transformations upon transformations. While the full traversals discussed above walk over the tree once, cascading transformations apply multiple _waves_ of transformations to the nodes in the tree. The prototypical example is the `innermost` strategy, which exhaustively applies a transformation, typically a set of rules, to a tree.

    simplify =
      innermost(R1 <+ ... <+ Rn)

The basis of `innermost` is a `bottomup` traversal that tries to apply the transformation at each node after visiting its subterms.

    innermost(s) = bottomup(try(s; innermost(s)))

If the transformation `s` succeeds, the result term is transformed again with a recursive call to `innermost`.

Application of `innermost` exhaustively applies _one_ set of rules to a tree. Using sequential composition we can apply several _stages_ of reductions. A special case of such a _staged transformation_, is known as _sequence of normal forms_ (in the TAMPR system):

    simplify =
      innermost(A1 <+ ... <+ Ak)
      ; innermost(B1 <+ ... <+ Bl)
      ; ...
      ; innermost(C1 <+ ... <+ Cm)

At each stage the term is reduced with respect to a different set of rules.

Of course it is possible to mix different types of transformations in such a stage pipeline, for example.

    simplify =
      topdown(try(A1 <+ ... <+ Ak))
      ; innermost(B1 <+ ... <+ Bl)
      ; ...
      ; bottomup(repeat(C1 <+ ... <+ Cm))

At each stage a different strategy and different set of rules can be used. (Of course one may use the same strategy several times, and some of the rule sets may overlap.)

### 9.2.2. Mixing Generic and Specific Traversals

While completely generic strategies such as `bottomup` and `innermost` are often useful, there are also situations where a mixture of generic and data-type specific traversal is necessary. Fortunately, Stratego allows you to mix generic traversal operators, congruences, your own traversal and regular rules, any way you see fit.

A typical pattern for such strategies first tries a number of special cases that deal with traversal themselves. If none of the special cases apply, a generic traversal is used, followed by application of some rules applicable in the general case.

    transformation =
      special-case1
      <+ special-case2
      <+ special-case3
      <+ all(transformation); reduce

    reduce = ...

**Constant Propagation.** A typical example is the following constant propagation strategy. It uses the exceptions to the basic generic traversal to traverse the tree in the order of the control-flow of the program that is represented by the term. This program makes use of _dynamic rewrite rules_, which are used to propagate context-sensitive information through a program. In this case, the context-sensitive information concerns the constant values of some variables in the program, which should be propagated to the uses of those variables. Dynamic rules will be explained in [Chapter 12][3]; for now we are mainly concerned with the traversal strategy.

    module propconst
    imports
      libstratego-lib

    signature
      constructors
        Var    : String -> Exp
        Plus   : Exp * Exp -> Exp
        Assign : String * Exp -> Stat
        If     : Exp * Stat * Stat -> Stat
        While  : Exp * Stat -> Stat

    strategies

      propconst = ❶
        PropConst ❷
        <+ propconst-assign
        <+ propconst-if
        <+ propconst-while
        <+ all(propconst); try(EvalBinOp)

      EvalBinOp : ❸
        Plus(Int(i), Int(j)) -> Int(k) where <addS>(i,j) => k

      EvalIf :
        If(Int("0"), s1, s2) -> s2

      EvalIf :
        If(Int(i), s1, s2) -> s1 where <not(eq)>(i, "0")

      propconst-assign = ❹
        Assign(?x, propconst => e)
        ; if <is-value> e then
            rules( PropConst : Var(x) -> e )
          else
            rules( PropConst :- Var(x) )
          end

      propconst-if = ❺
        If(propconst, id, id)
        ; (EvalIf; propconst
          <+ (If(id, propconst, id) /PropConst\ If(id,id,propconst)))

      propconst-while = ❻
        While(id,id)
        ; (/PropConst\* While(propconst, propconst))

      is-value = Int(id)

The main strategy of the constant propagation transformation ❶, follows the pattern described above; a number of special case alternatives followed by a generic traversal alternative. The special cases are defined in their own definitions. Generic traversal is followed by the constant folding rule `EvalBinOp` ❸.

The first special case is an application of the dynamic rule `PropConst`, which replaces a constant valued variable by its constant value ❷. This rule is defined by the second special case strategy, `propconst-assign` ❹. It first traverses the right-hand side of an assignment with an `Assign` congruence operator, and a recursive call to `propconst`. Then, if the expression evaluated to a constant value, a new `PropConst` rule is defined. Otherwise, any old instance of `PropConst` for the left-hand side variable is undefined.

The third special case for `If` uses congruence operators to order the application of `propconst` to its subterms ❺. The first congruence applies `propconst` to the condition expression. Then an application of the rule `EvalIf` attempts to eliminate one of the branches of the statement, in case the condition evaluated to a constant value. If that is not possible the branches are visited by two more congruence operator applications joined by a dynamic rule intersection operator, which distributes the constant propagation rules over the branches and merges the rules afterwards, keeping only the consistent ones. Something similar happens in the case of `While` statements ❻. For details concerning dynamic rules, see [Chapter 12][3].

To see what `propconst` achieves, consider the following abstract syntax tree (say in file `foo.prg`).

    Block([
      Assign("x", Int("1")),
      Assign("y", Int("42")),
      Assign("z", Plus(Var("x"), Var("y"))),
      If(Plux(Var("a"), Var("z")),
        Assign("b", Plus(Var("x"), Int("1"))),
        Block([
          Assign("z", Int("17")),
          Assign("b", Int("2"))
        ])),
      Assign("c", Plus(Var("b"), Plus(Var("z"), Var("y"))))
    ])

We import the module in the Stratego Shell, read the abstract syntax tree from file, and apply the `propconst` transformation to it:

    stratego> import libstrategolib
    stratego> import propconst
    stratego> <ReadFromFile> "foo.prg"
    ...
    stratego> propconst
    Block([Assign("x",Int("1")),Assign("y",Int("42")),Assign("z",Int("43")),
    If(Plux(Var("a"),Int("43")),Assign("b",Int("2")),Block([Assign("z",
    Int("17")),Assign("b",Int("2"))])),Assign("c",Plus(Int("2"),Plus(
    Var("z"),Int("42"))))])

Since the Stratego Shell does not (yet) pretty-print terms, the result is rather unreadable. We can remedy this by writing the result of the transformation to a file, and pretty-printing it on the regular command-line with ``pp-aterm``.

    stratego> <ReadFromFile> "foo.prg"
    ...
    stratego> propconst; <WriteToTextFile> ("foo-pc.prg", <id>)
    ...
    stratego> :quit
    ...
    $ pp-aterm -i foo-pc.prg
    Block(
      [ Assign("x", Int("1"))
      , Assign("y", Int("42"))
      , Assign("z", Int("43"))
      , If(
          Plux(Var("a"), Int("43"))
        , Assign("b", Int("2"))
        , Block(
            [Assign("z", Int("17")), Assign("b", Int("2"))]
          )
        )
      , Assign(
          "c"
        , Plus(Int("2"), Plus(Var("z"), Int("42")))
        )
      ]
    )

Compare the result to the original program and try to figure out what has happened and why that is correct. (Assuming the _usual_ semantics for this type of imperative language.)

**Generic Strategies with Exceptional Cases.** Patterns for mixing specific and generic traversal can be captured in parameterized strategies such as the following. They are parameterized with the usual transformation parameter `s` and with a higher-order strategy operator `stop`, which implements the special cases.

    topdownS(s, stop: (a -> a) * b -> b) =
      rec x(s; (stop(x) <+ all(x)))

    bottomupS(s, stop: (a -> a) * b -> b) =
      rec x((stop(x) <+ all(x)); s)

    downupS(s, stop: (a -> a) * b -> b) =
      rec x(s; (stop(x) <+ all(x)); s)

    downupS(s1, s2, stop: (a -> a) * b -> b) =
      rec x(s1; (stop(x) <+ all(x)); s2)

While normal strategies (parameters) are functions from terms to terms, the `stop` parameter is a function from strategies to strategies. Such exceptions to the default have to be declared explicitly using a type annotation. Note that the `bottomupS` strategy is slightly different from the pattern of the `propconst` strategy; instead of applying `s` _only_ after the generic traversal case, it is here applied in all cases.

However, the added value of these strategies is not very high. The payoff in the use of generic strategies is provided by the basic generic traversal operators, which provide generic behavior for all constructors. The `stop` callback can make it harder to understand the control-flow structure of a strategy; use with care and don't overdo it.

### 9.2.3. Separate rules and strategies

While it is possible to construct your own strategies by mixing traversal elements and rules, in general, it is a good idea to try to get a clean separation between pure rewrite rules and a (simple) strategy that applies them.

### 9.2.4. Partial Traversals

The full traversals introduced above mostly visit all nodes in the tree. Now we consider traversals that visit only some of the nodes of a tree.

The `oncet` and `oncebu` strategies apply the argument strategy `s` at one position in the tree. That is, application is tried at every node along the traversal until it succeeds.

    oncetd(s) = s <+ one(oncetd(s))
    oncebu(s) = one(oncebu(s)) <+ s

The `sometd` and `somebu` strategies are variations on `oncet` and `oncebu` that apply `s` at least once at some positions, but possibly many times. As soon as one is found, searching is stopped, i.e., in the top-down case searching in subtrees is stopped, in bottom-up case, searching in upper spine is stopped.

    sometd(s) = s <+ some(sometd(s))
    somebu(s) = some(somebu(s)) <+ s

Similar strategies that find as many applications as possible, but at least one, can be built using `some`:

    manybu(s) = rec x(some(x); try(s) <+ s)
    manytd(s) = rec x(s; all(try(x)) <+ some(x))

&nbsp;

    somedownup(s) = rec x(s; all(x); try(s) <+ some(x); try(s))

The `alltd(s)` strategy stops as soon as it has found a subterm to which `s` can be succesfully applied.

    alltd(s) = s <+ all(alltd(s))

If `s` does not succeed, the strategy is applied recursively at all direct subterms. This means that `s` is applied along a frontier of the subject term. This strategy is typically used in substitution operations in which subterms are replaced by other terms. For example, the strategy `alltd(?Var(x); !e)` replaces all occurrences of `Var(x)` by `e`. Note that `alltd(try(s))` is not a useful strategy. Since `try(s)` succeeds at the root of the term, no traversal is done.

A typical application of `alltd` is the definition of local transformations, that only apply to some specific subterm.

    transformation =
      alltd(
        trigger-transformation
        ; innermost(A1 <+ ... <+ An)
      )

Some relatives of `alltd` that add a strategy to apply on the way up.

    alldownup2(s1, s2) = rec x((s1 <+ all(x)); s2)
    alltd-fold(s1, s2) = rec x(s1 <+ all(x); s2)

Finally, the following strategies select the _leaves_ of a tree, where the determination of what is a leaf is up to a parameter strategy.

    leaves(s, is-leaf, skip: a * (a -> a) -> a) =
      rec x((is-leaf; s) <+ skip(x) <+ all(x))

    leaves(s, is-leaf) =
      rec x((is-leaf; s) <+ all(x))

A spine of a term is a chain of nodes from the root to some subterm. `spinetd` goes down one spine and applies `s` along the way to each node on the spine. The traversal stops when `s` fails for all children of a node.

    spinetd(s)  = s; try(one(spinetd(s)))
    spinebu(s)  = try(one(spinebu(s))); s
    spinetd'(s) = s; (one(spinetd'(s)) + all(fail))
    spinebu'(s) = (one(spinebu'(s)) + all(fail)); s

Apply `s` everywhere along al spines where `s` applies.

    somespinetd(s) = rec x(s; try(some(x)))
    somespinebu(s) = rec x(try(some(x)); s)
    spinetd'(s)    = rec x(s; (one(x) + all(fail)))
    spinebu'(s)    = rec x((one(x) + all(fail)); s)

While these strategies define the notion of applying along a spine, they are rarely used. In practice one would use more specific traversals with that determine which subterm to include in the search for a path.

TODO: examples

### 9.2.5. Recursive Patterns (*)

TODO: format checking

TODO: matching of complex patterns

TODO: contextual rules (local traversal)

### 9.2.6. Dynamic programming (*)

TODO (probably move to dynamic rules chapter)

[1]: 05-rewriting-strategies "Rewriting Strategies"
[2]: 08-creating-and-analyzing-terms "Creating and Analyzing Terms"
[3]: 12-dynamic-rules "Dynamic Rules"
