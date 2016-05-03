```eval_rst
.. highlight:: DynSem
```

# Getting started

This guide will get you started with DynSem to specify the dynamic semantics of your language. By the end of these instructions you will have learnt how to do the following:

1. [Define your first semantics module](#define-your-first-module)
2. [Specify semantics of context-free language constructs](#specifying-context-free-language-constructs)
3. [Specify semantics of context-sensitive language constructs](#specifying-context-sensitive-language-constructs)
4. [Run an interpreter for an object language](#running-an-interpreter-for-an-object-language)
5. [Extend specifications with native operations](#extending-specifications-with-native-operations)
6. [Writing to standard output and reading standard input](#writing-to-standard-output-and-reading-standard-input)
7. [Interact with native data types](#interacting-with-native-data-types)
8. [Write Java code that invokes the generated interpreter](#interacting-with-the-interpreter-from-java)


### The *SIMPL* language as running example

This guide is centered around a very simple language we call *SIMPL*. The *SIMPL* code is maintained in it's own [GitHub repository][1]. We start with a basic definition (in [SDF3][2]) of concrete syntax which covers arithmetic expressions:

```sdf3
context-free start-symbols
  Exps

context-free syntax

  Exps.Lit   = <<INT>>
  Exps.Plus  = <<Exps> + <Exps>> {left}
  Exps.Minus = <<Exps> - <Exps>> {left}
  Exps.Times = <<Exps> * <Exps>> {left}

  Exps = <(<Exps>)> {bracket}
```

Note that terms of the sort `Exps` are start symbols for *SIMPL* programs.

## Defining your first DynSem module

We create the main DynSem module named *trans/simpl* in the file `trans/simpl.ds`:

```dynsem
module trans/simpl

imports
  src-gen/ds-signatures/simpl-sig

```

The module imports the abstract syntax definitions (term signatures) which is generated from the concrete syntax definition:

```dynsem
module ds-signatures/simpl-sig

imports ds-signatures/Common-sig

signature
  sorts
    Exp
  constructors
    Lit : INT -> Exp
    Plus : Exp * Exp -> Exp
    Minus : Exp * Exp -> Exp
    Times : Exp * Exp -> Exp
```

Importing these makes the sorts and constructors available to the rest of the modules. We extend module *trans/simpl* with definitions for value sorts and for the main reduction relation:

```dynsem
module trans/simpl

imports
  src-gen/ds-signatures/simpl-sig

signature
  sorts
    V

  constructors
    NumV: Int -> V

  arrows
    Exp --> V

  variables
    v : V

```

We declared constructor *NumV* which will be used to represent numerical value terms. We also declare reduction relation `-->` from `Exp` terms to values `V`, and a variable scheme for variables named *v*. For details about the signature section of DynSem specification see the [DynSem Language Reference][3].

## Specifying context-free language constructs

We specify reduction rules for *SIMPL* constructs that do not depend on the evaluation contexts (such as environments). These are *number literals*, and simple *arithmetic operations*. The reduction rules are given in a big-step style:

```dynsem
rules
  Lit(s) --> NumV(parseI(s)).

  Plus(e1, e2) --> NumV(addI(i1, i2))
  where
    e1 --> NumV(i1);
    e2 --> NumV(i2).
```

The first rule specifies that literal terms such as `42` whose abstract syntax is of the form `Lit("42")` evaluate to `NumV` terms. The second rule specifies the semantics of the addition expressions of the form `Plus(e1, e2)` inductively on the default reduction relation. First the expression **e1** is reduced and the expectation is that it reduces to a `NumV` term. Variable `i1` is bound to the integer value surrounded by the resulting `NumV` term. This is captured in the first premise of the reduction rule. Similarly, the reduction of the right expression of the addition is captured in the second premise. The conclusion of the rule composes the two integers to a `NumV` term.

In the rules above `parseI` and `addI` are native operators which we provide the functionality of parsing a string into an integer, and of adding two integers, respectively. We provide the signatures for these when we [Extend specifications with native operations](#extending-specifications-with-native-operations).

```eval_rst
.. note:: Unlike with regular big-step style rules, premises in DynSem are ordered. The `Plus` rule above states that the left expression will be evaluated first and the right expression second.
```

The rules for subtraction and multiplication proceed similarly:

```dynsem
  Minus(e1, e2) --> NumV(subI(i1, i2))
  where
    e1 --> NumV(i1);
    e2 --> NumV(i2).

  Times(e1, e2) --> NumV(mulI(i1, i2))
  where
    e1 --> NumV(i1);
    e2 --> NumV(i2).
```

In all three rules seen so far (`Plus`, `Minus`, `Times`) the reductions for the subexpressions can be specified implicitly:

```dynsem
  Plus(NumV(i1), NumV(i2)) --> NumV(addI(i1, i2)).

  Minus(NumV(i1), NumV(i2)) --> NumV(subI(i1, i2)).

  Times(NumV(i1), NumV(i2)) --> NumV(mulI(i1, i2)).
```

Specifying the reductions and term expectations implicitly allows rules to be written more concisely without creating ambiguities.

```eval_rst
.. note:: Implicit reductions are applied in left-to-right order and so expand to the explicit form of the rules.
```

## Specifying context-sensitive language constructs

We define *SIMPL* language constructs whose semantics depend on the evaluation context. First we extend the syntax definition of *SIMPL* with let expressions:

```sdf3
context-free syntax
  Exp.Let = <let <ID> = <Exp> in <Exp>> {non-assoc}

  Exp.Var = <<ID>>
```

This allows expressions to be written that bind and read variables. An example of a such a program is:

```
let x = 40 in x + 2
```

We expect the program above to evaluate to `NumV(42)` and extend the semantics of *SIMPL* with the following definitions:

```dynsem
signature
  sort aliases
    Env = Map<String,V>

rules
  Env e |- Let(x, e1, e2) --> v2
  where
    Env e |- e1 --> v1;
    Env {x |--> v1} |- e2 --> v2.

  Env e |- Var(x) --> e[x].
```

The `signature` section defines an alias `Env` for an associative array. We use this associative array as the evaluation context for variables. This associative array will be pushed down in the evaluation of the tree. Looking at the first rule, it reduces `Let` terms to values by first evaluating the variable expression to a value, and then evaluating the body expression in the updated evaluation environment. The evaluation context `Env e` is passed into the reduction rules together with the `Let` expression to be reduced. The variable expression is evaluated in the same context.


Terms left of the `|-` symbol are treated in DynSem as read-only semantic components  



hiding semantics

```eval_rst
.. error:: TODO implicit propagation of the semantic components
```

```eval_rst
.. error:: not written
```

## Running an interpreter for an object language

## Extending specifications with native operations

## Writing to standard output and reading standard input

## Interacting with native data types

## Interacting with the interpreter from Java

<!-- Bookmarks -->

[1]: https://github.com/metaborg-cube/simpl
[2]: linktoSDF3
[3]: linktoLanguageReference

<!-- TODO -->
