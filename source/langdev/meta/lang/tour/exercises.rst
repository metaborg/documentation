=========================
Exercises
=========================

In the previous sections you have seen all aspects of language definition with Spoofax. 
Before going out on your own and designing / implementing your own language using Spoofax, it is probably a good idea to first experiment a bit with working language implementation to get a better working understanding of the workbench.
A good way to do that is to take the existing Calc project and extend / adapt it in various ways, perhaps in the direction of your own ideas for a language.
This section provides some ideas for extending the Calc language.
Fork the project from `github <https://github.com/MetaBorgCube/metaborg-calc>`_ and make a branch. Let us know by sending us a link to your fork or by submitting a pull request for a branch and we'll add your version to the list.

For many of these exercises you will need to dive deeper into the documentation of Spoofax. 

Alternative Syntax
---------------------

Experiment with designing an alternative notation for parts of the language. Here are some ideas:

* Introduce a keyword such as ``def`` to introduce a (top-level) variable declaration

* Currently, Calc function expressions use lambda notation ``\ _._``. Try out alternatives such as Scala's ``_ => _`` notation or Javascripts ``function (_){ _ }`` notation. Can you do this without changing the abstract syntax?

Type Annotations
---------------------

Calc relies on type inference; programmers do not declare the types of variables or return types of functions. 
That is fine for a calculator language; the types are often obvious from context.
However, it is good programming practice to document the types of functions and variables.
Extend Calc with optional type annotations for variable declarations. 
When present the inferred types should correspond to the type annotations, otherwise an error should be displayed.

example::

  max : Num -> Num -> Num = \ x y . if (x > y) x else y

Type Aliases
----------------------

When type expressions become more complicated it can be useful to assign them a name

example::

   type foo = Num -> Num 
   
Rich Arithmetic
---------------------

The dynamic semantics of numbers is based on the BigDecimal Java library. Enrich the language to make better use of the library.


If-Then
--------------

Extend the language with an if-then statement `if(e1) e2`, i.e. without `else` branch. 
There are some challenges:

* The combination of the `if(e1) e2 else e3` expression with the `if(e1) e2` expression leads to the dangling else disambiguation problem. That is, how should the expression `if(e1) if(e2) e3 else e4` be parsed? Does the `else` belong to the inner or to the outer `if`? The usual convention is that the `else` belongs to the closest `if`. Can you express this in SDF3?

* Calc is a functional language. That is, the if-else form can be used as an expression that (always) yields a value. The `if` form only yields a value if the condition evaluates to `true`. Define a desugaring that transform the `if` form to the `if-else` form by producing a default value for the missing `else` branch. The challenge is that the default value depends on the type of `then` branch.

Nullary Functions
--------------------

Calc does not support n-ary functions `\ x y z . ...`, which are desugared to curried unary functions. However, nullary functions are not supported. Adapt the language definition to support nullary functions.

State
--------------------

Variables in Calc are immutable. Add mutable variables to the language.

This requires threading a store through evaluation.

Recursion
--------------------

Calc functions are currently not recursive since there is no way for a function to refer to itself. Extend the language with a `letrec` binding construct that allows recursive bindings.

Lazy Evaluation
--------------------

create your own control constructs

instead of eagerly evaluating expressions, only evaluate an expression when it is required fora computation

Lists and Tuples
-------------------

Extend the language with

Algebraic Data Types
------------------------

Extend the language with algebraic data types

Units
--------------------



Exceptions
--------------------

Calculations may go wrong. For example, division by zero does not work. Extend the language with defined exceptions (possibly raised by native operators) and a `try-catch` form to handle exceptions.


Multiplicities
---------------------

Translation to Java Bytecode
-------------------------------