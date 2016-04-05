```eval_rst
.. highlight:: str
```

# 10. Type Unifying Strategies

In [Chapter17][1] we have seen combinators for composing _type preserving_ strategies. That is, structural transformations in which basic transformation rules don't change the type of a term. Such strategies are typically applied in transformations, which change the structure of a term, but not its type. Examples are simplification and optimization. In this chapter we consider the class of _type unifying_ strategies, in which terms of different types are mapped onto one type. The application area for this type of strategy is analysis of expressions with examples such as free variables collection and call-graph extraction.

We consider the following example problems:

* _term-size_: Count the number of nodes in a term
* _occurrences_: Count number of occurrences of a subterm in a term
* _collect-vars_: Collect all variables in expression
* _free-vars_: Collect all _free_ variables in expression

These problems have in common that they reduce a structure to a single value or to a collection of derived values. The structure of the original term is usually lost.

We start with examining these problems in the context of lists, and then generalize the solutions we find there to arbitrary terms using generic term deconstruction, which allows concise implementation of generic type unifying strategies, similarly to the generic traversal strategies of [Chapter17][1].

## 10.1. Type Unifying List Transformations

We start with considering type-unifying operations on lists.

**Sum.** Reducing a list to a value can be conveniently expressed by means of a fold, which has as parameters operations for reducing the list constructors. The `foldr/2` strategy reduces a list by replacing each `Cons` by an application of `s2`, and the empty list by `s1`.

    foldr(s1, s2) =
      []; s1 <+  [y|ys] -> (y,  ys)

Thus, when applied to a list with three terms the result is

     [t1,t2,t3] => (t1, (t2, (t3,  [])))

A typical application of `foldr/2` is `sum`, which reduces a list to the sum of its elements. It sums the elements of a list of integers, using `0` for the empty list and `add` to combine the head of a list and the result of folding the tail.

    sum = foldr(!0, add)

The effect of `sum` is illustrated by the following application:

     [1,2,3] => (1, (2, (3,  []))) => 6

Note the build operator for replacing the empty list with `0`; writing `foldr(0, add)` would be wrong, since `0` by itself is a congruence operator, which basically _matches_ the subject term with the term `0` (rather than replacing it).

**Size.** The `foldr/2` strategy does not touch the elements of a list. The `foldr/3` strategy is a combination of fold and map that extends `foldr/2` with a parameter that is applied to the elements of the list.

    foldr(s1, s2, f) =
      []; s1 <+  [y|ys] -> (y, ys)

Thus, when applying it to a list with three elements, we get:

     [t1,t2,t3] => (t1, (t2, (t3,  [])))

Now we can solve our first example problem `term-size`. The size of a list is its _length_, which corresponds to the sum of the list with the elements replaced by `1`.

    length = foldr(!0, add, !1)

**Number of occurrences.** The number of occurrences in a list of terms that satisfy some predicate, entails only counting those elements in the list for which the predicate succeeds. (Where a predicate is implemented with a strategy that succeeds only for the elements in the domain of the predicate.) This follows the same pattern as counting the length of a list, but now only counting the elements for which `s` succeeds.

    list-occurrences(s) = foldr(!0, add, s < !1 + !0)

Using `list-occurrences` and a match strategy we can count the number of variables in a list:

    list-occurrences(?Var(_))

**Collect.** The next problem is to _collect_ all terms for which a strategy succeeds. We have already seen how to do this for lists. The `filter` strategy reduces a list to the elements for which its argument strategy succeeds.

    filter(s) = [] <+ [s | filter(s)] <+ ?[ |]

Collecting the variables in a list is a matter of filtering with the `?Var(_)` match.

    filter(?Var(_))

The final problem, collecting the free variables in a term, does not really have a counter part in lists, but we can mimick this if we consider having two lists; where the second list is the one with the bound variables that should be excluded.

    (filter(?Var(_)),id); diff

This collects the variables in the first list and subtracts the variables in the second list.

## 10.2. Extending Fold to Expressions

We have seen how to do typical analysis transformations on lists. How can we generalize this to arbitrary terms? The general idea of a folding operator is that it replaces the constructors of a data-type by applying a function to combine the reduced arguments of constructor applications. For example, the following definition is a sketch for a fold over abstract syntax trees:

    fold-exp(binop, assign, if, ...) = rec f(
      fold-binop(f, binop)
      <+ fold-assign(f, assign)
      <+ fold-if(f, if)
      <+ ... )

    fold-binop(f, s)  : BinOp(op, e1, e2) -> (op, e1, e2)
    fold-assign(f, s) : Assign(e1, e2)    -> (e1, e2)
    fold-if(f, s)     : If(e1, e2, e3)    -> (e1, e2, e3)

For each constructor of the data-type the fold has an argument strategy and a rule that matches applications of the constructor, which it replaces with an application of the strategy to the tuple of subterms reduced by a recursive invocation of the fold.

