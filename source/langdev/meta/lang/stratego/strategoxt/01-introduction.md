```eval_rst
.. highlight:: str
```

# 1. Introduction

Program transformation is the mechanical manipulation of a program in order to improve it relative to some cost function ``$ C $``, such that ``$ C(P) > C(tr(P)) $``, i.e., the cost decreases as a result of applying the transformation. The cost of a program can be measured in different dimensions such as performance, memory usage, understandability, flexibility, maintainability, portability, correctness, or satisfaction of requirements. Related to these goals, program transformations are applied in different settings; e.g. compiler optimizations improve performance and refactoring tools aim at improving understandability.

While transformations can be achieved by manual manipulation of programs, in general, the aim of program transformation is to increase programmer productivity by automating programming tasks, thus enabling programming at a higher-level of abstraction, and increasing maintainability and re-usability of programs. Automatic application of program transformations requires their implementation in a programming language. In order to make the implementation of transformations productive, such a programming language should support abstractions for the domain of program transformation.

Stratego is a language designed for this purpose. It is a language based on the paradigm of rewriting with programmable rewriting strategies and dynamic rules.


## 1.1. Transformation by Rewriting

Term rewriting is an attractive formalism for expressing basic program transformations. A rewrite rule `p1 -> p2` expresses that a program fragment matching the left-hand side pattern `p1` can be replaced by the instantiation of the right-hand side pattern `p2`. For instance, the rewrite rule

    |[ i + j ]| -> |[ k ]| where (i, j) => k

expresses constant folding for addition, i.e., replacing an addition of two constants by their sum. Similarly, the rule

    |[ if 0 then e1 else e2 ]| -> |[ e2 ]|

defines unreachable code elimination by reducing a conditional statement to its right branch since the left branch can never be executed. Thus, rewrite rules can directly express laws derived from the semantics of the programming language, making the verification of their correctness straightforward. A correct rule can be safely applied anywhere in a program. A set of rewrite rules can be directly operationalized by rewriting to normal form, i.e. exhaustive application of the rules to a term representing a program. If the rules are confluent and terminating, the order in which they are applied is irrelevant.


## 1.2. Limitations of Pure Rewriting

However, there are two limitations to the application of standard term rewriting techniques to program transformation: the need to intertwine rules and strategies in order to control the application of rewrite rules and the context-free nature of rewrite rules.


## 1.3. Transformation Strategies

Exhaustive application of all rules to the entire abstract syntax tree of a program is not adequate for most transformation problems. The system of rewrite rules expressing basic transformations is often non-confluent and/or non-terminating. An ad hoc solution that is often used is to encode control over the application of rules into the rules themselves by introducing additional function symbols. This intertwining of rules and strategies obscures the underlying program equalities, incurs a programming penalty in the form of rules that define a traversal through the abstract syntax tree, and disables the reuse of rules in different transformations.

Stratego solves the problem of control over the application of rules while maintaining the separation of rules and strategies. A strategy is a little program that makes a selection from the available rules and defines the order and position in the tree for applying the rules. Thus rules remain pure, are not intertwined with the strategy, and can be reused in multiple transformations.


## 1.4. Context-Sensitive Transformation

The second problem of rewriting is the context-free nature of rewrite rules. A rule has access only to the term it is transforming. However, transformation problems are often context-sensitive. For example, when inlining a function at a call site, the call is replaced by the body of the function in which the actual parameters have been substituted for the formal parameters. This requires that the formal parameters and the body of the function are known at the call site, but these are only available higher-up in the syntax tree. There are many similar problems in program transformation, including bound variable renaming, typechecking, data flow transformations such as constant propagation, common-subexpression elimination, and dead code elimination. Although the basic transformations in all these applications can be expressed by means of rewrite rules, these require contextual information.



The following chapters give a tutorial for the Stratego language in which these ideas are explained and illustrated.
