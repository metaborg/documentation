.. _stratego-index:

=====================================
Transformation with Stratego 
=====================================

Parsing a program text results in an abstract syntax tree. Stratego is a language for defining transformations on such trees. Stratego provides a term notation to construct and deconstruct trees and uses *term rewriting* to define transformations. Instead of applying all rewrite rules to all sub-terms, Stratego supports programmable *rewriting strategies* that control the application of rewrite rules.

.. toctree::
   :maxdepth: 1

   01-introduction
   02-terms
   03-running-stratego-programs
   04-term-rewriting
   05-rewriting-strategies
   06-rules-and-strategies
   07-strategy-combinators
   08-creating-and-analyzing-terms
   09-traversal-strategies
   10-type-unifying-strategies
   11-concrete-object-syntax
   12-dynamic-rules
   lib/index