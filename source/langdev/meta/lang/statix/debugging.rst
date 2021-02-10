.. _statix-debugging:

.. role:: statix(code)
   :language: statix
   :class: highlight

=========
Debugging
=========

This section describes several techniques that can be used to debug
your Statix specification if it does not work as you expect.

There are three main categories of problems you may encounter:

1. Errors reported in your Statix files. These may come from syntax errors, unresolved names for
   modules or predicates, type errors, or problems with illegal scope extension.
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

- See if the disappears after a clean build (run ``Project > Clean...`` and than ``Project > Build
  Project`` on your project). If the problem disappears after a clean build, but then consistently
  reappears after subsequent editing or building, it should be reported as a potential bug.
- Are there errors on any Statix files? The behavior of running Statix on your language files is
  undefined when the specification itself has errors. Check the ``Package Explorer`` as well as the
  ``Problems`` and ``Console`` views to make sure none of the Statix files have errors on them. Fix
  such errors before debugging any other issues!
- Check for errors in the ``Package Explorer`` and in open editors, as well as in the ``Console``,
  ``Problems``, and ``Error Log`` views.
  
Checking AST Traversal
----------------------

Ensure that your Statix rules are applied to the AST nodes. It is easy to forget to apply a
predicate to a subterm, especially for bigger languages. If you are not sure if the rules are
applied to a certain AST node, add a forced node to that AST node as follows:

.. code-block:: statix

   extendsOk(s_lex, Extends(m), s_mod) :- {s_mod'}
     try { false } | note "extendsOK applied",
     resolveMod(s_lex, m) == s_mod',
     s_mod -EXT-> s_mod'. 

Build your project and check if the note appears where you expect it. If it does not appear, find
the places where those AST nodes may appear and enure the predicate is applied.

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
and check if references resolve to the definitions you expect, by ``Ctrl/Cmd+RightClick`` on the
reference.

Note that ``statix/References`` must be included in one of your ESV files for this to work. This is
by default the case for generated projects that use Statix.

Interpreting Error Messages
---------------------------

The error messages produced by Statix include a part of the trace of the failing constraint, to make
it easier to figure out where the error originated. A typical error message may look as follows:

.. code-block:: text

     [(?q.unit-wld61-10,(?q.unit-x'-11,?q.unit-T-5))] == []
   > query filter ((Label("units/name-resolution/interface!EXT"))* Label("units/name-resolution/default-impl!var")) and { (?x',_) :- ?x' == "q" } min irrefl trans anti-sym { <edge>Label("units/name-resolution/default-impl!var") < <edge>Label("units/name-resolution/interface!EXT"); } and { _, _ :- true } in Scope("p.unit","s_mod_4-4") |-> [(?q.unit-wld61-10,(?q.unit-x'-11,?q.unit-T-5))]
   > units/name-resolution/interface!resolveVar(Scope("q.unit","s_mod_2-4"), QDefRef(QModInModRef(ModRef("P"),"B"),"q"),?q.unit-T-5)
   > units/statics!typeOfExpr(Scope("q.unit","s_mod_2-4"), VarRef(QDefRef(QModInModRef(ModRef(…),"B"),"q")), ?q.unit-T-5)
   > units/statics!defOk(Scope("q.unit","s_mod_2-4"), VarDef("e",VarRef(QDefRef(QModInModRef(…,…),"q"))), Scope("q.unit","s_mod_2-4"))
   > ... trace truncated ... 

As this looks daunting at first, we break it down.  At the top is the constraint that failed; in
this case an equality constraint.  Below that are several lines prefixed with ``>`` that show where
the constraint above it originated. We see that the equality originated from a ``query``, which
itself originated from one of the rules of ``resolveVar``, which was applied in one of the rules of
``typeOfExpr`` etc. As these traces can get very long, they are truncated to five entries.

Now we explain some more details of what we can see here:

- Errors may contain unification variables of the form ``?FILENAME-VARNAME-NUM``. These are
  instantiations of the meta-variables in the specification. The variable name ``VARNAME``
  corresponds to the name of the meta-variable that was instantiated, and can be helpful in
  reasoning about the origin of a unification variable. The file name is the file that was being
  checked when the unification variable was created. Due to Statix's operation, this can sometimes
  be the project root instead of the actual file.
- Scope values are shown as ``#FILENAME-VARNAME-NUM``. Sometimes appear in the exploded form
  ``Scope("FILENAME", "VARNAME-NUM")``, such as in the example error message above.
- Predicate names are prefixed with the name of the module they are defined in. For example,
  ``defOk`` is defined in ``units/statics`` and therefore appears as ``units/statics!defOk`` in the
  trace. Note that the predicate name is prefixed with the Statix module that *defines* the
  predicate. (The rules for the predicate may be defined in other modules.)
- The trace shows which predicates were applied, and to which arguments. It does not show which
  predicate rule was chosen! This can often be deduced from the line above it in the trace, but if
  unsure, use a forced note (see :ref:`Inspecting Variables`) to check your expectation.

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
         units/name-resolution/interface!LEX : #-s_1-1
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
         units/name-resolution/interface!LEX : #-s_1-1
       }
     }
     #-s_1-1 {
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
  those edges to be traversed? Are you querying the correct relation, and are is the filter
  predicate correct for the data you want to match?

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

Some Common Problems
--------------------

- Predicates fail with ``amb(...)`` terms as arguments. These terms indicate parsing ambiguities,
  which should be fixed in the grammar (SDF3) files.

Getting Help and Reporting Issues
---------------------------------

If the techniques above did not help to solve your problem, you can ask us for help or report the
issue you found. To make this process as smooth as possible, we ask you to follow the following
template when asking a Statix related question:

1. Single sentence description of the issue.
2. Spoofax version. See *About Eclipse*; *Installation Details*; *Features*, and search for
   *Spoofax*.
3. Statix configuration: single-file or multi-file mode. Multi-file mode is enabled when the
   ``observer`` setting in in your ESV looks like ``observer: XXX (constraint) (multifile)``.
4. Steps to reproduce. Best is to include a small, self-contained test (see :ref:`Testing
   Predicates` above) so that others can easily run the test and reproduce the issue! If that is not
   possible, provide a (link to) a project, including an example file, that shows the problem. Keep
   the project and the example as small as possible, and be specific about
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

