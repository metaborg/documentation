```eval_rst
.. highlight:: str
```

# 4. Term Rewriting

In [PartII][1] we saw how terms provide a structured representation for programs derived from a formal definition of the syntax of a programming language. Transforming programs then requires transformation of terms. In this chapter we show how to implement term transformations using _term rewriting_ in Stratego. In term rewriting a term is transformed by repeated application of _rewrite rules_.


## 4.1. Transformation with Rewrite Rules

To see how this works we take as example the language of propositional formulae, also known as Boolean expressions:

    module prop
    signature
      sorts Prop
      constructors
        False : Prop
        True  : Prop
        Atom  : String -> Prop
        Not   : Prop -> Prop
        And   : Prop * Prop -> Prop
        Or    : Prop * Prop -> Prop
        Impl  : Prop * Prop -> Prop
        Eq    : Prop * Prop -> Prop

Given this signature we can write terms such as `And(Impl(True(),False()),False())`, and `And(Atom("p"),False()))`. Atoms are also known as proposition letters; they are the variables in propositional formulae. That is, the truth value of an atom should be provided in order to fully evaluate an expression. Here we will evaluate expressions as far as possible, a transformation also known as _constant folding_. We will do this using _rewrite rules_ that define how to simplify a single operator application.

A _term pattern_ is a term with _meta variables_, which are identifiers that are not declared as (nullary) constructors. For example, `And(x, True())` is a term pattern with variable `x`. Variables in term patterns are sometimes called _meta_ variables, to distinguish them from variables in the source language being processed. For example, while atoms in the proposition expressions are variables from the point of view of the language, they are not variables from the perspective of a Stratego program.

A term pattern `p` _matches_ with a term `t`, if there is a _substitution_ that replaces the variables in `p` such that it becomes equal to `t`. For example, the pattern `And(x, True())` matches the term `And(Impl(True(),Atom("p")),True())` because replacing the variable `x` in the pattern by `Impl(True(),Atom("p"))` makes the pattern equal to the term. Note that `And(Atom("x"),True())` does _not_ match the term `And(Impl(True(),Atom("p")),True())`, since the subterms `Atom("x")` and `Impl(True(),Atom("p"))` do not match.

An _unconditional rewrite rule_ has the form `L : p1 -> p2`, where `L` is the name of the rule, `p1` is the left-hand side and `p2` the right-hand side term pattern. A rewrite rule `L : p1 -> p2` applies to a term `t` when the pattern `p1` matches `t`. The result is the instantiation of `p2` with the variable bindings found during matching. For example, the rewrite rule

    E : Eq(x, False()) -> Not(x)

rewrites the term `Eq(Atom("q"),False())` to `Not(Atom("q"))`, since the variable `x` is bound to the subterm `Atom("q")`.

Now we can create similar evaluation rules for all constructors of sort `Prop`:

    module prop-eval-rules
    imports prop
    rules
      E : Not(True())      -> False()
      E : Not(False())     -> True()
      E : And(True(), x)   -> x
      E : And(x, True())   -> x
      E : And(False(), x)  -> False()
      E : And(x, False())  -> False()
      E : Or(True(), x)    -> True()
      E : Or(x, True())    -> True()
      E : Or(False(), x)   -> x
      E : Or(x, False())   -> x
      E : Impl(True(), x)  -> x
      E : Impl(x, True())  -> True()
      E : Impl(False(), x) -> True()
      E : Eq(False(), x)   -> Not(x)
      E : Eq(x, False())   -> Not(x)
      E : Eq(True(), x)    -> x
      E : Eq(x, True())    -> x

Note that all rules have the same name, which is allowed in Stratego.

Next we want to _normalize_ terms with respect to a collection of rewrite rules. This entails applying all rules to all subterms until no more rules can be applied. The following module defines a rewrite system based on the rules for propositions above:

    module prop-eval
    imports libstrategolib prop-eval-rules
    strategies
      main = io-wrap(eval)
      eval = innermost(E)

The module imports the Stratego Library (`libstrategolib`) and the module with the evaluation rules, and then defines the `main` strategy to apply `innermost(E)` to the input term. (See the discussion of `io-wrap` in [Section11.2][2].) The `innermost` strategy from the library exhaustively applies its argument transformation to the term it is applied to, starting with _inner_ subterms.

