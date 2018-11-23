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

Running the analysis
--------------------

There are strategies to integrate FlowSpec analysis in the NaBL2 analysis, and strategies for doing both NaBL2 analysis and FlowSpec analysis on an AST. 

Integrated into NaBL2 analysis
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

These can be used in the final phase of the NaBL2 analysis process using the :ref:`Stratego hooks <nabl2-custom-analysis>`. 

.. code-block:: stratego

    /**
     * Analyze the given AST with FlowSpec.
     * The FlowSpec analysis is added to given NaBL2 analysis result and returned.
     *
     * @param analysis:Analysis
     * @param propnames:String or List(String)
     * @type ast:Term -> Analysis
     */
    flowspec-analyze(|analysis)

    /**
     * Analyze the given AST with FlowSpec, but only the given FlowSpec properties.
     * The FlowSpec analysis is added to given NaBL2 analysis result and returned.
     *
     * @param analysis:Analysis
     * @param propnames:String or List(String)
     * @type ast:Term -> Analysis
     */
    flowspec-analyze(|analysis, propnames)

The analysis results are also usable at that point for generating editor messages. Integration with NaBL2 is done by giving the FlowSpec analysis result as the "custom final analysis result":

.. code-block:: stratego

    nabl2-custom-analysis-unit-hook(|a):
        (resource, ast, custom-initial-result) -> (resource, ast)

    nabl2-custom-analysis-final-hook(|a):
        (resource, custom-initial-result, custom-unit-results) -> (errors, warnings, notes, custom-final-result)
      with asts     := <map(\(ast-resource, ast) -> <nabl2--index-ast(|ast-resource)> ast\)> custom-unit-results ; // workaround for https://yellowgrass.org/issue/NaBL2/54
           custom-final-result := <flowspec-analyze(|a)> asts ;
           errors   := ... ;
           warnings := ... ;
           notes    := ...

This propagates the AST of each unit from the unit phase, and analyzes all of them together in the final phase. The ``custom-final-result`` is returned so that NaBL2 preserves it for later usage. FlowSpec provides convenience functions that request the custom final result again later:

.. code-block:: stratego

    /**
     * Get analysis for the given AST node. Includes flowspec analysis if custom final hook is set up
     *  correctly.
     *
     * @type node:Term -> Analysis
     */
    flowspec-get-ast-analysis

    /**
     * Get analysis for the given resource. Includes flowspec analysis if custom final hook is set up
     *  correctly.
     *
     * @type filename:String -> Analysis
     */
    flowspec-get-resource-analysis

Running the analysis manually
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Sometimes you need data-flow analysis between transformations which change the program. That means you need to run the analysis just before a transformation to have analysis results corresponding to the current program. 

The following strategies execute the analysis and help with consuming the resulting tuple. 

