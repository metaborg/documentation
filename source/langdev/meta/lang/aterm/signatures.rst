.. highlight:: sdf3

==================
Signatures
==================

The ATerm format does not restrict terms

describing terms schemas with signatures



Stratego Signatures
------------------------

Sort
  a type of terms
  
Constructor declaration
  name and types of arguments::
  
    C : S1 * ... * Sn -> S0

To use terms in Stratego programs, their constructors should be declared in a signature. A signature declares a number of sorts and a number of constructors for these sorts. For each constructor, a signature declares the number and types of its arguments. For example, the following signature declares some typical constructors for constructing abstract syntax trees of expressions in a programming language::

    module Expressions-sig
    imports Common
    signature
      sorts Exp
      constructors
        Var    : ID -> Exp
        Int    : INT -> Exp
        Plus   : Exp * Exp -> Exp
        Mul    : Exp * Exp -> Exp
        Call   : ID  * List(Exp) -> Exp

Currently, the Stratego compiler only checks the arity of constructor applications against the signature. Still, it is considered good style to also declare the types of constructors in a sensible manner for the purpose of documentation. Also, a later version of the language may introduce type checking.



SDF3 Syntax Definitions
----------------------------

signature derived from syntax definition

for example::

   module Expressions
   imports Common
   sorts Exp
   context-free syntax
     Exp.Var  = <<ID>>
     Exp.Int  = <<INT>>
     Exp.Plus = <<Exp> + <Exp>> {left}
     Exp.Mul  = <<Exp> * <Exp>> {left}
     Exp.Call = <<ID>(<{Exp ","}*>)>
   context-free priorities
     Exp.Mul > Exp.Plus