.. _stratego-index:

=====================================
Transformation with Stratego
=====================================

Parsing a program text results in an abstract syntax tree. Stratego is a language for defining transformations on such trees. Stratego provides a term notation to construct and deconstruct trees and uses *term rewriting* to define transformations. Instead of applying all rewrite rules to all sub-terms, Stratego supports programmable *rewriting strategies* that control the application of rewrite rules.

.. toctree::
   :maxdepth: 1

   strategoxt/index
   lib/index
   concrete-syntax

..   stratego.rst
