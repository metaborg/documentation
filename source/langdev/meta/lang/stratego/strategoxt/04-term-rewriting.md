```eval_rst
.. highlight:: str
```

# 4. Term Rewriting

In this chapter we show how to implement term transformations using _term rewriting_ in Stratego. In term rewriting a term is transformed by repeated application of _rewrite rules_.


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
      E : Impl(x, False()) -> Not(x)
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

The module imports the Stratego Library (`libstrategolib`) and the module with the evaluation rules, and then defines the `main` strategy to apply `innermost(E)` to the input term. The `innermost` strategy from the library exhaustively applies its argument transformation to the term it is applied to, starting with _inner_ subterms.

As an aside, we have now seen Stratego modules with `rules` and `strategies` sections. It's worth noting that a module can have any number of sections of either type, and that there is no actual semantic difference between the two section headings. In fact, either rewrite rules and/or strategy definitions can occur in either kind of section. Nevertheless, it often helps with making your transformations clearer to generally segregate rules and strategy definitions, and so both headings are allowed so you can punctuate your Stratego modules with them to improve readability.

In any case, we can now compile the above program:

    $ strc -i prop-eval.str -la stratego-lib

This results in an executable `prop-eval` that can be used to evaluate Boolean expressions. For example, here are some applications of the program:

    $ cat test1.prop
    And(Impl(True(),And(False(),True())),True())

    $ ./prop-eval -i test1.prop
    False

    $ cat test2.prop
    And(Impl(True(),And(Atom("p"),Atom("q"))),Atom("p"))

    $ ./prop-eval -i test2.prop
    And(And(Atom("p"),Atom("q")),Atom("p"))

We can also import these definitions in the Stratego Shell, as illustrated by the following session:

    $ stratego-shell
    stratego> import prop-eval

    stratego> !And(Impl(True(),And(False(),True())),True())
    And(Impl(True(),And(False,True)),True)

    stratego> eval
    False

    stratego> !And(Impl(True(),And(Atom("p"),Atom("q"))),Atom("p"))
    And(Impl(True,And(Atom("p"),Atom("q"))),Atom("p"))

    stratego> eval
    And(And(Atom("p"),Atom("q")),Atom("p"))

    stratego> :quit
    And(And(Atom("p"),Atom("q")),Atom("p"))
    $

The first command imports the `prop-eval` module, which recursively loads the evaluation rules and the library, thus making its definitions available in the shell. The `!` commands replace the current term with a new term. (This _build_ strategy will be properly introduced in [Chapter 8][1].)

The next commands apply the `eval` strategy to various terms.

## 4.2. Running `prop-eval` in Spoofax/Eclipse

If you'd like to try out some of these Stratego examples in Spoofax/Eclipse, the first step is to define a _concrete syntax_ for Boolean expressions that will parse to the sorts of ATerms that we have been working with. The [SDF3 Manual](../../sdf3/index.md) provides the best introduction to how one might go about doing that, but here is the bulk of an SDF3 syntax definition that will allow us to represent any of the ATerms above:

    context-free syntax

      Prop.True  = <1>
      Prop.False = <0>
      Prop.Atom  = String
      Prop.Not   = <!<Prop>>
      Prop.And   = <<Prop> & <Prop>>  {left}
      Prop.Or    = <<Prop> | <Prop>>  {left}
      Prop.Impl  = [[Prop] -> [Prop]] {right}
      Prop.Eq    = <<Prop> = <Prop>>  {non-assoc}
      Prop       = <(<Prop>)> {bracket}

      String = ID

    context-free priorities

      Prop.Not
      > Prop.And
      > Prop.Or
      > Prop.Impl
      > Prop.Eq

With this grammar in place, the first two examples at the beginning of this chapter (just below the `prop` signature) can be expressed by `(1 -> 0) & 0` and `p & 0`, respectively. So you can see that the concrete syntax will actually make it much easier to construct the example expressions used throughout this manual.

If you'd like to see this in action in Spoofax/Eclipse, you can set up a language with the above grammar. Or you can clone the publicly-available [repository](https://code.studioinfinity.org/glen/spoofax_prop) containing most of the `prop` language examples from this manual.

Either way, you can place either of the above expressions in a file (`syntax/examples/sec4.1_A.spl` or ...`_B.spl` in the repository) and visit it in Eclipse. Then if you select "Syntax > Show parsed AST" from the Spoofax menu, the parsed AST matching our first expressions above will pop up in the editor.

### 4.2.1 Using Editor Services to run a Stratego transformation

Naturally, we'd now like to run `prop-eval` in Spoofax/Eclipse. So we can take the `prop-eval-rules` module above and save it as `trans/prop-eval-rules.str`, with just one small change. Instead of `import prop` in the second line, we can say `import signatures/-`, since Spoofax has written out the signature implied by the grammar for us.

We're also going to have a small module `trans/prop-eval.str` to call the `prop-eval-rules`. It starts out rather similarly to the `prop-eval` for Stratego/XT; here's the first four lines:

    module prop-eval
    imports libstrategolib prop-eval-rules
    strategies
      eval = innermost(E)

Note that we don't have the `main = io-wrap(eval)` line. For Stratego/XT, that was the sort of "glue" we needed to connect the execution environment with the basic `eval` strategy we've defined in Stratego. Similarly, a "glue" expression is needed in Spoofax/Eclipse as well. Because the Eclipse environment is more flexible, the necessary glue is rather more complicated; for now we needn't worry much about its details:

    // Interface eval strategy with editor services and file system
    do-eval: (selected, _, _, path, project-path) -> (filename, result)
      with filename := <guarantee-extension(|"eval.aterm")> path
         ; result   := <eval> selected