.. code-block:: stratego

    /**
     * Analyze the given AST with NaBL2 and FlowSpec
     *
     * @param resource:String
     * @type ast:Term -> (ast:Term, Analysis, errors:List(EditorMessage), warnings:List(EditorMessage), notes:List(EditorMessage))
     */
    flowspec-analyze-ast(|resource)

    /**
     * Analyze the given AST with NaBL2 and FlowSpec.
     * Transform the AST with pre before the FlowSpec analysis, and with post after the FlowSpec analysis.
     *
     * @param pre:Term -> Term
     * @param post:Term -> Term
     * @param resource:String
     * @type ast:Term -> (ast:Term, Analysis, errors:List(EditorMessage), warnings:List(EditorMessage), notes:List(EditorMessage))
     */
    flowspec-analyze-ast(pre,post|resource)

    /**
     * Analyze the given AST with NaBL2 and FlowSpec, but only the given FlowSpec properties.
     *
     * @param resource:String
     * @param propnames:String or List(String)
     * @type ast:Term -> (ast:Term, Analysis, errors:List(EditorMessage), warnings:List(EditorMessage), notes:List(EditorMessage))
     */
    flowspec-analyze-ast(|resource, propname)

    /**
     * Analyze the given AST with NaBL2 and FlowSpec, but only the given FlowSpec properties.
     * Transform the AST with pre before the FlowSpec analysis, and with post after the FlowSpec analysis.
     *
     * @param pre:Term -> Term
     * @param post:Term -> Term
     * @param resource:String
     * @param propnames:String or List(String)
     * @type ast:Term -> (ast:Term, Analysis, errors:List(EditorMessage), warnings:List(EditorMessage), notes:List(EditorMessage))
     */
    flowspec-analyze-ast(pre,post|resource, propnames)

    /**
     * Take the analyze-ast 5-tuple output and return the result of applying the given strategy to the AST.
     * Note that the strategy takes the analysis object as a term argument.
     *
     * @param s(|Analysis): Term -> Term
     * @type ast: (ast:Term, Analysis, errors:List(EditorMessage), warnings:List(EditorMessage), notes:List(EditorMessage)) -> Term
     */
    flowspec-then(s)

    /**
     * Analyze the given AST with NaBL2 and FlowSpec, but only the given FlowSpec properties.
     * Then return the result of applying the given strategy to the AST. 
     * Note that the strategy takes the analysis object as a term argument.
     *
     * @param s(|Analysis): Term -> Term
     * @param resource:String
     * @param propnames:String or List(String)
     * @type ast:Term -> Term
     */
    flowspec-analyze-ast-then(s|resource, propnames)

    /**
     * Analyze the given AST with NaBL2 and FlowSpec, but only the given FlowSpec properties.
     * Transform the AST with pre before the FlowSpec analysis, and with post after the FlowSpec analysis.
     * Then return the result of applying the given strategy to the AST. 
     * Note that the strategy takes the analysis object as a term argument.
     *
     * @param pre:Term -> Term
     * @param post:Term -> Term
     * @param s(|Analysis): Term -> Term
     * @param resource:String
     * @param propnames:String or List(String)
     * @type ast:Term -> Term
     */
    flowspec-analyze-ast-then(pre, post, s|resource, propnames)

Querying analysis
-----------------

The NaBL2 API defines several :ref:`strategies to get an analysis term by resource
name or from an AST node <nabl2-get-analysis-result>`. This analysis
term can then be passed to the querying strategies that give access to the data
flow properties, *if* you hooked FlowSpec into the NaBL2 analysis process.

The other way to get the analysis term is to execute the analysis with the `flowspec-analyze-ast*` variants. 

Control-flow graph
^^^^^^^^^^^^^^^^^^

There are a number of strategies to get the control-flow graph nodes associated with an AST fragment, as well as control-flow graph navigation strategies and AST search strategies to get back to the AST from a control-flow graph node. Note that querying the control-flow graph is cheap but finding the way back from the control-flow graph to the AST is more expensive. 

.. code-block:: stratego

    /**
     * Get the control flow graph node associated with the given term. 
     *
     * @param a : Analysis
     * @type term:Term -> CFGNode
     */
    flowspec-get-cfg-node(|a)

    /**
     * Get the control flow graph start node associated with the given term.
     *
     * @param a : Analysis
     * @type term:Term -> CFGNode
     */
    flowspec-get-cfg-start-node(|a)

    /**
     * Get the control flow graph start node associated with the given term.
     *
     * @param a : Analysis
     * @type term:Term -> CFGNode
     */
    flowspec-get-cfg-end-node(|a)

    /**
     * Get the control flow graph start node associated with the given term.
     *
     * @param a : Analysis
     * @type term:Term -> CFGNode
     */
    flowspec-get-cfg-entry-node(|a)

    /**
     * Get the control flow graph start node associated with the given term.
     *
     * @param a : Analysis
     * @type term:Term -> CFGNode
     */
    flowspec-get-cfg-exit-node(|a)

    /**
     * Get the control flow graph start node associated with the given term. 
     *
     * @param a : Analysis
     * @type term:Term -> CFGNode
     */
    flowspec-get-cfg-prev-nodes(|a)

    /**
     * Get the control flow graph start node associated with the given term. 
     *
     * @param a : Analysis
     * @type term:Term -> CFGNode
     */
    flowspec-get-cfg-next-nodes(|a)

    /**
     * Find AST node corresponding to the CFGNode back again
     *
     * @param ast : Term
     * @type node:CFGNode -> Term
     */
    flowspec-cfg-node-ast(|ast)

    /**
     * Find AST node corresponding to the CFGNode back again
     *
     * @param ast : Term
     * @type pos:Position -> Term
     */
    flowspec-pos-ast(|ast)

    /**
     * Find parent of AST node corresponding to the CFGNode back again by matching the parent with
     *  the parent argument and giving back the child that is likely to be a match to the CFG node.
     *
     * @param parent : Term -> Term
     * @param ast : Term
     * @type node:CFGNode -> Term
     */
    flowspec-cfg-node-ast(parent|ast)

    /**
     * Find parent of AST node corresponding to the CFGNode back again by matching the parent with
     *  the parent argument and giving back the child that is likely to be a match to the CFG node.
     *
     * @param parent : Term -> Term
     * @param ast : Term
     * @type pos:Position -> Term
     */
    flowspec-pos-ast(parent|ast)

    /**
     * Get the position of an AST node.
     *
     * @type Term -> Position
     */
    flowspec-get-position

