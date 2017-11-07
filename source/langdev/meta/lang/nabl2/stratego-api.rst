============
Stratego API
============

.. role:: nabl2(code)
   :language: nabl2
   :class: highlight

The Stratego API to NaBL2 allows the customization of certain parts of
the analysis process, and access to analysis result during after
analysis.

The full definition of the API can be found in the `nabl2/api
<https://github.com/metaborg/nabl/blob/master/org.metaborg.meta.nabl2.runtime/trans/nabl2/api.str>`__
module.

Setup
-----

Using the Stratego API requires a dependency on the NaBL2 runtime, and
an import of ``nabl2/api``.

*Example.* A Stratego module importing the NaBL2 API.

.. code-block:: stratego

   module example

   imports

     nabl2/api

Customizing analysis
--------------------

Several aspects of the analysis process can be customized by
implementing hooks in Stratego.

Custom pretty-printing
^^^^^^^^^^^^^^^^^^^^^^

By default the object language terms that are mentioned in error
messages are printed as generic terms. This may lead to error messages
like ``Expected number, but got FunT(IntT(), Int())``. By implementing
the ``nabl2-prettyprint-hook``, the term might be pretty-printed,
resulting in a message like ``Expected number, but got 'int ->
int'``. Care needs to be taken though, because the terms might contain
constraint variables, that are not part of the object language and
would break pretty-printing. This can be fixed by injecting the
``nabl2-prettyprint-term`` strategy into the object language
pretty-printing rule.

*Example.* A module that implements the pretty-printing hooks to
format types from the object language. This assumes that types are
defined in an SDF3 file using the sort ``Type``.

.. code-block:: stratego

   module example

   imports

     nabl2/api

   rules

     nabl2-prettyprint-hook    = prettyprint-YOURLANG-Type
     prettyprint-YOURLANG-Type = nabl2-prettyprint-term

Custom analysis
^^^^^^^^^^^^^^^

Analysis in NaBL2 proceeds in three phases. An initial phase is used
to create initial scopes and parameters. A second phase is used to
collected, and partially solve, constraints per compilation unit. A
final phase solves constraints. The constraints in the final phase are
those of all compilation units combined, if multi-file analysis is
enabled.

It is possible to run custom code after each of these phases, by
implementing ``nabl2-custom-analysis-init-hook``,
``nabl2-custom-analysis-unit-hook``, and
``nabl2-custom-analysis-final-hook(|a)``.

The initial hook receives a tuple of a resource string and AST node as
its argument. The result type of the initial hook is free.

The unit hook receives a tuple of a resource string, and AST node, and
the initial result if the initial hook was implemented. If the initial
hook is not implemented, an empty tuple ``()`` is passed as the
initial result. The result type of the unit hook is free.

The final hook receives a tuple of a resource string, the result if
the initial hook, and a list of results of the unit hook. The initial
result will again be ``()`` if the initial hook is not
implemented. The unit results might be an empty list if the unit hook
is not implemented. The final hook also receives an term argument for
the analysis result, that can be passed to the strategies to access
the analysis result. The final hook should return a tuple of errors,
warnings, notes, and a custom result. Messages should be tuples
``(origin-term, message)`` of the origin term from the AST, and the
message to report.

Custom analysis hooks are advised to use the strategies
``nabl2-custom-analysis-info-msg(|msg)`` and
``nabl2-custom-analysis-info(|msg)`` to report to the user. The first
version just logs the message term, while the second version also logs
the current term. If formatting the info messages is expensive, the
strategy ``nabl2-is-custom-analysis-info-enabled`` to check if logging
is actually enabled. The advantage of using these logging strategies
is that they are influenced by the logging settings in the project
configuration.

*Example.* A Stratego module that shows how to set up custom analysis
strategies.

.. code-block:: stratego

   module example

   imports

     nabl2/api

   rules

     nabl2-custom-analysis-init-hook:
         (resource, ast) -> custom-initial-result
       with nabl2-custom-analysis-info-msg(|"Custom initial analysis step");
            custom-initial-result := ...

     nabl2-custom-analysis-unit-hook:
         (resource, ast, custom-initial-result) -> custom-unit-result
       with <nabl2-custom-analysis-info(|"Custom unit analysis step")> resource;
            custom-unit-result := ...

     nabl2-custom-analysis-final-hook(|a):
         (resource, custom-initial-result, custom-unit-results) -> (errors, warnings, notes, custom-final-result)
       with nabl2-custom-analysis-info-msg(|"Custom final analysis step");
            custom-final-result := ... ;
            errors   := ... ;
            warnings := ... ;
            notes    := ...

