============
Stratego API
============

The Stratego API to NaBL2 allows the customization of certain parts of
the analysis process, and access to analysis results during after
analysis.

The full definition of the API can be found in `nabl2/api.str
<https://github.com/metaborg/nabl/blob/master/org.metaborg.meta.nabl2.runtime/trans/nabl2/api.str>`_.

Setup
-----

Using the Stratego API requires a dependency on the NaBL2 runtime, and
an import of the ``nabl2/api`` file.

*Example.* A Stratego module importing the NaBL2 API.

.. code-block:: stratego

   module example

   imports

     nabl2/api

Customization hooks
-------------------

Several aspects of the analysis process can be customized by
implementing hooks in Stratego.

Custom pretty-printing
~~~~~~~~~~~~~~~~~~~~~~

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
~~~~~~~~~~~~~~~

Analysis in NaBL2 proceeds in three phases. An initial phase is used
to create initial scopes and parameters. A second phase is used to
collected, and partially solve, constraints per compilation unit. A
final phase solves constraints. The constraints in the final phase are
those of all compilation units combined, if multi-file analysis is
enabled.

It is possible to run custom code after each of these phases, by
implementing ``nabl2-custom-analysis-init-hook``,
``nabl2-custom-analisys-unit-hook``, and
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
the analysis results. The final hook should return a tuple of errors,
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

Analysis querying
-----------------

The analysis API gives access to the result of analysis. Analysis
results are available during the final custom analysis step, or in
post-analysis transformations.

The API defines several strategies to get an analysis term by resource
name or from an AST node. This analysis term can then be passed to the
querying strategies that give access to the scope graph, name
resolution, etc.
