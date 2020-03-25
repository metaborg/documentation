```eval_rst
.. highlight:: str
```

# 7. Strategy Combinators

We have seen the use of strategies to combine rules into complex transformations. Rather than providing a fixed set of high-level strategy operators such as `bottomup`, `topdown`, and `innermost`, Stratego provides a small set of basic combinators, that can be used to create a wide variety of strategies. In [Chapter 7][1] until [Chapter 10][2] we will introduce these combinators. In this chapter we start with a set of combinators for sequential composition and choice of strategies.

## 7.1. Identity and Failure

The most basic operations in Stratego are `id` and `fail`. The identity strategy `id` always succeeds and behaves as the identity function on terms. The failure strategy `fail` always fails. The operations have no side effects.

    stratego> !Foo(Bar())
    Foo(Bar)
    stratego> id
    Foo(Bar)
    stratego> fail
    command failed

## 7.2. Sequential composition

The sequential composition `s1 ; s2` of the strategies `s1` and `s2` first applies the strategy `s1` to the subject term and then `s2` to the result of that first application. The strategy fails if either `s1` or `s2` fails.

**Properties.** Sequential composition is associative. Identity is a left and right unit for sequential composition; since `id` always succeeds and leaves the term alone, it has no additional effect to the strategy that it is composed with. Failure is a left zero for sequential composition; since `fail` always fails the next strategy will never be reached.

    (s1; s2) ; s3 = s1; (s2; s3)

    id; s = s

    s; id = s

    fail; s = fail

However, not for all strategies `s` we have that failure is a right zero for sequential composition:

    s ; fail = fail   (is not a law)

Although the composition `s; fail` will always fail, the execution of `s` may have side effects that are not performed by `fail`. For example, consider printing a term in `s`.

**Examples.** As an example of the use of sequential composition consider the following rewrite rules.

    stratego> A : P(Z(),x) -> x
    stratego> B : P(S(x),y) -> P(x,S(y))

The following session shows the effect of first applying `B` and then `A`:

    stratego> !P(S(Z()), Z())
    P(S(Z),Z)
    stratego> B
    P(Z,S(Z))
    stratego> A
    S(Z)

Using the sequential composition of the two rules, this effect can be achieved 'in one step':

    stratego> !P(S(Z()),Z())
    P(S(Z),Z)
    stratego> B; A
    S(Z)

The following session shows that the application of a composition fails if the second strategy in the composition fails to apply to the result of the first:

    stratego> !P(S(Z()),Z())
    P(S(Z),Z)
    stratego> B; B
    command failed

Choosing between rules to apply is achieved using one of several _choice_ combinators, all of which are based on the guarded choice combinator. The common approach is that failure to apply one strategy leads to backtracking to an alternative strategy.

### Deterministic Choice (Left Choice)

The left choice or deterministic choice `s1 <+ s2` tries to apply `s1` and `s2` in that order. That is, it first tries to apply `s1`, and if that succeeds the choice succeeds. However, if the application of `s1` fails, `s2` is applied to _the original term_.

**Properties.** Left choice is associative. Identity is a left zero for left choice; since `id` always succeeds, the alternative strategy will never be tried. Failure is a left and right unit for left choice; since `fail` always fails, the choice will always backtrack to the alternative strategy, and use of `fail` as alternative strategy is pointless.

    (s1 <+ s2) <+ s3 = s1 <+ (s2 <+ s3)

    id <+ s  = id

    fail <+ s = s

    s <+ fail = s

However, identity is not a right zero for left choice. That is, not for all strategies `s` we have that

    s <+ id =  s    (is not a law)

The expression `s <+ id` always succeeds, even (especially) in the case that `s` fails, in which case the right-hand side of the equation fails of course.

**Local Backtracking.** The left choice combinator is a _local backtracking_ combinator. That is, the choice is committed once the left-hand side strategy has succeeded, even if the continuation strategy fails. This is expressed by the fact that the property

    (s1 <+ s2); s3 = (s1; s3) <+ (s2; s3)    (is not a law)

does _not_ hold for all `s1`, `s2`, and `s3`. The difference is illustrated by the following applications:

    stratego> !P(S(Z()),Z())
    P(S(Z),Z)
    stratego> (B <+ id); B
    command failed

    stratego> !P(S(Z()),Z())
    P(S(Z),Z)
    stratego> (B <+ id)
    P(Z,S(Z))
    stratego> B
    command failed

    stratego> (B; B) <+ (id; B)
    P(Z,S(Z))

