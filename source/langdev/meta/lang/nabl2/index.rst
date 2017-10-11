.. _nabl2-index:

=======================================
Static Semantics Definition with NaBL2
=======================================

Programs that are syntactically well-formed are not necessarily valid programs. 
Programming languages typically impose additional *context-sensitive* requirements on programs that cannot be captured in a syntax definition. 
Languages use names to identify reusable units that can be invoked at multiple parts in a program. 
In addition, statically typed languages require that expressions are consistently typed.
The NaBL2 'Name Binding Language' supports the specification of name binding and type checking
rules of a language. NaBL2 uses a constraint-based approach, and uses scope graphs for name resolution.

.. toctree::
   :maxdepth: 2
   :numbered: 3
   :caption: Table of Contents
   
   introduction
   reference
   stratego-api
   configuration
   examples
   bibliography
   NaBL/TS (Deprecated) <nabl>
   

.. note:: The predecessor of NaBL2, the NaBL/TS name binding and type analysis meta-language is deprecated.