Instantiation of this strategy requires a rule for each constructor of the data-type. For instance, the following instantiation defines `term-size` using `fold-exp` by providing rules that sum up the sizes of the subterms and add one (`inc`) to account for the node itself.

    term-size  = fold-exp(BinOpSize, AssignSize, IfSize, ...)

    BinOpSize  : (Plus(), e1, e2) -> (e1, e2)
    AssignSize : (e1, e2)         -> (e1, e2)
    IfSize     : (e1, e2, e3)     -> (e1, (e2, e3))

This looks suspiciously like the traversal rules in [Chapter17][1]. Defining folds in this manner has several limitations. In the definition of fold, one parameter for each constructor is provided and traversal is defined explicitly for each constructor. Furthermore, in the instantiation of fold, one rule for each constructor is needed, and the default behaviour is not generically specified.

One solution would be to use the generic traversal strategy `bottomup` to deal with fold:

    fold-exp(s) = bottomup(s)

    term-size   = fold-exp(BinOpSize <+ AssignSize <+ IfSize <+ ...)

    BinOpSize   : BinOp(Plus(), e1, e2) -> (1, (e1, e2))
    AssignSize  : Assign(e1, e2)        -> (e1, e2)
    IfSize      : If(e1, e2, e3)        -> (e1, (e2, e3))

Although the recursive application to subterms is now defined generically , one still has to specify rules for the default behavior.

## 10.3. Generic Term Deconstruction

Instead of having folding rules that are specific to a data type, such as

    BinOpSize  : BinOp(op, e1, e2) -> (1, (e1, e2))
    AssignSize : Assign(e1, e2)    -> (1, (e1, e2))

we would like to have a generic definition of the form

    CSize : c(e1, e2, ...) -> (e1, (e2, ...))

This requires generic decomposition of a constructor application into its constructor and the list with children. This can be done using the `#` operator. The match strategy `?p1#(p2)` decomposes a constructor application into its constructor name and the list of direct subterms. Matching such a pattern against a term of the form `C(t1,...,tn)` results in a match of `"C"` against `p1` and a match of [`t1,...,tn]` against `p2`.

    Plus(Int("1"), Var("2"))
    stratego> ?c#(xs)
    stratego> :binding c
    variable c bound to "Plus"
    stratego> :binding xs
    variable xs bound to [Int("1"), Var("2")]

**Crush.** Using generic term deconstruction we can now generalize the type unifying operations on lists to arbitrary terms. In analogy with the generic traversal operators we need a generic one-level reduction operator. The `crush/3` strategy reduces a constructor application by folding the list of its subterms using `foldr/3`.

    crush(nul, sum, s) : c#(xs) ->  xs

Thus, `crush` performs a fold-map over the direct subterms of a term. The following application illustrates what

     C(t1, t2) => (t1, (t2, []))

The following Shell session instantiates this application in two ways:

    stratego> import libstrategolib
    stratego> !Plus(Int("1"), Var("2"))
    Plus(Int("1"),Var("2"))

    stratego> crush(id, id, id)
    (Int("1"),(Var("2"),[]))

    stratego> !Plus(Int("1"), Var("2"))
    Plus(Int("1"),Var("2"))

    stratego> crush(!Tail(), !Sum(,), !Arg())
    Sum(Arg(Int("1")),Sum(Arg(Var("2")),Tail([])))

The `crush` strategy is the tool we need to implement solutions for the example problems above.

**Size.** Counting the number of direct subterms of a term is similar to counting the number of elements of a list. The definition of `node-size` is the same as the definition of `length`, except that it uses `crush` instead of `foldr`:

    node-size = crush(!0, add, !1)

Counting the number of subterms (nodes) in a term is a similar problem. But, instead of counting each direct subterm as 1, we need to count _its_ subterms.

    term-size = crush(!1, add, term-size)

The `term-size` strategy achieves this simply with a recursive call to itself.

    stratego>  Plus(Int("1"), Var("2"))
    2
    stratego>  Plus(Int("1"), Var("2"))
    5

**Occurrences.** Counting the number of occurrences of a certain term in another term, or more generally, counting the number of subterms that satisfy some predicate is similar to counting the term size. However, only those terms satisfying the predicate should be counted. The solution is again similar to the solution for lists, but now using `crush`.

    om-occurrences(s) = s < !1 + crush(!0, add, om-occurrences(s))

The `om-occurrences` strategy counts the _outermost_ subterms satisfying `s`. That is, the strategy stops counting as soon as it finds a subterm for which `s` succeeds.

The following strategy counts _all_ occurrences:

    occurrences(s) = (, )

It counts the current term if it satisfies `s` and adds that to the occurrences in the subterms.

    stratego>  Plus(Int("1"), Plus(Int("34"), Var("2")))
    2
    stratego>  Plus(Int("1"), Plus(Int("34"), Var("2")))
    1
    stratego>  Plus(Int("1"), Plus(Int("34"), Var("2")))
    2

**Collect.** _Collecting_ the subterms that satisfy a predicate is similar to counting, but now a _list_ of subterms is produced. The `collect(s)` strategy collects all _outermost_ occurrences satisfying `s`.

    collect(s) = ![] <+ crush(![], union, collect(s))

When encountering a subterm for which `s` succeeds, a singleton list is produced. For other terms, the matching subterms are collected for each direct subterm, and the resulting lists are combined with `union` to remove duplicates.

A typical application of `collect` is the collection of all variables in an expression, which can be defined as follows:

    get-vars = collect(?Var(_))

Applying `get-vars` to an expression AST produces the list of all subterms matching `Var(_)`.

The `collect-all(s)` strategy collects _all_ occurrences satisfying `s`.

    collect-all(s) =
      ![ | ] <+ crush(![], union, collect(s))

If `s` succeeds for the subject term combines the subject term with the collected terms from the subterms.

**Free Variables.** Collecting the variables in an expression is easy, as we saw above. However, when dealing with languages with variable bindings, a common operation is to extract only the _free_ variables in an expression or block of statements. That is, the occurrences of variables that are not bound by a variable declaration. For example, in the expression

    x + let var y := x + 1 in f(y, a + x + b) end

the free variables are `{x, a, b}`, but not `y`, since it is bound by the declaration in the let. Similarly, in the function definition

    function f(x : int) = let var y := h(x) in x + g(z) * y end

the only free variable is `z` since `x` and `y` are declared.

Here is a free variable extraction strategy for Tiger expressions. It follows a similar pattern of mixing generic and data-type specific operations as we saw in [Chapter17][1]. The `crush` alternative takes care of the non-special constructors, while `ExpVars` and `FreeVars` deal with the special cases, i.e. variables and variable binding constructs:

    free-vars =
      ExpVars
      <+ FreeVars(free-vars)
      <+ crush(![], union, free-vars)

    ExpVars :
      Var(x) -> [x]

    FreeVars(fv) :
      Let([VarDec(x, t, e1)], e2) -> ( e1, ( e2, [x]))

    FreeVars(fv) :
      Let([FunctionDec(fdecs)], e2) -> (( fdecs, e2), fs)
      where ,_,_,_))> fdecs => fs

    FreeVars(fv) :
      FunDec(f, xs, t, e) -> (e, xs)
      where  xs => xs