In the application of `(B <+ id); B`, the first application of `B` succeeds after which the choice is committed. The subsequent application of `B` then fails. This equivalent to first applying `(B <+ id)` and then applying `B` to the result. The application of `(B; B) <+ (id; B)`, however, is successful; the application of `B; B` fails, after which the choice backtracks to `id; B`, which succeeds.

**Choosing between Transformations.** The typical use of left choice is to create a composite strategy trying one from several possible transformations. If the strategies that are composed are mutually exclusive, that is, don't succeed for the same terms, their sum is a transformation that (deterministically) covers a larger set of terms. For example, consider the following two rewrite rules:

    stratego> PlusAssoc : Plus(Plus(e1, e2), e3) -> Plus(e1, Plus(e2, e3))
    stratego> PlusZero  : Plus(Int("0"),e) -> e

These rules are mutually exclusive, since there is no term that matches the left-hand sides of both rules. Combining the rules with left choice into `PlusAssoc <+ PlusZero` creates a strategy that transforms terms matching both rules as illustrated by the following applications:

    stratego> !Plus(Int("0"),Int("3"))
    Plus(Int("0"),Int("3"))

    stratego> PlusAssoc
    command failed
    stratego> PlusAssoc <+ PlusZero
    Int("3")

    stratego> !Plus(Plus(Var("x"),Int("42")),Int("3"))
    Plus(Plus(Var("x"),Int("42")),Int("3"))

    stratego> PlusZero
    command failed
    stratego> PlusAssoc <+ PlusZero
    Plus(Var("x"),Plus(Int("42"),Int("3")))

**Ordering Overlapping Rules.** When two rules or strategies are mutually exlusive the order of applying them does not matter. In cases where strategies are overlapping, that is, succeed for the same terms, the order becomes crucial to determining the semantics of the composition. For example, consider the following rewrite rules reducing applications of `Mem`:

    stratego> Mem1 : Mem(x,[]) -> False()
    stratego> Mem2 : Mem(x,[x|xs]) -> True()
    stratego> Mem3 : Mem(x,[y|ys]) -> Mem(x,ys)

Rules `Mem2` and `Mem3` have overlapping left-hand sides. Rule `Mem2` only applies if the first argument is equal to the head element of the list in the second argument. Rule `Mem3` applies always if the list in the second argument is non-empty.

    stratego> !Mem(1, [1,2,3])
    Mem(1, [1,2,3])
    stratego> Mem2
    True
    stratego> !Mem(1, [1,2,3])
    Mem(1,[1,2,3])
    stratego> Mem3
    Mem(1,[2,3])

In such situations, depending on the order of the rules, different results are produced. (The rules form a non-confluent rewriting system.) By ordering the rules as `Mem2 <\+ Mem3`, rule `Mem2` is tried before `Mem3`, and we have a deterministic transformation strategy.

**Try**: A useful application of `<+` in combination with `id` is the reflexive closure of a strategy `s`:

    try(s) = s <+ id

The user-defined strategy combinator `try` tries to apply its argument strategy `s`, but if that fails, just succeeds using `id`.

Sometimes it is not desirable to backtrack to the alternative specified in a choice. Rather, after passing a _guard_, the choice should be committed. This can be expressed using the _guarded left choice_ operator `s1 < s2 + s3`. If `s1` succeeds `s2` is applied, else `s3` is applied. If `s2` fails, the complete expression fails; no backtracking to `s3` takes place.

**Properties.** This combinator is a generalization of the left choice combinator `<+`.

    s1 <+ s2 = s1 < id + s2

The following laws make clear that the 'branches' of the choice are selected by the success or failure of the guard:

    id < s2 + s3  = s2

    fail < s2 + s3 = s3

If the right branch always fails, the construct reduces to the sequential composition of the guard and the left branch.

    s1 < s2 + fail = s1; s2

Guarded choice is not associative:

    (s1 < s2 + s3) < s4 + s5 = s1 < s2 + (s3 < s4 + s5)    (not a law)

To see why consider the possible traces of these expressions. For example, when `s1` and `s2` succeed subsequently, the left-hand side expression calls `s4`, while the right-hand side expression does not.

