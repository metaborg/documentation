.. _statix-index:

=======================================
Static Semantics Definition with Statix
=======================================

Programs that are syntactically well-formed are not necessarily valid programs. 
Programming languages typically impose additional *context-sensitive* requirements on programs that cannot be captured in a syntax definition. 
Languages use names to identify reusable units that can be invoked at multiple parts in a program. 
In addition, statically typed languages require that expressions are consistently typed.
The Statix language supports the specification of name binding and type checking
rules of a language. The rules of the static semantics are written as logic rules, and solved using a constraint-based approach, and uses scope graphs for name resolution.

.. warning:: Statix is still considered experimental.

.. toctree::
   :maxdepth: 2
   :numbered: 3
   :caption: Table of Contents
   
   usage
   reference
   stratego-api

