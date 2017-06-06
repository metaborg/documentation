```eval_rst
.. highlight:: str
```

# 6. Rules and Strategies

Pure term rewriting is not adequate for program transformation because of the lack of control over the application of rules.  Attempts to encode such control within the pure rewriting paradigm lead to functionalized control by means of extra rules and constructors, at the expense of traversal overhead and at the loss of the separation of rules and strategies.  By selecting the appropriate rules and strategy for a transformation, Stratego programmers can control the application of rules, while maintaining the separation of rules and strategies and keeping traversal overhead to a minimum.

We saw that many transformation problems can be solved by alternative strategies such as a one-pass bottom-up or top-down traversals.  Others can be solved by selecting the rules that are applied in an innermost normalization, rather than all the rules in a specification.  However, no fixed set of such alternative strategies will be sufficient for dealing with all transformation problems.  Rather than providing one or a few fixed collection of rewriting strategies, Stratego supports the _composition_ of strategies from basic building blocks with a few fundamental operators.

On this page we define the basic notions of rules and strategies, and we will see how new strategies and strategy combinators can be defined.


## 6.1. What is a rule?

A _rule_ defines a transformation on terms. A _named rewrite rule_ is a declaration of the form:

    L : p1 -> p2

where `L` is the rule name, `p1` the left-hand side term pattern, and `p2` the right-hand side term pattern.  A rule can be applied _through its name_ to a term. It will transform the term if the term matches with `p1`, and will replace the term with `p2` instantiated with the variables bound during the match to `p1`.  The application _fails_ if the term does not match `p1`.  Thus, a _transformation_ is a _partial function from terms to terms_.

Let's look at an example. The `SwapArgs` rule swaps the sub-terms of the `Plus` constructor.  Note that it is possible to introduce rules on the fly in the [Stratego Shell](http://hydra.nixos.org/build/10497731/download/1/manual/chunk-chapter/ref-stratego-shell.html).

    stratego> SwapArgs : Plus(e1,e2) -> Plus(e2,e1)