However, sequential composition distributes over guarded choice from left _and_ right:

    (s1 < s2 + s3); s4 = s1 < (s2; s4) + (s3; s4)

    s0; (s1 < s2 + s3) = (s0; s1) < s2 + s3

**Examples.** The guarded left choice operator is most useful for the implementation of higher-level control-flow strategies. For example, the _negation_ `not(s)` of a strategy `s`, succeeds if `s` fails, and fails when it succeeds:

    not(s) = s < fail + id

Since failure discards the effect of a (successful) transformation, this has the effect of testing whether `s` succeeds. So we have the following laws for `not`:

    not(id) = fail
    not(fail) = id

However, side effects performed by `s` are not undone, of course. Therefore, the following equation does _not_ hold:

    not(not(s)) = s   (not a law)

Another example of the use of guarded choice is the `restore-always` combinator:

    restore-always(s, r) = s < r + (r; fail)

It applies a 'restore' strategy `r` after applying a strategy `s`, even if `s` fails, and preserves the success/failure behavior of `s`. Since `fail` discards the transformation effect of `r`, this is mostly useful for ensuring that some side-effecting operation is done (or undone) after applying `s`.

For other applications of guarded choice, Stratego provides syntactic sugar.

The guarded choice combinator is similar to the traditional if-then-else construct of programming languages. The difference is that the 'then' branch applies to the result of the application of the condition. Stratego's `if s1 then s2 else s3 end` construct is more like the traditional construct since both branches apply to the original term. The condition strategy is only used to test if it succeeds or fails, but it's transformation effect is undone. However, the condition strategy `s1` is still applied to the current term. The `if s1 then s2 end` strategy is similar; if the condition fails, the strategy succeeds.

**Properties.** The `if-then-else-end` strategy is just syntactic sugar for a combination of guarded choice and the `where` combinator:

    if s1 then s2 else s3 end  =  where(s1) < s2 + s3

The strategy `where(s)` succeeds if `s` succeeds, but returns the original subject term. The implementation of the `where` combinator will be discussed in [Chapter 8][3]. The following laws show that the branches are selected by success or failure of the condition:

    if id   then s2 else s3 end  =  s2

    if fail then s2 else s3 end  =  s3

The `if-then-end` strategy is an abbreviation for the `if-then-else-end` with the identity strategy as right branch:

    if s1 then s2 end  =  where(s1) < s2 + id

**Examples.** The _inclusive or_ `or(s1, s2)` succeeds if one of the strategies `s1` or `s2` succeeds, but guarantees that both are applied, in the order `s1` first, then `s2`:

    or(s1, s2) =
      if s1 then try(where(s2)) else where(s2) end

This ensures that any side effects are always performed, in contrast to `s1 <\+ s2`, where `s2` is only executed if `s1` fails. (Thus, left choice implements a short circuit Boolean or.)

Similarly, the following `and(s1, s2)` combinator is the non-short circuit version of Boolean conjunction:

    and(s1, s2) =
      if s1 then where(s2) else where(s2); fail end

The `switch` construct is an n-ary branching construct similar to its counter parts in other programming languages. It is defined in terms of guarded choice. The `switch` construct has the following form:

      switch s0
        case s1 : s1'
        case s2 : s2'
        ...
        otherwise : sdef
      end

The switch first applies the `s0` strategy to the current term `t` resulting in a term `t'`. Then it tries the cases in turn applying each `si` to `t'`. As soon as this succeeds the corresponding case is selected and `si'` is applied to the `t`, the term to which the switch was applied. If none of the cases applies, the default strategy `sdef` from the `otherwise` is applied.

**Properties.** The switch construct is syntactic sugar for a nested if-then-else:

    {x : where(s0 => x);
        if <s1> x
        then s1'
        else if <s2> x
            then s2'
            else if ...
                then ...
                else sdef
                end
            end
        end}

This translation uses a couple of Stratego constructs that we haven't discussed so far.

**Examples.** TODO

## 7.3. Non-deterministic Choice

The deterministic left choice operator prescribes that the left alternative should be tried before the right alternative, and that the latter is only used if the first fails. There are applications where it is not necessary to define the order of the alternatives. In those cases non-deterministic choice can be used.

The non-deterministic choice operator `s1 + s2` chooses one of the two strategies `s1` or `s2` to apply, such that the one it chooses succeeds. If both strategies fail, then the choice fails as well. Operationally the choice operator first tries one strategy, and, if that fails, tries the other. The order in which this is done is undefined, i.e., arbitrarily chosen by the compiler.

