==================
Naming Conventions
==================

The current code base of Spoofax has a variety of naming conventions. We are in the processes of consolidating this. Any new additions to Spoofax should ideally use the following naming conventions (note that this includes both Java code and Spoofax meta languages):

Artifact ID (Identifier in the Spoofax "new project" wizard)
  <to-the-point, unique, name, separated by '.' if needed>
Group ID  (Group Identifier in the wizard)
  org.metaborg
Package
  mb.<Artifact ID>.*
Directory name (Project name in the wizard unless you specify the location separately)
  <Artifact ID, separated by '.' or directory structure if needed>
Language name (Name in the wizard)
  <to-the-point, unique, name>

Everything lowercase and singular.

Examples
--------

NaBL2 language
^^^^^^^^^^^^^^


Artifact ID
  nabl2.lang
Group ID
  org.metaborg
Directory name
  nabl2.lang
Language name
  nabl2

NaBL2 solver Java code
^^^^^^^^^^^^^^^^^^^^^^


Artifact ID
  nabl2.solver
Group ID
  org.metaborg
Package
  mb.nabl2.solver.*
Directory name
  nabl2.solver

PIE language
^^^^^^^^^^^^


Artifact ID
  pie.lang
Group ID
  org.metaborg
Directory name
  pie/lang
Language name
  pie

PIE runtime (core)
^^^^^^^^^^^^^^^^^^


Artifact ID
  pie.runtime.core
Group ID
  org.metaborg
Package
  mb.pie.runtime.core.*
Directory name
  pie/runtime/core

PIE runtime (builtin functions)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


Artifact ID
  pie.runtime.builtin
Group ID
  org.metaborg
Package
  mb.pie.runtime.builtin.*
Directory name
  pie/runtime/builtin