The `FreeVars` rules for binding constructs use their `fv` parameter to recursively get the free variables from subterms, and they subtract the bound variables from any free variables found using `diff`.

We can even capture the pattern exhibited here in a generic collection algorithm with support for special cases:

    collect-exc(base, special : (a -> b) * a -> b) =
      base
      <+ special(collect-exc(base, special))
      <+ crush(![], union, collect-exc(base, special))

The `special` parameter is a strategy parameterized with a recursive call to the collection strategy. The original definition of `free-vars` above, can now be replaced with

    free-vars = collect-exc(ExpVars, FreeVars)

## 10.4. Generic Term Construction

It can also be useful to _construct_ terms generically. For example, in parse tree implosion, application nodes should be reduced to constructor applications. Hence build operators can also use the `#` operator. In a strategy `!p1#(p2)`, the current subject term is replaced by a constructor application, where the constructor name is provided by `p1` and the list of subterms by `p2`. So, if `p1` evaluates to `"C"` and `p2` evaluates to [`t1,...,tn]`, the expression `!p1#(p2)` build the term `C(t1,...,tn)`.

**Imploding Parse Trees.** A typical application of generic term construction is the implosion of parse trees to abstract syntax trees performed by [implode-asfix][2]. Parse trees produced by [sglr][3] have the form:

    appl(prod(sorts, sort, attrs([cons("C")])),[t1,...,tn])

That is, a node in a parse tree consists of an encoding of the original production from the syntax definition, and a list with subtrees. The production includes a constructor annotation `cons("C")` with the name of the abstract syntax tree constructor. Such a tree node should be imploded to an abstract syntax tree node of the form `C(t1,...,tn)`. Thus, this requires the construction of a term with constructor `C` given the string with its name. The following implosion strategy achieves this using generic term construction:

    implode = appl(id, map(implode)); Implode
    Implode : appl(prod(sorts, sort, attrs([cons(c)])), ts) -> c#(ts)

The `Implode` rule rewrites an `appl` term to a constructor application, by extracting the constructor name from the production and then using generic term construction to apply the constructor.

Note that this is a gross over simplification of the actual implementation of [implode-asfix][2]. See the source code for the full strategy.

Generic term construction and deconstruction support the definition of generic analysis and generic translation problems. The generic solutions for the example problems term size, number of occurrences, and subterm collection demonstrate the general approach to solving these types of problems.

[1]: stratego-traversal-strategies.html "Chapter"
[2]: ref-implode-asfix.html "implode-asfix"
[3]: ref-sglr.html "sglr"