The `+` combinator is used to model modular composition of rewrite rules and strategies with the same name. Multiple definitions with the same name, are merged into a single definition with that name, where the bodies are composed with `+`. The following transformation illustrates this:

      f = s1  f = s2      ==>    f = s1 + s2

This transformation is somewhat simplified; the complete transformation needs to take care of local variables and parameters.

While the `+` combinator is used internally by the compiler for this purpose, programmers are advised _not_ to use this combinator, but rather use the left choice combinator `<+` to avoid surprises.

Repeated application of a strategy can be achieved with recursion. There are two styles for doing this; with a recursive definition or using the fixpoint operator `rec`. A recursive definition is a normal strategy definition with a recursive call in its body.

    f(s) = ... f(s) ...

Another way to define recursion is using the fixpoint operator `rec x(s)`, which recurses on applications of `x` within `s`. For example, the definition

    f(s) = rec x(... x ...)

is equivalent to the one above. The advantage of the `rec` operator is that it allows the definition of an unnamed strategy expression to be recursive. For example, in the definition

    g(s) = foo; rec x(... x ...); bar

the strategy between `foo` and `bar` is a recursive strategy that does _not_ recurse to `g(s)`.

Originally, the `rec` operator was the only way to define recursive strategies. It is still in the language in the first place because it is widely used in many existing programs, and in the second place because it can be a concise expression of a recursive strategy, since call parameters are not included in the call. Furthermore, all free variables remain in scope.

**Examples.** The `repeat` strategy applies a transformation `s` until it fails. It is defined as a recursive definition using `try` as follows:

    try(s)    = s <+ id
    repeat(s) = try(s; repeat(s))

An equivalent definition using `rec` is:

    repeat(s) = rec x(try(s; x))

The following Stratego Shell session illustrates how it works. We first define the strategies:

    stratego> try(s) = s <+ id
    stratego> repeat(s) = try(s; repeat(s))
    stratego> A : P(Z(),x) -> x
    stratego> B : P(S(x),y) -> P(x,S(y))

Then we observe that the repeated application of the individual rules `A` and `B` reduces terms:

    stratego> !P(S(Z()),Z())
    P(S(Z),Z)
    stratego> B
    P(Z,S(Z))
    stratego> A
    S(Z)

We can automate this using the `repeat` strategy, which will repeat the rules as often as possible:

    stratego> !P(S(Z()),Z())
    P(S(Z),Z)
    stratego> repeat(A <+ B)
    S(Z)

    stratego> !P(S(S(S(Z()))),Z())
    P(S(S(S(Z))),Z)
    stratego> repeat(A <+ B)
    S(S(S(Z)))

To illustrate the intermediate steps of the transformation we can use `debug` from the Stratego Library.

    stratego> import libstratego-lib
    stratego> !P(S(S(S(Z()))),Z())
    P(S(S(S(Z))),Z)
    stratego> repeat(debug; (A <+ B))
    P(S(S(S(Z))),Z)
    P(S(S(Z)),S(Z))
    P(S(Z),S(S(Z)))
    P(Z,S(S(S(Z))))
    S(S(S(Z)))
    S(S(S(Z)))

**A Library of Iteration Strategies.** Using sequential composition, choice, and recursion a large variety of iteration strategies can be defined. The following definitions are part of the Stratego Library (in module `strategy/iteration`).

    repeat(s) =
      rec x(try(s; x))

    repeat(s, c) =
      (s; repeat(s, c)) <+ c

    repeat1(s, c) =
      s; (repeat1(s, c) <+ c)

    repeat1(s) =
      repeat1(s, id)

    repeat-until(s, c) =
      s; if c then id else repeat-until(s, c) end

    while(c, s) =
      if c then s; while(c, s) end

    do-while(s, c) =
      s; if c then do-while(s, c) end

The following equations describe some relations between these strategies:

    do-while(s, c) = repeat-until(s, not(c))

    do-while(s, c) = s; while(c, s)

[1]: 07-strategy-combinators.md "Strategy Combinators"
[2]: 10-type-unifying-strategies.md "Type Unifying Strategies"
[3]: 08-creating-and-analyzing-terms.md "Creating and Analyzing Terms"
