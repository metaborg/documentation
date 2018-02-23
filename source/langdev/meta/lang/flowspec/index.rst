.. _flowspec-index:

===========================================
Data Flow Analysis Definition with FlowSpec
===========================================

Programs that are syntactically well-formed are not necessarily valid programs. 
Programming languages typically impose additional *context-sensitive* requirements on programs that cannot be captured in a syntax definition. 
Languages use data and control flow to check certain extra properties that fall outside of names and type systems. 
The FlowSpec 'Flow Analysis Specification Language' supports the specification of rules to define the static control flow of a language, and data flow analysis on over that control flow.
FlowSpec supports flow-sensitive intra-procedural data flow analysis. 

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
