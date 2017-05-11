.. _dev-intro:

============
Introduction
============

Spoofax is the integration of many different tools, compilers, (meta-)languages, (meta-)libraries, and runtime components. This integration is made concrete in the `spoofax-releng <https://github.com/metaborg/spoofax-releng>`_ Git repository on GitHub. This repository contains all components via `Git submodules <https://git-scm.com/book/en/v2/Git-Tools-Submodules>`_, which are updated by our `build farm <http://buildfarm.metaborg.org/view/Spoofax/job/metaborg/job/spoofax-releng/>`_ that builds Spoofax whenever one of its components in a submodule changes.

Spoofax currently contains the following subcomponents as submodules:

- `releng <https://github.com/metaborg/spoofax-deploy/>`_ - release engineering scripts for managing and building the ``spoofax-releng`` repostory.
- Java libraries and runtimes

  - `mb-rep <https://github.com/metaborg/mb-rep/>`_ - libraries for program representation such as abstract terms
  - `mb-exec <https://github.com/metaborg/mb-exec/>`_ - Stratego interpreter and utilities
  - `jsglr <https://github.com/metaborg/jsglr/>`_ - JSGLR parser
  - `spoofax <https://github.com/metaborg/spoofax/>`_ - Spoofax Core, a cross platform API to Spoofax languages
  - `spoofax-maven <https://github.com/metaborg/spoofax-maven/>`_ - Maven integration for Spoofax Core
  - `spoofax-sunshine <https://github.com/metaborg/spoofax-sunshine/>`_ - Command-line integration for Spoofax Core
  - `spoofax-eclipse <https://github.com/metaborg/spoofax-eclipse/>`_ - Eclipse plugin for Spoofax Core
  - `spoofax-intellij <https://github.com/metaborg/spoofax-intellij/>`_ - IntelliJ plugin for Spoofax Core

- Meta-languages and libraries

  - `esv <https://github.com/metaborg/esv/>`_ - Editor service language
  - `sdf <https://github.com/metaborg/sdf/>`_ - Syntax Definition Formalisms, containing the SDF2 and SDF 3 languages
  - `stratego <https://github.com/metaborg/stratego/>`_ and `strategoxt <https://github.com/metaborg/strategoxt/>`_ - Stratego compiler, runtime, and editor
  - `nabl <https://github.com/metaborg/nabl/>`_ - Name binding languages, containing the NaBL and NaBL2 languages, and support libraries for NaBL2
  - `ts <https://github.com/metaborg/ts/>`_ - Type system language
  - `dynsem <https://github.com/metaborg/dynsem/>`_ - Dynamic semantics language
  - `metaborg-coq <https://github.com/metaborg/metaborg-coq/>`_ - Coq signatures and syntax definition
  - `spt <https://github.com/metaborg/spt/>`_ - Spoofax testing language
  - `runtime-libraries <https://github.com/metaborg/runtime-libraries/>`_ - NaBL support libraries, incremental task engine for incremental name and type analysis

Furthermore, this repository contains a Bash script :command:`./b` that redirects into the Python release engineering scripts in the ``releng`` submodule. These scripts support managing this Git repository, version management, generation of Eclipse instances, building Spoofax, and releasing new versions of Spoofax.

The rest of this manual describes how to set up Maven and other required tools for building and developing Spoofax, how to build and develop Spoofax, how to write this documentation, and explains some of the internals of Spoofax components.