Data flow properties
^^^^^^^^^^^^^^^^^^^^

FlowSpec properties can be read in two versions, *pre* and *post*. These indicate whether the effect of the cfg node has been applied yet. Whether or not it is applied depends on the direction of the analysis. *pre* for a forward analysis is without the effect of the node, but *pre* for a backward analysis includes the effect of the node. 

Note that each strategy can simply take the term that's associated with the control-flow graph node. But the control-flow graph node itself is also an accepted input.

.. code-block:: stratego

    /**
     * Get the property of the control flow graph node associated with
     * the given term. The value returned is the value of the property
     * _before_ the effect of the control flow graph node. 
     *
     * @param a : Analysis
     * @param prop : String
     * @type term:Term -> Term
     */
    flowspec-get-property-pre(|a, propname)

    /**
     * Get the property of the control flow graph node associated with
     * the given term. The value returned is the value of the property
     * _after_ the effect of the control flow graph node. 
     *
     * @param a : Analysis
     * @param prop : String
     * @type term:Term -> Term
     */
    flowspec-get-property-post(|a, propname)

    /**
     * Get the property of the control flow graph node associated with
     * the given term. The value returned is the value of the property
     * _after_ the effect of the control flow graph node. If no node
     * is found the exit control flow graph node of the AST node is
     * queried for its post-effect property value. 
     *
     * @param a : Analysis
     * @param prop : String
     * @type term:Term -> Term
     */
    flowspec-get-property-post-or-exit-post(|analysis-result, analysis-name)

FlowSpec data helpers
"""""""""""""""""""""

FlowSpec sets and maps are passed back to Stratego as lists wrapped in ``Set`` and ``Map`` constructors. As a convenience, the most common operations are lifted and added to the flowspec API:

.. code-block:: stratego

    /**
     * Check if a FlowSpec Set contains an element. Succeeds if the given strategy succeeds for at
     * least one element.
     *
     * @param s: Term -?>
     * @type FlowSpecSet -?> FlowSpecSet
     */
    flowspec-set-contains(s)

    /**
     * Look up elements in a FlowSpec Set of pairs. Returns the right elements of all pairs where
     * the given strategy succeeds on the left element.
     *
     * @param s: Term -?>
     * @type FlowSpecSet -?> List(Term)
     */
    flowspec-set-lookup(s)

    /**
     * Look up a key in a FlowSpec Map. Returns the element if the given key exists in the map.
     *
     * @param k: Term
     * @type FlowSpecMap -?> Term
     */
    flowspec-map-lookup(|k)

Hover text
----------

For a hover implementation that displays name, type and FlowSpec properties use:

.. code-block:: stratego

    /**
     * Provides a strategy for a hover message with as much information as possible about name, type
     * (from NaBl2) and FlowSpec properties. 
     */
    flowspec-editor-hover(language-pp)

Profiling information
---------------------

.. code-block:: stratego

    /**
     * If flowspec-debug-profile is extended to succeed, some timing information will be printed in
     * stderr when using flowspec-analyze*.
     */
    flowspec-debug-profile
