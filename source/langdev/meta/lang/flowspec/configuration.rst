=============
Configuration
=============

We will show you how to prepare your project for use with FlowSpec, and
write your first small specification.

Prepare your project
--------------------

You can start using FlowSpec by creating a new project, or by modifying
an existing project. See below for the steps for your case.

Start a new project
~~~~~~~~~~~~~~~~~~~

If you have not done this already, install Spoofax Eclipse, by
following the :doc:`installation instructions
</source/langdev/start>`.

Create a new project by selecting ``New > Project...`` from the
menu. Selecting ``Spoofax > Spoofax language project`` from the list,
and click ``Next``. After filling in a project name, an identifier,
name etc will be automatically suggested. Select ``NaBL2`` as the 
analysis type, FlowSpec builds on top of NaBL2's analysis infrastructure.
Click ``Finish`` to create the project.

Add the following dependencies in the ``metaborg.yaml`` file:

.. code-block:: yaml

   ---
   # ...
   dependencies:
     compile:
     - org.metaborg:flowspec.lang:${metaborgVersion}
     source:
     - org.metaborg:flowspec.lang:${metaborgVersion}

Add menus to access the result of analysis, by adding the following import
to ``editor/Main.esv``.

.. code-block:: esv

   module Main

   imports

     flowspec/Menus

Convert an existing project
~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you have an existing project, and you want to start using FlowSpec,
there are a few changes you need to make.

First of all, make sure the ``metaborg.yaml`` file contains at least
the following dependencies.

.. code-block:: yaml

   ---
   # ...
   dependencies:
     compile:
     - org.metaborg:org.metaborg.meta.nabl2.lang:${metaborgVersion}
     - org.metaborg:flowspec.lang:${metaborgVersion}
     source:
     - org.metaborg:org.metaborg.meta.nabl2.shared:${metaborgVersion}
     - org.metaborg:org.metaborg.meta.nabl2.runtime:${metaborgVersion}
     - org.metaborg:flowspec.lang:${metaborgVersion}

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

     editor-analyze = nabl2-analyze(desugar-pre)

If your language does not have a desugaring step, use
``nabl2-analyze(id)`` instead.

Add an NaBL2 specification. The most minimal one is the following.

.. code-block:: nabl2

    module analysis/minimal

    rules

    init.

    [[ _ ]].

Running and integrating the FlowSpec analysis is explained on the :doc:`Stratego API page <stratego-api>`. 

Finally, we will add reference resolution and menus to access the
result of analysis, by adding the following lines to
``editor/Main.esv``.

.. code-block:: esv

   module Main

   imports

     nabl2/References
     nabl2/Menus
     flowspec/Menus

You can now continue to the :doc:`example specification here
<examples>`, or directly to the :doc:`language reference <reference>`.
       
Inspecting analysis results
---------------------------

You can debug your specification by inspecting the result of analysis.

The result of analysis can be inspected, by selecting elements from the 
``Spoofax > FlowSpec Analysis`` the menu. For multi-file projects, use the ``Project`` results, or
the ``File`` results for single-file projects. The result is given as a control-flow graph annotated
with data-flow properties in the DOT format used by GraphViz. If you have GraphViz installed, you
can set the ``dot`` executable in the settings of the graphviz editor to allow you to jump straight
from Eclipse to the rendered graph. 