Querying analysis
-----------------

The analysis API gives access to the result of analysis. The analysis
result is available during the final custom analysis step, or in
post-analysis transformations.

The API defines several strategies to get an analysis term by resource
name or from an AST node. This analysis term can then be passed to the
querying strategies that give access to the scope graph, name
resolution, etc.

Getting the analysis result
^^^^^^^^^^^^^^^^^^^^^^^^^^^



.. code-block:: stratego

   /**
    * Get analysis for the given AST node
    *
    * @type node:Term -> Analysis
    */
   nabl2-get-ast-analysis

   /**
    * Get analysis for the given resource
    *
    * @type filename:String -> Analysis
    */
   nabl2-get-resource-analysis

   /**
    * Test if analysis has errors
    *
    * Fails if there are no errors, succeeds otherwise.
    *
    * @type Analysis -> _
    */
   nabl2-analysis-has-errors

There are two ways to get the result of analysis. The first is calling
``nabl2-get-ast-analysis`` on a node if the analyzed AST. The second
is to call ``nabl2-get-resource-analysis`` with a resource name. The
resulting term can be passed as a term argument to the different query
strategies.

To check if analysis was successful, the strategy
``nabl2-analysis-has-errors`` can be used. This strategy will succeed
if any errors were encountered, and fail otherwise.

*Example.* Builder that only runs if analysis has no errors.

.. code-block:: stratego

   module example

   imports

     nabl2/api

   rules

     example-builder:
         (_, _, ast, path, project-path) -> (output-file, result)
       where analysis := <nabl2-get-resource-analysis> $[[project-path]/[path]];
             <not(nabl2-analysis-has-errors)> analysis
       with output-file := ... ;
            result      := ...

AST properties
^^^^^^^^^^^^^^

.. code-block:: stratego

  /**
   * @param a : Analysis
   * @type node:Term -> Term
   */
  nabl2-get-ast-params(|a)

  /**
   * @param a : Analysis
   * @type node:Term -> Type
   */
  nabl2-get-ast-type(|a)

AST nodes are associated with the parameters and (optionally) the type
mentioned in the rule that was applied to the node. For example, if a
rule like :nabl2:`[[ e ^ (s) : ty ]]` was applied to an expression in
the AST, it is possible to query the analysis for the scope ``s`` and
the type ``ty``. The strategy ``nabl2-get-ast-params(|a)`` expects an
AST node, and returns a tuple with the parameters. Similary
``nabl2-get-ast-type(|a)`` expects an AST node and returns the
type. If no type was specified, for example in a rule such as ``[[ e ^
(s1, s2) ]]``, the call will fail. The term argument ``a`` should be
an analysis result.

Nodes in the AST are indexed to make the connection between the AST
and the analysis result. The following strategies can be used to
preserve or manipulate AST indices. Note that this has no effect on
the result of analysis, so whether such manipulation is sound is up to
the user.

.. code-block:: stratego

   /**
    * Get AST index. Fails if term has no index.
    *
    * @type Term -> TermIndex
    */
   nabl2-get-ast-index

   /**
    * Set AST index on a term. Throws an exception of the index argument
    * is not a valid index.
    *
    * @param index : Termindex
    * @type Term -> Term
    */
   nabl2-set-ast-index(|index)

   /**
    * Copy AST index from one term to another. Fails if the source has no
    * index.
    *
    * @param from : Termindex
    * @type Term -> Term
    */
   nabl2-copy-ast-index(|from)

   /**
    * Execute a strategy and copy the index of the input term to the output
    * term. If the original term has no index, the result of applying s is
    * returned unchanged. Thus, failure behaviour of s is preserved.
    *
    * @type Term -> Term
    */
   nabl2-preserve-ast-index(s)

   /**
    * Erase AST indices from a term, preserving other annotations and
    * attachments.
    *
    * @type Term -> Term
    */
   nabl2-erase-ast-indices

Scope graph & name resolution
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The strategies concerning scope graphs and name resolution are
organized in three groups. The first group are strategies to create
and query occurrences in the scope graph. The second group gives
access to the structure of the scope graph. The third group exposes
the result of name resolution, as well as types and properties that
are set on declarations.

