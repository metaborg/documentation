.. _statix-debugging:

.. role:: statix(code)
   :language: statix
   :class: highlight

=========
Debugging
=========

This section describes several techniques that can be used to debug
your Statix specification if it does not work as you expect.

.. note::

   The single most useful thing you can do when debugging is to **make the problem as small as
   possible**! All the techniques you can use for debugging are more effective when the problem is
   as small as possible. Try to find the smallest example program and Statix specification that
   still exhibits your problem, and focus on those.

There are three main categories of problems you may encounter:

1. Errors reported in your Statix files. These may come from syntax errors, unresolved names for 
   modules or predicates, type errors, or problems with illegal scope extension. When these errors 
   are unexpected and not mentioned in :ref:`Common problems`, follow the steps in 
   :ref:`Basic Checklist` and :ref:`Creating Minimal Examples`. If that does not help out, please 
   follow the steps in :ref:`Getting Help`.
2. Unexpected behavior when running Statix on files of your language. This is the most common kind
   of problems. All debugging techniques after the :ref:`Basic Checklist` are focused on finding and
   debugging problems in the definitions in your specification. **Note that it is useless to try to
   solve problems of this kind when your specification still has errors!**
3. Analysis fails altogether. This usually results in ``Analysis failed`` errors at the top of files
   or on the project in the *Package Explorer*. Check the *Console* and *Error Log* for reported
   Java exceptions that can be included in a bug report.

.. _Basic Checklist:

Basic Checklist
---------------

These are some basic things that should always be checked when you encounter a problem:

- See if the disappears after a clean build (run ``Project > Clean...`` and than 
  ``Project > Build Project`` on your project). If the problem disappears after a clean build, but 
  then consistently reappears after subsequent editing or building, it should be reported as a
  potential bug.
- Are there errors on any Statix files? The behavior of running Statix on your language files is
  undefined when the specification itself has errors. Check the ``Package Explorer`` as well as the
  ``Problems`` and ``Console`` views to make sure none of the Statix files have errors on them. Fix
  such errors before debugging any other issues!
- Check for errors in the ``Package Explorer`` and in open editors, as well as in the ``Console``,
  ``Problems``, and ``Error Log`` views.
- See whether the section on :ref:`Common problems` or the remainder of the documentation answers 
  your question already.
  
Checking AST Traversal
----------------------

Ensure that your Statix rules are applied to the AST nodes. It is easy to forget to apply a
predicate to a subterm, especially for bigger languages. If you are not sure if the rules are
applied to a certain AST node, add a forced note (e.g. ``try { false } | note "text"``) to that AST
node as follows:

