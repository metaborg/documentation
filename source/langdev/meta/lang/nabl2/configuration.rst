=============
Configuration
=============

We will show you how to prepare your project for use with NaBL2, and
write your first small specification.

Prepare your project
--------------------

You can start using NaBL2 by creating a new project, or by modifying
an existing project. See below for the steps for your case.

Start a new project
~~~~~~~~~~~~~~~~~~~

If you have not done this already, install Spoofax Eclipse, by
following the :doc:`installation instructions
</source/langdev/start>`.

Create a new project by selecting ``New > Project...`` from the
menu. Selecting ``Spoofax > Spoofax language project`` from the list,
and click ``Next``. After filling in a project name, an identifier,
name etc will be automatically suggested. To use NaBL2 in the project,
select ``NaBL2`` as the analysis type. Click ``Finish`` to create the
project.

Convert an existing project
~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you have an existing project, and you want to start using NaBL2,
there are a few changes you need to make.

First of all, make sure the ``metaborg.yaml`` file contains at least
the following dependencies.

.. code-block:: yaml

   ---
   # ...
   dependencies:
     compile:
     - org.metaborg:org.metaborg.meta.nabl2.lang:${metaborgVersion}
     source:
     - org.metaborg:org.metaborg.meta.nabl2.shared:${metaborgVersion}
     - org.metaborg:org.metaborg.meta.nabl2.runtime:${metaborgVersion}

We will set things up, such that analysis rules will be grouped
together in the directory ``trans/analysis``. Create a file
``trans/analysis/main.str`` that contains the following.

.. code-block:: stratego

   module analysis/main

   imports

     nabl2shared
     nabl2runtime
     analysis/-

Add the following lines to your main ``trans/LANGUAGE.str``.

.. code-block:: stratego

   module LANGUAGE

   imports

     analysis/main

   rules

     editor-analyze = analyze(desugar-pre,desugar-post)

If your language does not have a desugaring step, use
``analyze(id,id)`` instead.

Finally, we will add reference resolution and menus to access the
result of analysis, by adding the following lines to
``editor/Main.esv``.

.. code-block:: esv

   module Main

   imports

     nabl2/References
     nabl2/Menus

You can now continue to the :doc:`example specification here
<examples>`, or directly to the :doc:`language reference <reference>`.

Runtime settings
----------------

Multi-file analysis
~~~~~~~~~~~~~~~~~~~

By default, files are analyzed independently of each other. Files can
also be analyzed in the project context. This allows cross-file
references, imports, et cetera. This is called ``multifile`` mode, and
is configured the ESV files of a language definition. To enable
multi-file mode, add the ``(multifile)`` option to the ``observer``:

.. code-block:: esv

   observer = editor-analyze (multifile)

Logging
~~~~~~~

The log output of NaBL2 analysis can be controlled by setting the
``runtime.nabl2.debug`` option in a projects ``metaborg.yaml``.

The following debug flags are recognized:

 * ``analysis`` enables summary output about the analysis; number of
   files analyzed and overal runtime.
 * ``files`` enables output about individual files; which files are
   being analyed.
 * ``collection`` enables output about constraint collection; a trace
   of the rules are applied during collection.
 * ``timing`` enables output about the runtimes of different parts of
   the analysis.
 * ``all`` enables all possible output.

For example, to enable summary output about the analysis, add the
following to a projects ``metaborg.yaml``:

.. code-block:: yaml

   runtime:
     nabl2:
       debug: analysis
       
Stratego API
------------------

Strategies to interact with analysis are defined in the nabl2 API:

   <https://github.com/metaborg/nabl/blob/master/org.metaborg.meta.nabl2.runtime/trans/nabl2/api.str>
   
Use the API by importing ``import nabl2/api``

Customize analysis
------------------

Custom post-analysis
~~~~~~~~~~~~~~~~~~~~

Implements hooks to add your own analysis step

Custom pretty-printing
~~~~~~~~~~~~~~~~~~~~~~

Printing of terms

Make sure everything can be printed

Inspecting analysis results
---------------------------

You can debug your specification by inspecting the result of analysis,
and by logging a trace of the rules that get applied during constraint
generation.

The result of analysis can be inspected, by selecting elements from
the ``Spoofax > Analysis`` the menu. For multifile projects, use the
``Project`` results, or the ``File`` results for singlefile projects.

