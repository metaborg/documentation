============
Stratego API
============

.. role:: flowspec(code)
   :language: flowspec
   :class: highlight

The Stratego API to FlowSpec allows access to analysis result during and
 after analysis.

The full definition of the API can be found in the `flowspec/api
<https://github.com/metaborg/flowspec/blob/master/flowspec.lang/trans/flowspec/api.str>`__
module.

Setup
-----

Using the Stratego API requires a dependency on the FlowSpec Stratego
code (source dependency), and an import of ``flowspec/api``.

*Example.* A Stratego module importing the FlowSpec API.

.. code-block:: stratego

   module example

   imports

     flowspec/api

Editor message based on analysis
--------------------------------

Several aspects of the NaBL2 analysis process can be customized by
:ref:`implementing hooks <nabl2-custom-analysis>`_ in Stratego. 
During the so-called *final* phase, FlowSpec has run its analysis,
and this information is available to be used for creating custom
notes, warnings and errors. 

Querying analysis
-----------------

The analysis API gives access to the result of analysis. The analysis
result is available during the final custom analysis step, or in
post-analysis transformations.

The NaBL2 API defines several strategies to get an analysis term by resource
name or from an AST node :ref:`here <nabl2-get-analysis-result>`. This analysis
term can then be passed to the querying strategies that give access to the data
flow properties

Data flow properties
^^^^^^^^^^^^^^^^^^^^

.. code-block:: stratego

   /**
    * Get the property of the control flow graph node associated with
    * the given term. The value returned is the value of the property
    * _before_ the effect of the control flow graph node. 
    *
    * @param a : Analysis
    * @param prop : String
    * @type decl:Term -> Term
    */
   flowspec-get-property-pre(|a,prop)

   /**
    * Get the property of the control flow graph node associated with
    * the given term. The value returned is the value of the property
    * _after_ the effect of the control flow graph node. 
    *
    * @param a : Analysis
    * @param prop : String
    * @type decl:Term -> Term
    */
   flowspec-get-property-post(|a,prop)