Working with occurrences
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: stratego

   /**
    * Make an occurrence in the default namespace
    *
    * NaBL2 equivalent: {node}
    *
    * @type node:Term -> Occurrence
    */
   nabl2-mk-occurrence

   /**
    * Make an occurrence in the specified namespace
    *
    * NaBL2 equivalent: ns{node}
    *
    * @param ns : String
    * @type node:Term -> Occurrence
    */
   nabl2-mk-occurrence(|ns)

   /**
    * Make an occurrence in the specified namespace, using an origin term
    *
    * NaBL2 equivalent: ns{node @t}
    *
    * @param ns : String
    * @param t : Term
    * @type node:Term -> Occurrence
    */
   nabl2-mk-occurrence(|ns,t)

   /**
    * Get namespace of an occurrence
    *
    * @type Occurrence -> ns:String
    */
   nabl2-get-occurrence-ns

   /**
    * Get name of an occurrence
    *
    * @type Occurrence -> Term
    */
   nabl2-get-occurrence-name



Querying the scope graph
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: stratego

   /**
    * Get all declarations in the scope graph
    *
    * @param a : Analysis
    * @type _ -> List(Occurrences)
    */
   nabl2-get-all-decls(|a)

   /**
    * Get all references in the scope graph
    *
    * @param a : Analysis
    * @type _ -> List(Occurrences)
    */
   nabl2-get-all-refs(|a)

   /**
    * Get all scopes in the scope graph
    *
    * @param a : Analysis
    * @type _ -> List(Scope)
    */
   nabl2-get-all-scopes(|a)

   /**
    * Get the scope of a reference
    *
    * @param a : Analysis
    * @type ref:Occurrence -> Scope
    */
   nabl2-get-ref-scope(|a)

   /**
    * Get the scope of a declaration
    *
    * @param a : Analysis
    * @type decl:Occurrence -> Scope
    */
   nabl2-get-decl-scope(|a)

   /**
    * Get declarations in a scope
    *
    * @param a : Analysis
    * @type Scope -> List(Occurrence)
    */
   nabl2-get-scope-decls(|a)

   /**
    * Get references in a scope
    *
    * @param a : Analysis
    * @type Scope -> List(ref:Occurrence)
    */
   nabl2-get-scope-refs(|a)

   /**
    * Get direct edges from a scope
    *
    * @param a : Analysis
    * @type Scope -> List((Label,Scope))
    * @type (Scope,Label) -> List(Scope)
    */
   nabl2-get-direct-edges(|a)

   /**
    * Get inverse direct edges from a scope
    *
    * @param a : Analysis
    * @type Scope -> List((Label,Scope))
    * @type (Scope,Label) -> List(Scope)
    */
   nabl2-get-direct-edges-inv(|a)

   /**
    * Get import edges from a scope
    *
    * @param a : Analysis
    * @type Scope -> List((Label,ref:Occurrence))
    * @type (Scope,Label) -> List(ref:Occurrence)
    */
   nabl2-get-import-edges(|a)

   /**
    * Get inverse import edges from a reference
    *
    * @param a : Analysis
    * @type ref:Occurrence -> List((Label,Scope))
    * @type (ref:Occurrence,Label) -> List(Scope)
    */
   nabl2-get-import-edges-inv(|a)

   /**
    * Get associated scopes of a declaration
    *
    * @param a : Analysis
    * @type decl:Occurrence -> List((Label,Scope))
    * @type (decl:Occurrence,Label) -> List(Scope)
    */
   nabl2-get-assoc-edges(|a)

   /**
    * Get associated declarations of a scope
    *
    * @param a : Analysis
    * @type Scope -> List((Label,decl:Occurrence))
    * @type (Scope,Label) -> List(decl:Occurrence)
    */
   nabl2-get-assoc-edges-inv(|a)

Querying name resolution
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: stratego

   /**
    * @param a : Analysis
    * @type decl:Occurrence -> Type
    */
   nabl2-get-type(|a)

   /**
    * @param a : Analysis
    * @param prop : String
    * @type decl:Occurrence -> Term
    */
   nabl2-get-property(|a,prop)

   /**
    * @param a : Analysis
    * @type ref:Occurrence -> (decl:Occurrence, Path)
    */
   nabl2-get-resolved-name(|a)

   /**
    * @param a : Analysis
    * @type ref:Occurrence -> List((decl:Occurrence, Path))
    */
   nabl2-get-resolved-names(|a)

   /**
    * Get visible declarations in scope
    *
    * @param a : Analysis
    * @type Scope -> List(Occurrence)
    */
   nabl2-get-visible-decls(|a)

   /**
    * Get reachable declarations in scope
    *
    * @param a : Analysis
    * @type Scope -> List(Occurrence)
    */
   nabl2-get-reachable-decls(|a)