We can now compile the program as discussed in [Chapter11][3]:

    $ strc -i prop-eval.str -la stratego-lib

This results in an executable `prop-eval` that can be used to evaluate Boolean expressions. For example, here are some applications of the program:

    $ cat test1.prop
    And(Impl(True(),And(False(),True())),True())

    $ ./prop-eval -i test1.prop
    False

    $ cat test2.prop
    And(Impl(True(),And(Atom("p"),Atom("q"))),ATom("p"))

    $ ./prop-eval -i test2.prop
    And(And(Atom("p"),Atom("q")),ATom("p"))

We can also import these definitions in the [Stratego Shell][4], as illustrated by the following session:

    $ stratego-shell
    stratego> import prop-eval

    stratego> !And(Impl(True(),And(False(),True())),True())
    And(Impl(True(),And(False,True)),True)

    stratego> eval
    False

    stratego> !And(Impl(True(),And(Atom("p"),Atom("q"))),ATom("p"))
    And(Impl(True,And(Atom("p"),Atom("q"))),ATom("p"))

    stratego> eval
    And(And(Atom("p"),Atom("q")),ATom("p"))

    stratego> :quit
    And(And(Atom("p"),Atom("q")),ATom("p"))
    $

The first command imports the `prop-eval` module, which recursively loads the evaluation rules and the library, thus making its definitions available in the shell. The `!` commands replace the current term with a new term. (This _build_ strategy will be properly introduced in [Chapter16][5].)

The next commands apply the `eval` strategy to various terms.

## 4.2. Adding Rules to a Rewrite System

Next we extend the rewrite rules above to rewrite a Boolean expression to disjunctive normal form. A Boolean expression is in disjunctive normal form if it conforms to the following signature:

    signature
      sorts Or And NAtom Atom
      constructors
        Or   : Or * Or -> Or
             : And -> Or
        And  : And * And -> And
             : NAtom -> And
        Not  : Atom -> NAtom
             : Atom -> NAtom
        Atom : String -> Atom

We use this signature only to describe what a disjunctive normal form is, not in an the actual Stratego program. This is not necessary, since terms conforming to the DNF signature are also `Prop` terms as defined before. For example, the disjunctive normal form of

    And(Impl(Atom("r"),And(Atom("p"),Atom("q"))),ATom("p"))

is

    Or(And(Not(Atom("r")),ATom("p")),
       And(And(Atom("p"),Atom("q")),ATom("p")))

Module `prop-dnf-rules` extends the rules defined in `prop-eval-rules` with rules to achieve disjunctive normal forms:

    module prop-dnf-rules
    imports prop-eval-rules
    rules
      E : Impl(x, y) -> Or(Not(x), y)
      E : Eq(x, y)   -> And(Impl(x, y), Impl(y, x))

      E : Not(Not(x)) -> x

      E : Not(And(x, y)) -> Or(Not(x), Not(y))
      E : Not(Or(x, y))  -> And(Not(x), Not(y))

      E : And(Or(x, y), z) -> Or(And(x, z), And(y, z))
      E : And(z, Or(x, y)) -> Or(And(z, x), And(z, y))

The first two rules rewrite implication (`Impl`) and equivalence (`Eq`) to combinations of `And`, `Or`, and `Not`. The third rule removes double negation. The fifth and sixth rules implement the well known DeMorgan laws. The last two rules define distribution of conjunction over disjunction.

We turn this set of rewrite rules into a compilable Stratego program in the same way as before:

    module prop-dnf
    imports libstrategolib prop-dnf-rules
    strategies
      main = io-wrap(dnf)
      dnf = innermost(E)

compile it in the usual way

    $ strc -i prop-dnf.str -la stratego-lib

so that we can use it to transform terms:

    $ cat test3.prop
    And(Impl(Atom("r"),And(Atom("p"),Atom("q"))),ATom("p"))
    $ ./prop-dnf -i test3.prop
    Or(And(Not(Atom("r")),ATom("p")),And(And(Atom("p"),Atom("q")),ATom("p")))

[1]: tutorial-xt.html "Part"
[2]: running-stratego-programs.html#identity-with-io "11.2."
[3]: running-stratego-programs.html "Chapter"
[4]: running-stratego-programs.html#stratego-shell "11.4."
[5]: stratego-creating-and-analyzing-terms.html "Chapter"