How do we now invoke this interface? That's where the Spoofax [Editor Services](../../esv) (ESV) comes in. ESV is responsible, among other things, for the "Spoofax" menu item on the top bar of Eclipse. And you can add a new submenu, which we'll call "Manual", to that menu with a little module `editor/Manual.esv` like this:

    module Manual
    menus
      menu: "Manual" (openeditor) (source)
        action: "prop-eval" = do-eval

Finally, we have to get Spoofax to see our new Stratego and ESV modules. We do this by importing them in the main Stratego and ESV files of the project. In the repository these are in `trans/spoofax_propositional_language.str` and `editor/Main.esv`, respectively. Their beginnings end up looking like:

    module spoofax_propositional_language

    imports

      completion/completion
      pp
      outline
      analysis
      prop-eval
    rules // Debugging

and

    module Main
    imports
      Syntax
      Analysis
      Manual
    language

Now at last we're ready to invoke the `eval` transformation. Make sure you have your project rebuilt cleanly. Visit a `.spl` file that has the expression you'd like to evaluate, such as `syntax/examples/sec4.1_test1.spl` containing `(1 -> 0 & 1) & 1`. Then select "Spoofax > Manual > prop-eval" from the menu bar to see the value (in this case `False()`. (There's also a ...`_test2.spl` with `(1 -> p & q) & p` for the other example, and you can create your own files for some of the expressions in the Stratego Shell session shown above, if you like.)

## 4.3. Adding Rules to a Rewrite System

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

    And(Impl(Atom("r"),And(Atom("p"),Atom("q"))),Atom("p"))

is

    Or(And(Not(Atom("r")),Atom("p")),
       And(And(Atom("p"),Atom("q")),Atom("p")))

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
    And(Impl(Atom("r"),And(Atom("p"),Atom("q"))),Atom("p"))
    $ ./prop-dnf -i test3.prop
    Or(And(Not(Atom("r")),Atom("p")),And(And(Atom("p"),Atom("q")),Atom("p")))

[1]: 08-creating-and-analyzing-terms.md "Creating and Analyzing Terms"

## 4.4. Using Spoofax Testing Language to run a Stratego Transformation

We can of course run `prop-dnf` in Spoofax/Eclipse in the same way as before. The `prop-dnf-rules` module is saved verbatim in `trans/prop-dnf-rules.str`, and the `prop-dnf` module becomes the following `trans/prop-dnf.str`:

    module prop-dnf
    imports libstrategolib prop-dnf-rules
    strategies
      dnf = innermost(E)

      // Interface dnf strategy with editor services and file system
      do-dnf: (selected, _, _, path, project-path) -> (filename, result)
        with filename := <guarantee-extension(|"dnf.aterm")> path
           ; result   := <dnf> selected

If you add a "prop-dnf" action to `editor/Manual.esv` calling `do-dnf` and rebuild the project, then you can visit, say, `syntax/examples.sec4.2_test3.spl` containing `(r -> p & q) & p` to produce exactly the DNF shown above.

However, we also want use this example to show another method of running Stratego strategies from the Eclipse IDE.

The [Spoofax Testing Language](../../spt/index.md) (SPT) is a declarative language that provides for a full range of tests for a Spoofax language project. As such, it includes the ability to run an arbitrary Stratego strategy on the results of parsing an arbitrary piece of the language you're working with.

So, we can just take our test3 expression above and make it a part of an SPT test suite, which we will call `test/manual-suite.spt`:

    module manual-suite
    language Spoofax-Propositional-Language

    test sec4_2_test3 [[
      (r -> p & q) & p
    ]] run dnf

Once we have saved this file, the tests run automatically. What does this mean? The file seems to be just "sitting there;" there's no indication that anything is happening. That's because this test we've just written succeeds. All we asked is that Spoofax run the dnf transformation on the results of parsing the test expression. It did that, and the transformation succeeded. So all is well, and no output is generated.

But of course, we want to check the result of the transformation as well. Fortunately, we know what we expect it to be. So we can change the test like so:

    test sec4_2_test3_ex [[
      (r -> p & q) & p
    ]] run dnf to Or(And(Not(Atom("r")),Atom("p")),
                     And(And(Atom("p"),Atom("q")),Atom("p")))

Now if there is no error or warning on this test then you know the `dnf` strategy produced the result shown in the `to` clause, and otherwise, the actual result will be shown in the error popup.

What if you _don't_ know what the expression is going to produce? Then you can just put a dummy expression like `Atom("x")` in the `to` clause, and you will be sure to get an error. The error popup will show the actual transformation results. But beware! The results will be hard to read because of the annotations that Spoofax adds to track where in the source code each part of the AST originates. (For example, in the example above we get

    Got: Or(And(Not(Atom("r"{TermIndex("test/manual-suite.spt",1)}){TermIndex
     ("test/manual-suite.spt",2)}),Atom("p"{TermIndex("test/manual-suite.spt",9)})
     {TermIndex("test/manual-suite.spt",10)}),And(And(Atom("p"{TermIndex("test/manual-
     suite.spt",3)}){TermIndex("test/manual-suite.spt",4)},Atom("q"{TermIndex
     ("test/manual-suite.spt",5)}){TermIndex("test/manual-suite.spt",6)}){TermIndex
     ("test/manual-suite.spt",7)},Atom("p"{TermIndex("test/manual-suite.spt",9)})
     {TermIndex("test/manual-suite.spt",10)}))

Nevertheless, with the editor outliner you can puzzle out what your transformation has done. The fact remains that it is most practical to put the actual expected result of the transformation in the `to` clause.