Now we create a new term, and apply the `SwapArgs` rule to it by calling its name at the prompt.  (The build `!t` of a term replaces the current term by `t`, as is explained [here](#).)

    stratego> !Plus(Var("a"),Int("3"))
    Plus(Var("a"),Int("3"))
    stratego> SwapArgs
    Plus(Int("3"),Var("a"))

The application of `SwapArgs` fails when applied to a term to which the left-hand side does not match.  For example, since the pattern `Plus(e1,e2)` does not match with a term constructed with `Times` the following application fails:

    stratego> !Times(Int("4"),Var("x"))
    Times(Int("4"),Var("x"))
    stratego> SwapArgs
    command failed

A rule is applied at the _root_ of a term, not at one of its subterms.  Thus, the following application fails even though the term _contains_ a `Plus` subterm:

    stratego> !Times(Plus(Var("a"),Int("3")),Var("x"))
    Times(Plus(Var("a"),Int("3")),Var("x"))
    stratego> SwapArgs
    command failed

Likewise, the following application only transforms the outermost occurrence of `Plus`, not the inner occurrence:

    stratego> !Plus(Var("a"),Plus(Var("x"),Int("42")))
    Plus(Var("a"),Plus(Var("x"),Int("42")))
    stratego> SwapArgs
    Plus(Plus(Var("x"),Int("42")),Var("a"))

Finally, there may be multiple rules with the same name.  This has the effect that all rules with that name will be tried in turn until one succeeds, or all fail.  The rules are tried in some undefined order.  This means that it only makes sense to define rules with the same name if they are mutually exclusive, that is, do not have overlapping left-hand sides.  For example, we can extend the definition of `SwapArgs` with a rule for the `Times` constructor, as follows:

    stratego> SwapArgs : Times(e1, e2) -> Times(e2, e1)

Now the rule can be applied to terms with a `Plus` *and* a `Times` constructor, as illustrated by the following applications:

    stratego> !Times(Int("4"),Var("x"))
    Times(Int("4"),Var("x"))
    stratego> SwapArgs
    Times(Var("x"),Int("4"))

    stratego> !Plus(Var("a"),Int("3"))
    Plus(Var("a"),Int("3"))
    stratego> SwapArgs
    Plus(Int("3"),Var("a"))

Later we will see that a rule is nothing more than a syntactical convention for a strategy definition.


## 6.2. What is a Strategy?

A rule defines a transformation, that is, a partial function from terms to terms.  A _strategy expressions_ is a combination of one or more transformations into a new transformation.  So, a strategy expressions also defines a transformation, i.e., a partial function from terms to terms.  Strategy _operators_ are functions from transformations to transformations.

In the [previous chapter](#) we saw some examples of strategy expressions.  Lets examine these examples in the light of our new definition.  First of all, _rule names_ are basic strategy expressions.  If we import module `prop-laws`, we have at our disposal all rules it defines as basic strategies:

    stratego> import prop-laws
    stratego> !Impl(True(), Atom("p"))
    Impl(True, Atom("p"))
    stratego> DefI
    Or(Not(True),Atom("p"))

Next, given a collection of rules we can create more complex transformations by means of strategy operators.  For example, the `innermost` strategy creates from a collection of rules a new transformation that exhaustively applies those rules.

    stratego> !Eq(Atom("p"), Atom("q"))
    Eq(Atom("p"),Atom("q"))

    stratego> innermost(DefI <+ DefE <+ DAOL <+ DAOR <+ DN <+ DMA <+ DMO)

    Or(Or(And(Not(Atom("p")),Not(Atom("q"))),
          And(Not(Atom("p")),Atom("p"))),
       Or(And(Atom("q"),Not(Atom("q"))),
          And(Atom("q"),Atom("p"))))

(Exercise: add rules to this composition that remove tautologies or false propositions.)

Here we see that the rules are first combined using the choice operator `<+` into a composite transformation, which is the argument of the `innermost` strategy.

The `innermost` strategy always succeeds (but may not terminate), but this is not the case for all strategies.  For example `bottomup(DefI)` will not succeed, since it attempts to apply rule `DefI` to all sub-terms, which is clearly not possible.  Thus, strategies extend the property of rules that they are _partial_ functions from terms to terms.

Observe that in the composition `innermost(...)`, the term to which the transformation is applied is never mentioned.  The 'current term', to which a transformation is applied is often implicit in the definition of a strategy.  That is, there is no variable that is bound to the current term and then passed to an argument strategy.  Thus, a strategy operator such as `innermost` is a function from transformations to transformations.

While strategies are functions, they are not necessarily _pure_ functions.  Strategies in Stratego may have side effects such as performing input/output operations.  This is of course necessary in the implementation of basic tool interaction such as provided by `io-wrap`, but is also useful for debugging.  For example, the `debug` strategy prints the current term, but does not transform it.  We can use it to visualize the way that `innermost` transforms a term.

    stratego> !Not(Impl(Atom("p"), Atom("q")))
    Not(Impl(Atom("p"),Atom("q")))
    stratego> innermost(debug(!"in:  "); (DefI <+ DefE <+ DAOL <+ DAOR <+ DN <+ DMA <+ DMO); debug(!"out: "))
    in:  p
    in:  Atom("p")
    in:  q
    in:  Atom("q")
    in:  Impl(Atom("p"),Atom("q"))
    out: Or(Not(Atom("p")),Atom("q"))
    in:  p
    in:  Atom("p")
    in:  Not(Atom("p"))
    in:  q
    in:  Atom("q")
    in:  Or(Not(Atom("p")),Atom("q"))
    in:  Not(Or(Not(Atom("p")),Atom("q")))
    out: And(Not(Not(Atom("p"))),Not(Atom("q")))
    in:  p
    in:  Atom("p")
    in:  Not(Atom("p"))
    in:  Not(Not(Atom("p")))
    out: Atom("p")
    in:  p
    in:  Atom("p")
    in:  q
    in:  Atom("q")
    in:  Not(Atom("q"))
    in:  And(Atom("p"),Not(Atom("q")))
    And(Atom("p"),Not(Atom("q")))

This session nicely shows how innermost traverses the term it transforms.  The `in:` lines show terms to which it attempts to apply a rule, the `out:` lines indicate when this was successful and what the result of applying the rule was.  Thus, `innermost` performs a post-order traversal applying rules after transforming the sub-terms of a term.  (Note that when applying `debug` to a string constant, the quotes are not printed.)


## 6.3. Strategy Definitions

Stratego programs are about defining transformations in the form of rules and strategy expressions that combine them.  Just defining strategy _expressions_ does not scale, however.  Strategy _definitions_ are the abstraction mechanism of Stratego and allow naming and parametrization of strategy expressions for reuse.

### 6.3.1. Simple Strategy Definition and Call

A simple strategy definition names a strategy expression.  For instance, the following module defines a combination of rules (`dnf-rules`), and some strategies based on it:

    module dnf-strategies
    imports libstrategolib prop-dnf-rules
    strategies

      dnf-rules =
        DefI <+ DefE <+ DAOL <+ DAOR <+ DN <+ DMA <+ DMO

      dnf =
        innermost(dnf-rules)

      dnf-debug =
        innermost(debug(!"in:  "); dnf-rules; debug(!"out: "))

      main =
        io-wrap(dnf)

Note how `dnf-rules` is used in the definition of `dnf`, and `dnf` itself in the definition of `main`.

In general, a definition of the form

    f = s

introduces a new transformation `f`, which can be invoked by calling `f` in a strategy expression, with the effect of executing strategy expression `s`.  The expression should have no free variables.  That is, all strategies called in `s` should be defined strategies. Simple strategy definitions just introduce names for strategy expressions.  Still, such strategies have an argument, namely the implicit current term.


### 6.3.2. Parametrized Definitions

Strategy definitions with strategy and/or term parameters can be used to define transformation _schemas_ that can instantiated for various situations.

A parametrized strategy definition of the form

    f(x1,...,xn | y1,..., ym) = s

introduces a user-defined operator `f` with `n` _strategy parameters_ and `m` _term parameters_.  Such a user-defined strategy operator can be called as `f(s1,...,sn|t1,...,tm)` by providing it `n` strategy arguments and `m` term arguments.  The meaning of such a call is the body `s` of the definition in which the actual arguments have been substituted for the formal parameters.  Strategy arguments and term arguments can be left out of calls and definitions.  That is, a call `f(|)` without strategy and term arguments can be written as `f()`, or even just `f`.  A call `f(s1,..., sn|)` without term arguments can be written as `f(s1,...,sn)`.  The same holds for strategy definitions.

In most cases the term parameters are simple variable names to which the argument will be bound when the strategy is called. However, it is also possible to use a _term pattern_ in place of a term parameter, to which the argument will be matched. The strategy will fail when one or more term arguments could not be matched to their corresponding term pattern. These term patterns have the same freedoms as those used at left-hand side of a rule. For example, the following strategies act like a switch-case:

    strategies
      to-english(|1) = !"one"
      to-english(|2) = !"two"
      to-english(|_) = !"many"

Or a more complex example:

    strategies
      get-type(|<is-list>)      = !"A list"
      get-type(|<not(is-list)>) = !"Not a list"

As we will see, strategies such as `innermost`, `topdown`, and `bottomup` are _not built into the language_, but are defined using strategy definitions in the language itself using more basic combinators, as illustrated by the following definitions (without going into the exact meaning of these definitions):

    strategies
      try(s)      = s <+ id
      repeat(s)   = try(s; repeat(s))
      topdown(s)  = s; all(topdown(s))
      bottomup(s) = all(bottomup(s)); s

Such parametrized strategy operators are invoked by providing arguments for the parameters.  Specifically, strategy arguments are instantiated by means of strategy expressions.  Wherever the argument is invoked in the body of the definition, the strategy expression is invoked.  For example, in the [previous chapter](#) we saw the following instantiations of the `topdown`, `try`, and `repeat` strategies:

    module prop-desugar
    // ...
    strategies

      desugar =
        topdown(try(DefI <+ DefE))

      impl-nf =
        topdown(repeat(DefN <+ DefA2 <+ DefO1 <+ DefE))

Multiple definitions with the same name but with a _different_ numbers of parameters are treated as _different_ strategy operators.


### 6.3.3. Local Definitions

Strategy definitions at top-level are visible everywhere.  Sometimes it is useful to define a _local_ strategy operator.  This can be done using a let expression of the form `let d* in s end`, where `d*` is a list of definitions.  For example, in the following strategy expression, the definition of `dnf-rules` is only visible in the instantiation of `innermost`:

    let dnf-rules = DefI <+ DefE <+ DAOL <+ DAOR <+ DN <+ DMA <+ DMO
     in innermost(dnf-rules)
    end

The current version of Stratego does not support hidden strategy definitions at the module level.  Such a feature is under consideration for a future version.

### 6.3.4. Extending Definitions

As we saw in [?](#), a Stratego program can introduce several rules with the same name. It is even possible to extend rules across modules.  This is also possible for strategy definitions.  If two strategy definitions have the same name and the same number of parameters, they effectively define a single strategy that tries to apply the bodies of the definitions in some undefined order.  Thus, a definition of the form

    strategies
      f = s1
      f = s2

entails that a call to `f` has the effect of first trying to apply `s1`, and if that fails applies `s2`, or the other way around.  Thus, the definition above is either translated to

    strategies
      f = s1 <+ s2

or to

    strategies
      f = s2 <+ s1


## 6.4. Calling Primitives

Stratego provides combinators for composing transformations and basic operators for analyzing, creating and traversing terms.  However, it does not provide built-in support for other types of computation such as input/output and process control.  In order to make such functionality available to Stratego programmers, the language provides access to user-definable _primitive_ strategies through the `prim` construct.  For example, the following call to `prim` invokes the `SSL_printnl` native function:

    stratego> prim("SSL_printnl", stdout(), ["foo", "bar"])
    foobar
    ""

In general, a call `prim("f", s* | t*)` represents a call to a _primitive function_ `f` with strategy arguments `s*` and term arguments `t*`. Note that the 'current' term is not passed automatically as argument.

This mechanism allows the incorporation of mundane tasks such as arithmetic, I/O, and other tasks not directly related to transformation, but necessary for the integration of transformations with the other parts of a transformation system.


### 6.4.1. Implementing Primitives

The Stratego Library provides all the primitives for I/O, arithmetic, string processing, and process control that are usually needed in Stratego programs.  However, it is possible to add new primitives to a program as well.  That requires linking with the compiled program a library that implements the function. See the documentation of [?](#) for instructions.


## 6.5. External Definitions

The [Stratego Compiler](#ref-strc) is a _whole program compiler_. That is, the compiler includes all definitions from imported modules (transitively) into the program defined by the main module (the one being compiled).  This is the reason that the compiler takes its time to compile a program.  To reduce the compilation effort and the size of the resulting programs it is possible to create separately compiled _libraries_ of Stratego definitions.  The strategies that such a library provides are declared as _external_ definitions. A declaration of the form

    external f(s1 ... sn | x1 ... xm)

states that there is an externally defined strategy operator `f` with `n` strategy parameters and `m` term parameters.  When compiling a program with external definitions, a library should be provided that implements these definitions.

The Stratego Library is provided as a separately compiled library. The `libstrategolib` module that we have been using in the example programs contains external definitions for all strategies in the library, as illustrated by the following excerpt:

    module libstrategolib
    // ...
    strategies
      // ...
      external io-wrap(s)
      external bottomup(s)
      external topdown(s)
      // ...

When compiling a program using the library we used the `-la stratego-lib` option to provide the implementation of those definitions.


### 6.5.1. External Definitions cannot be Extended

Unlike definitions imported in the normal way, external definitions cannot be extended.  If we try to compile a module extending an external definition, such as

    module wrong
    imports libstrategolib
    strategies
      bottomup(s) = fail

compilation fails:

    $ strc -i wrong.str
    [ strc | info ] Compiling 'wrong.str'
    error: redefining external definition: bottomup/1-0
    [ strc | error ] Compilation failed (3.66 secs)


### 6.5.2. Creating Libraries

It is possible to create your own Stratego libraries as well. Currently that exposes you to a bit of compilation gibberish; in the future this may be incorporated in the Stratego compiler.  Lets create a library for the rules and strategy definitions in the `prop-laws` module.  We do this using the `--library` option to indicate that a library is being built, and the `-c` option to indicate that we are only interested in the generated C code.

    $ strc -i prop-laws.str -c -o libproplib.rtree --library
    [ strc | info ] Compiling 'proplib.str'
    [ strc | info ] Front-end succeeded         : [user/system] = [4.71s/0.77s]
    [ strc | info ] Abstract syntax in 'libproplib.rtree'
    [ strc | info ] Concrete syntax in 'libproplib.str'
    [ strc | info ] Export of externals succeeded : [user/system] = [2.02s/0.11s]
    [ strc | info ] Back-end succeeded          : [user/system] = [6.66s/0.19s]
    [ strc | info ] Compilation succeeded       : [user/system] = [13.4s/1.08s]
    $ rm libproplib.str

The result is of this compilation is a module `libproplib` that contains the external definitions of the module _and_ those inherited from `libstrategolib`. (This module comes in to versions; one in concrete syntax `libproplib.str` and one in abstract syntax `libproplib.rtree`; for some obscure reason you should throw away the `.str` file.) Furthermore, the Stratego Compiler produces a C program `libproplib.c` with the implementation of the library. This C program should be turned into an object library using `libtool`, as follows:

    $ libtool --mode=compile gcc -g -O -c libproplib.c -o libproplib.o -I <path/to/aterm-stratego/include>
    ...
    $ libtool --mode=link gcc -g -O -o libproplib.la libproplib.lo
    ...

The result is a shared library `libproplib.la` that can be used in other Stratego programs. (TODO: the production of the shared library should really be incorporated into strc.)


### 6.5.3. Using Libraries

Programmers that want to use your library can now import the module with external definitions, instead of the original module.

    module dnf-tool
    imports libproplib
    strategies
      main = main-dnf

This program can be compiled in the usual way, adding the new library to the libraries that should be linked against:

    $ strc -i dnf-tool.str -la stratego-lib -la ./libproplib.la

    $ cat test3.prop
    And(Impl(Atom("r"),And(Atom("p"),Atom("q"))),ATom("p"))

    $ ./dnf-tool -i test3.prop
    Or(And(Not(Atom("r")),ATom("p")),And(And(Atom("p"),Atom("q")),ATom("p")))

To correctly deploy programs based on shared libraries requires some additional effort.  [?](#) explains how to create deployable packages for your Stratego programs.


## 6.6. Dynamic Calls

Strategies can be called dynamically by name, i.e., where the name of the strategy is specified as a string. Such calls can be made using the `call` construct, which has the form:

    call(f | s1, ..., sn | t1, ..., tn)

where `f` is a term that should evaluate to a string, which indicates the name of the strategy to be called, followed by a list of strategy arguments, and a list of term arguments.

Dynamic calls allow the name of the strategy to be computed at run-time.  This is a rather recent feature of Stratego that was motivated by the need for call-backs from a separately compiled Stratego library combined with the computation of dynamic rule names.  Otherwise, there is not yet much experience with the feature.

In the current version of Stratego it is necessary to 'register' a strategy to be able to call it dynamically.  (In order to avoid deletion in case it is not called explicitly somewhere in the program.)  Strategies are registered by means of a dummy strategy definition `DYNAMIC-CALLS` with calls to the strategies that should called dynamically.

    DYNAMICAL-CALLS = foo(id)


## 6.7. Summary

We have learned that rules and strategies define _transformations_, that is, functions from terms to terms that can fail, i.e., partial functions. Rule and strategy definitions introduce names for transformations. Parametrized strategy definitions introduce new strategy _operators_, functions that construct transformations from transformations, and support term patterns as parameters.

Primitive strategies are transformations that are implemented in some language other than Stratego (usually Java), and are called through the `prim` construct.  External definitions define an interface to a separately compiled library of Stratego definitions.  Dynamic calls allow the name of the strategy to be called to be computed as a string.