.. code-block:: statix

   extendsOk(s_lex, Extends(m), s_mod) :- {s_mod'}
     try { false } | note "extendsOK applied",
     resolveMod(s_lex, m) == s_mod',
     s_mod -EXT-> s_mod'. 

Build your project and check if the note appears where you expect it. If it does not appear, find
the places where those AST nodes may appear and ensure the predicate is applied.

Checking Reference Resolution
-----------------------------

Setting ``ref`` attributes on references allows you to check reference resolution interactively in
example programs of your language. The following rule shows how to do that using ``@x.ref := x'``:


.. code-block:: statix

   resolveVar(s, x) = T :- {x'}
     query typeOfDecl
       filter P* and { x' :- x' == x }
       min $ < P and true
       in s |-> [(_, (x', T))],
     @x.ref := x'.

This requires that ``x`` and ``x'`` are both names from the AST. Now write some example programs
and check if references resolve to the definitions you expect, by ``Ctrl + Click / Cmd + Right Click``
on the reference.

Note that ``statix/References`` must be included in one of your ESV files for this to work. This is
by default the case for generated projects that use Statix.

Interpreting Error Messages
---------------------------

Statix can be configured to contain a trace as part of the error messages for failing constraints,
which can be a great help for debugging.  Two parameters control message formatting. The first,
``message-trace-length`` controls whether a trace is included in the message, and how long it will
be. A value of ``0`` means no trace (if no custom message is provided, the failing constraint itself
is still shown), ``-1`` means the full trace. The default is set to ``0``, as showing traces is
mostly helpful for debugging when writing the spec and it slows down message formatting. The second,
``message-term-depth`` controls the depth up to which terms in messages are formatted. A value of
``-1`` means full terms. The default is set to ``3``, which is usually enough to understand the
terms involved, without choking up Eclipse or the console with large error messages. It is not
recommended to set both settings to ``-1``, because then every message will contain the full AST.

The configuration settings are part of the ``metaborg.yaml`` file of the project containing the
language files (not the project containing the specification!), and look as follows:

.. code-block:: text

   runtime:
     statix:
       message-trace-length: 5 # default: 0, full trace: -1
       message-term-depth: 3 # -1 = max

A typical error message including a trace may look as follows:

.. code-block:: text

     [(?q.unit-wld61-10,(?q.unit-x'-11,?q.unit-T-5))] == []
   > query filter ((Label("units/name-resolution/interface!EXT"))* Label("units/name-resolution/default-impl!var")) and { (?x',_) :- ?x' == "q" } min irrefl trans anti-sym { <edge>Label("units/name-resolution/default-impl!var") < <edge>Label("units/name-resolution/interface!EXT"); } and { _, _ :- true } in #p.unit-s_mod_4-4 |-> [(?q.unit-wld61-10,(?q.unit-x'-11,?q.unit-T-5))]
   > units/name-resolution/interface!resolveVar(#q.unit-s_mod_2-4, QDefRef(QModInModRef(ModRef("P"),"B"),"q"),?q.unit-T-5)
   > units/statics!typeOfExpr(#q.unit-s_mod_2-4, VarRef(QDefRef(QModInModRef(ModRef(…),"B"),"q")), ?q.unit-T-5)
   > units/statics!defOk(#q.unit-s_mod_2-4, VarDef("e",VarRef(QDefRef(QModInModRef(…,…),"q"))), #q.unit-s_mod_2-4)
   > ... trace truncated ... 

As this looks daunting at first, we break it down.  At the top is the constraint that failed; in
this case an equality constraint.  Below that are several lines prefixed with ``>`` that show where
the constraint above it originated. We see that the equality originated from a ``query``, which
itself originated from one of the rules of ``resolveVar``, which was applied in one of the rules of
``typeOfExpr`` etc. As these traces can get very long, they are truncated to five entries.

Now we explain some more details of what we can see here:

- Errors may contain unification variables of the form ``?FILENAME-VARNAME-NUM`` or ``?VARNAME-NUM``.
  These are instantiations of the meta-variables in the specification. The variable name ``VARNAME``
  corresponds to the name of the meta-variable that was instantiated, and can be helpful in
  reasoning about the origin of a unification variable. When the name corresponds to a functional 
  predicate name, it is a return value from that predicate. The file name is the file that was being
  checked when the unification variable was created. Due to Statix's operation, this can sometimes
  be the project root instead of the actual file.
- Scope values are shown as ``#FILENAME-VARNAME-NUM`` or ``#VARNAME-NUM``. (Rarely they appear in the
  exploded form ``Scope("FILENAME", "VARNAME-NUM")``).
- Predicate names are prefixed with the name of the module they are defined in. For example,
  ``defOk`` is defined in ``units/statics`` and therefore appears as ``units/statics!defOk`` in the
  trace. Note that the predicate name is prefixed with the Statix module that *defines* the
  predicate. (The rules for the predicate may be defined in other modules.)
- The trace shows which predicates were applied, and to which arguments. It does not show which
  predicate rule was chosen! This can often be deduced from the line above it in the trace, but if
  unsure, use a forced note (see :ref:`Inspecting Variables`) to check your expectation.
- Error messages are fully instantiated with the *final* result. This means that variables that
  appear in error messages are free in the final result of this Statix execution. Therefore, we do
  *not* have to consider the order of execution or the moment when the error message was generated
  when interpreting error messages!

The section on :ref:`Common Problems` contains tips on how to deal with many error messages.

.. _Inspecting Variables:

Inspecting Variables
--------------------

Inspecting the values assigned to meta-variables can be very helpful to debug a
specification. Variables cannot be automatically inspected, but we can show their values by forcing
a note in the rule where the variable appears. The following rule shows how to do this for the
intermediate type ``T`` of the assigned variable:

.. code-block:: statix

   stmtOk(s, Assign(x, e)) :- {T U}
     T == resolveVar(s, x),
     try { false } | note $[assignee has type [T]],
     U == typeOfExp(s, e),
     subtype(U, T).

Inspecting the Scope Graph
--------------------------

Inspecting the scope graph that is constructed by Statix can be very helpful in debugging problems
with scoping and name resolution queries. After type checking, view the scope graph of a file using
the ``Spoofax > Statix > Show scope graph`` menu. Note that in multi-file mode, the scope graph is
always the graph of the whole project. Therefore, creating a small example project with only a few
files can be very helpful (see also :ref:`Creating Minimal Examples`).

Here is an example of such a scope graph:

.. code-block:: text

   scope graph
     #q.unit-s_mod_2-4 {
       relations {
         units/name-resolution/default-impl!var : ("e", UNIT())
       }
       edges {
         units/name-resolution/interface!LEX : #s_1-1
       }
     }
     #p.unit-s_mod_4-4 {
       relations {
         units/name-resolution/default-impl!var : ("b", UNIT())
       }
       edges {
         units/name-resolution/interface!LEX : #p.unit-s_mod_2-6
       }
     }
     #p.unit-s_mod_2-6 {
       relations {
         units/name-resolution/default-impl!mod : ("B", #p.unit-s_mod_4-4)
       }
       edges {
         units/name-resolution/interface!LEX : #s_1-1
       }
     }
     #s_1-1 {
       relations {
         units/name-resolution/default-impl!mod : ("E", #q.unit-s_mod_2-4)
                                                  ("P", #p.unit-s_mod_2-6)
       }
     }

The scope graph is presented as a list of scopes, with the relation entries and outgoing edges from
that scope. Remember that the names of the scopes match the names of the meta-variables in the
specification! For example, ``#p.unit-s_mod_4-4`` originated from a meta-variable ``s_mod``. Paying
attention to this is very helpful in figuring out the structure of the graph.

Some useful questions you can ask yourself when inspecting the scope graph for debugging:

- Does the graph have the structure I expect from the current example program? Are all the scopes
  that I expect there, and are all the scopes that are there expected? Do all scopes have the
  expected relations in them? Do the have the expected outgoing edges?
- When you are debugging a certain query, consider the scope in which the query starts, and execute
  the query in the given graph. Are the necessary edges present? Does the regular expression allow
  those edges to be traversed? Are you querying the correct relation, and is the filter predicate
  correct for the data you want to match?

When considering these questions, it can be helpful to use the ideas from :ref:`Inspecting
Variables` to verify the scope a query is executed in, or to show the scope that is created for a
definition, and match those with what you see in the scope graph.

.. _Creating Minimal Examples:

Creating Minimal Examples
-------------------------

Creating a minimal example is one of the most useful things you can do when debugging. It helps you
to get to the core of the problem, but it also benefits all of the other techniques we have
discussed so far. Having a smaller example makes it easier to inspect the scope graph, makes it
easier to inspect variables as there are fewer, and reduced the number of error messages to review.

An example is a file, or set of files, in your langauge, where Statix does not behave as you expect.
A minimal example is usually created by starting from a big example that exhibits the problem. Try
to eliminate files and simplify the example program while keeping the unexpected behavior. The
smaller the program and the fewer rules in your specification are used for this program, the easier
it is to debug.

.. _Testing Predicates:

Testing Predicates
------------------

Sometimes creating a minimal example program in your language is not enough to fix a problem. In
such cases writing Statix tests is a great way to test your definitions in even more detail. In a
Statix test you can specify a constraint and evaluate it to see how it behaves. For example, if you
suspect a bug in the definition of the ``subtype`` predicate, you could test it as follows:

.. code-block:: statix

   // file: debug.stxtest
   resolve {T}
     T == typeOfExp(Int("42")),
     subtype(T, LONG())
   imports
     statics

The ``.stxtest`` file starts with ``resolve`` and a constraint, which can be anything that can
appear in a rule body. After that, the test may specify ``imports``, ``signature`` and ``rules``
sections like a regular Statix module. A test is executed using the ``Spoofax > Evaluate > Evaluate
Test`` menu. Evaluation outputs a ``.stxresult`` file, which looks as follows:

.. code-block:: text

   substitution
     T |-> INT()

   analysis
     scope graph
   
   errors
     *   INT() == LONG()
       > statics!subtype(INT(), LONG())
       > ... trace truncated ...
   
   warnings
   
   notes
   
The test result shows the value of top-level variables from the ``resolve`` block (in this case
``T``), the scope graph that was constructed (in this case empty), and any messages that were
generated (in this case one error).

These tests are a great way to verify that the predicate definitions work as you expect. Apply your
predicates to different arguments to check their behavior. Even more complicated mechanisms such as
queries can be debugged this way. Simply construct a scope graph in the ``resolve`` block (using
``new``, edges, and declarations), and execute your querying predicate on the scopes you have
created. As a starting point, you can take the AST of your example program (using the ``Spoofax >
Syntax > Show parse AST`` menu), and use that as an argument to your top-level predicate.

Creating a *self-contained* Statix test is a good way to isolate a problem. Instead of importing all
your definitions, copy the relevant definitions to the test (in a ``rules`` section), and try to
create the smallest set of rules and predicate arguments that still exhibit the problem you are
debugging. A self-contained test is also very helpful when asking others for help, as it is much
easier to review and run than having to setup and build a complete language project.

.. _Common Problems:

Some Common Problems
--------------------

- Predicates fail with ``amb(...)`` terms as arguments. These terms indicate parsing ambiguities,
  which should be fixed in the grammar (SDF3) files.

- Errors in your specification appear at incorrect places (e.g. sort or constructor declarations).
  In such cases, the declaration is referenced from an invalid position anywhere in your 
  specification, but due to the non-deterministic order of constraint solving the error appears at
  the observed position. The best approach to solve these issues is to comment away all usages,
  until the error disappears. Then, in the last commented position, the declaration is used 
  incorrectly.

- One or both of the ``fileOk(...)`` or ``projectOk(...)`` predicates fail immediately, for example 
  with the error messages:

  .. code-block:: text

     statics!fileOk(#s_1-1,Test([Prog("A.mod",Decls(…)),Prog("B.mod",Decls(…)),Prog("C.mod",Decls(…))])) (no origin information)
     statics!projectOk(#s_1-1) (no origin information)
 
  In such cases, you have probably renamed the top-level file, or moved the declarations of these
  predicates to another file that is imported.  Assuming the predicates are now defined in the
  module ``statics/mylang`` as follows:

  .. code-block:: statix
  
     // file: trans/statics/mylang.stx
     module statics/mylang
     imports statics/mylang/program

     rules

       projectOk : scope
       projectOk(s).
  
       fileOk : scope * Start   
       fileOk(s, p) :- programOk(s, p).
  
  If this module is the top-level module of your specification, then you have to change the call to
  ``stx-editor-analyze`` in ``trans/analysis.str`` such that the first term argument (which
  specifies the module to use, by default ``"statics"``) is the new module name (in this case
  ``statics/mylang``).

  On the otherhand, if you kept ``statics`` as the top-level module and have it import the module
  ``statcs/mylang``, then you have to change the call to ``stx-editor-analyze`` in
  ``trans/analysis.str`` such that the second and third term argument (which specify the predicates
  to apply to projects and files, respectively) are qualified by the module name (in this case
  ``"statics/mylang!projectOk"`` and ``""statics/mylang!fileOk``, respectively).

- Files of your language are only analyzed by Statix after they are opened in an editor in
  Eclipse. There are several reasons why this may be hapening:

  - The project containing the files is not a Spoofax project. A spoofax project must contain a
    `metaborg.yaml`. If it is a Maven project, the `packaging` must be one of
    `spoofax-{language,test,project}`.

  - The project containing the files does not have a dependency on your language. Spoofax only
    analyzes files of your language if the `metaborg.yaml` configuration contains a `compile`
    dependency on the language definition. This should look similar to the following:

    .. code-block:: yaml

       dependencies:
         compile:
         - org.example:your-language:1.0-SNAPSHOT

  - The language is missing. If a language dependency is missing, this is reported with errors on
    the console. Make sure your language definition project is open in Eclipse and that is is
    successfully built.

  - Eclipse is not configured to automatically build files. This can be enabled by selecting
    `Project > Build automatically` from the Eclipse menu.

  - The project in Eclipse did not get the Spoofax nature. Imported Maven projects with one of the
    `spoofax-*` packagings normally get the Spofoax nature automatically, but sometimes this doesn't
    work correctly. Non-Maven projects always have to be assigned the Spoofax nature manually. This
    can be done with `Spoofax > Add Spoofax nature` in the context-menu of the project containing
    the files.

- A lot of errors are reported. It happens that a single problem in the type checked program leads
  to the failure of other constraints (cascading errors). For example, an unresolved name might lead
  to errors about subtype checks that cannot be solved, import edges that cannot be created,
  etc. Here are some tips to help you find the root cause of the probem:

  - Differentiate between failed and unsolved constraints. The cause of a problem is usually found
    best by looking at the failed constraints. For example, an unresolved name might result in an
    error on the equality constraint between the expected and actual query result. Errors on
    unsolved constraints are marked as _Unsolved_. Unsolved errors are often the result of
    uninstantiated logical variables.

    Predicates remain unsolved if the uninstantiated variable prevents the selection of an
    applicable rule for the predicate. For example, an unsolved error ``subtype(INT(), ?T-1)`` is
    caused by the free variable ``?T-1`` which prevents selecting the appropriate rule of the
    ``subtype`` predicate.

    Queries remain unsolved if the query scope is not instantiated, or if variables used in the
    matching predicate (such as the name to resolve) remained free. For example, an unsolved error
    ``query filter (e Label("typeOfDecl")) and { (?x',_) :- ?x' == ?x-5 } min irrefl trans anti-sym
    { <edge>Label("typeOfDecl") < <edge>Label("P"); } and { _, _ :- true } in ?s-3 |->
    [(?wld0-1,(?x'-2,?T-4))]`` cannot be resolved because the scope variable ``?s-3`` is free, and
    the free variable ``?x-5`` would prevent matching declarations. Use of the variables ``?x'-2``
    and ``?T-4`` might cause more unsolved constraints, since these also remain free when the query
    cannot be solved.

    Edge and declaration assertions remain unsolved if the scopes are not instantiated. For example,
    the edge assertion ``#s_2-1 -Label("P")-> ?s'-5`` cannot be solved because the
    variable for the target scope ``?s'-5`` is not instantiated. Unsolved edge constraints in
    particular can lead to lots of cascading errors, as they block all queries going through the
    source scope of the edge.

  - If it is not immediately clear which error is the root of a problem, it helps to figure out the
    free variable dependencies between reported errors. Consider the following small example of
    three reported errors:

    .. code-block:: text

       subtype(?T-5, LONG)
       #s_3-1 -Label("P")-> ?s'-6
       query filter ((Label("P"))* Label("typeOfDecl")) and { (?x',_) :- ?x' == "v" } min irrefl trans anti-sym { <edge>Label("typeOfDecl") < <edge>Label("P"); } and { _, _ :- true } in #s_3-1 |-> [(?wld4-1,(?x'-2,?T-5))]

    For each of these we can see which variables are necessary for the constraint to be solved, and
    which they might instantiate when solved. The ``subtype`` predicate is blocked on the variable
    ``?T-5``. The edge assertion is blocked on the scope variable ``?s'-6``. The query does not seem
    blocked on a variable (both the scope and the filter predicate are instantiated), but would
    instantiate the variables ``?x'-2`` and ``?T-5`` when solved.

    We can conclude that the ``subtype`` constraint depends on solving the query, so we focus our
    attention on the query. Now we realize that we query in the scope of the unsolved edge
    assertion. So, the query depends on the edge assertion, and our task is to figure out why the
    scope variable in the edge target is not instantiated.


.. _Getting Help:

Getting Help and Reporting Issues
---------------------------------

If the techniques above did not help to solve your problem, you can ask us for help or report the
issue you found. To make this process as smooth as possible, we ask you to follow the following
template when asking a Statix related question:

1. Single sentence description of the issue.
2. Spoofax version. See *About Eclipse*; *Installation Details*; *Features*, and search for
   *Spoofax*.
3. Statix configuration: single-file or multi-file mode. Multi-file mode is enabled when the
   ``observer`` setting in in your ESV looks like ``observer: editor-analyze (constraint) (multifile)``.
4. Steps to reproduce. Best is to include a small, self-contained test (see :ref:`Testing
   Predicates` above) so that others can easily run the test and reproduce the issue! If that is not
   possible, provide a (link to) a project, including an example file, that shows the problem. Keep
   the project and the example as small as possible, and be specific about the relevant parts of 
   your program and of your specification.
5. Description of the observed behavior. Also mention if the problem occurs consistently, or only
   sometimes? If only sometimes, does it occur always/never after a clean build, or does it occur
   always/never after editing and/or building without cleaning?
6. Description of the expected behavior.
7. Extra information that you think is relevant to the problem. For example, things you have tried
   already, pointers to the part of the rules you think are relevant to the problem etc. If you
   tried other examples that show some light on the issue, this is a good place to put those. Again,
   it is best if these also come as self-contained tests!

*Example.* An example bug report described using the format above:

.. code-block:: text

   Issue: 
   Spoofax version: 2.6.0.20210208-173259-master
   Statix setup: multi-file

   Steps to reproduce:
   Execute the test in ``example1.stxtest``.

   Observed behavior:
   Sometimes an error is reported that the ``query`` failed.
   The problem does not occur consistently. On some runs, the error appears, but not on others. This
   does not seem related to cleaning or building the project.

   Expected behavior:
   The test is executed and no errors are reported. Scope ``s1`` is reachable from ``s2``, so the
   query return a single result, and ``ps != []`` should therefore hold.


   Extra information:
   The test in ``example2.stxtest`` is very similar. The only difference is that the predicate
   ``nonempty`` has an extra rule for the singleton list. The predicate is semantically the same, as
   the extra rule fails, just as the general rule would do on the singleton list. However, this
   example never gives the unexpected error.

The bug report is accompanied by two self-contained tests. One illustrates the problem, while the
other shows a very similar variant that does not exhibit the problem.

.. code-block:: statix

   // example1.stxtest
   resolve {s1 s2}
     new s1, new s2, s2 -I-> s1,
     reachable(s1, s2)

   signature
     name-resolution
       labels
         I
   
   rules
   
     reachable : scope * scope
     reachable(s1, s2) :- {ps}
       query () filter I*
                and { s1' :- s1' == s1 }
                min and true
                in s2 |-> ps,
       nonempty(ps).
   
     nonempty : list((path * scope))
     nonempty(ps) :- ps != [].

.. code-block:: statix

   // example2.stxtest
   resolve {s1 s2}
     new s1, new s2, s2 -I-> s1,
     reachable(s1, s2)

   signature
     name-resolution
       labels
         I
   
   rules
   
     reachable : scope * scope
     reachable(s1, s2) :- {ps}
       query () filter I*
                and { s1' :- s1' == s1 }
                min and true
                in s2 |-> ps,
       nonempty(ps).
   
     nonempty : list((path * scope))
     nonempty(ps) :- ps != [].
     nonempty([_]) :- false.

