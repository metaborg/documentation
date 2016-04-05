```eval_rst
.. highlight:: str
```

# 12. Dynamic Rules

In the previous chapters we have shown how programmable rewriting strategies can provide control over the application of transformation rules, thus addressing the problems of confluence and termination of rewrite systems. Another problem of pure rewriting is the context-free nature of rewrite rules. A rule has access only to the term it is transforming. However, transformation problems are often context-sensitive. For example, when inlining a function at a call site, the call is replaced by the body of the function in which the actual parameters have been substituted for the formal parameters. This requires that the formal parameters and the body of the function are known at the call site, but these are only available higher-up in the syntax tree. There are many similar problems in program transformation, including bound variable renaming, typechecking, data flow transformations such as constant propagation, common-subexpression elimination, and dead code elimination. Although the basic transformations in all these applications can be expressed by means of rewrite rules, these require contextual information.

In Stratego context-sensitive rewriting can be achieved without the added complexity of local traversals and without complex data structures, by the extension of rewriting strategies with scoped dynamic rewrite rules. Dynamic rules are otherwise normal rewrite rules that are defined at run-time and that inherit information from their definition context. As an example, consider the following strategy definition as part of an inlining transformation:

    DefineUnfoldCall =
      ?|[ function f(x) = e1 ]|
      ; rules(
          UnfoldCall : |[ f(e2 ) ]| -> |[ let var x := e2 in e1 end ]|
        )

The strategy `DefineUnfoldCall` matches a function definition and defines the rewrite rule `UnfoldCall`, which rewrites a call to the specific function f , as encountered in the definition, to a let expression binding the formal parameter `x` to the actual parameter `e2` in the body of the function `e1` . Note that the variables `f`, `x` , and `e1` are bound in the definition context of `UnfoldCall`. The `UnfoldCall` rule thus defined at the function definition site, can be used at all function call sites. The storage and retrieval of the context information is handled transparently by the underlying language implementation and is of no concern to the programmer.

An overview with semantics and examples of dynamic rewrite rules in Stratego is available in the following publications:

* M. Bravenboer, A. van Dam, K. Olmos, and E. Visser. Program Transformation with Scoped Dynamic Rewrite Rules. Fundamenta Informaticae, 69:1--56, 2005.

An extended version is available as [technical report UU-CS-2005-005](http://www.cs.uu.nl/research/techreps/UU-CS-2005-005.html).

* K. Olmos and E. Visser. Composing Source-to-Source Data-Flow Transformations with Rewriting Strategies and Dependent Dynamic Rewrite Rules. In R. Bodik, editor, 14th International Conference on Compiler Construction (CC'05), volume 3443 of Lecture Notes in Computer Science, pages 204--220. Springer-Verlag, April 2005.

An extended version is available as [technical report UU-CS-2005-006](http://www.cs.uu.nl/research/techreps/UU-CS-2005-006.html)

Since these publications provide a fairly complete and up-to-date picture of dynamic rules, incorporation into this manual is not as urgent as other parts of the language.
