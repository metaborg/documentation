.. highlight:: yaml

=============
Configuration
=============

Configuration is specified in the :file:`metaborg.yaml` file at the root of the project.

------
Format
------

The configuration is written in `YAML <http://yaml.org/>`_, a human-friendly textual data format.
YAML is indentation sensitive, be sure to properly indent nested elements with 2 spaces.

We use the `commons-configuration2 <https://commons.apache.org/proper/commons-configuration/index.html>`_ framework to process configuration, which supports variables, nesting, and lists.


^^^^^^^^^
Variables
^^^^^^^^^


Any existing configuration option can be used as a variable with the ``${var}`` syntax, for example::

  id: org.metaborg:org.metaborg.meta.lang.sdf:${metaborgVersion}
  metaborgVersion: 2.0.0-SNAPSHOT

Here, the ``${metaborgVersion}`` variable reference is replaced with ``2.0.0-SNAPSHOT`` when reading the ``id`` configuration option.
Note that the order in which configuration options and variable references occur does not matter.

The ``${path:root}`` builtin property can be used to point to the root of the language specification.
Paths in the configuration must be absolute unless stated otherwise.
Use ``${path:root}/`` to make paths absolute, relative to the project root, where required.

Furthermore, environment variables can be used through ``${env:}``, for example ``${env:PATH}``.
See the documentation on `variable interpolation <https://commons.apache.org/proper/commons-configuration/userguide/howto_basicfeatures.html#Variable_Interpolation>`_ for more detailed informations on how variables work.

^^^^^^^
Nesting
^^^^^^^

Configuration options can be nested by nesting YAML objects, for example::

  language:
    sdf:
      version: sdf2

results in the ``language.sdf.version`` option being set to ``sdf2``, and can be referenced with a variable using ``${language.sdf.version}``.
The same option can be set in the following way::

  language.sdf.version: sdf2

^^^^^
Lists
^^^^^

Lists are supported using the YAML list syntax, for example::

  dependencies:
    compile:
    - org.metaborg:org.metaborg.meta.lang.esv:${metaborgVersion}
    - org.metaborg:org.metaborg.meta.lang.nabl:${metaborgVersion}
    - org.metaborg:org.metaborg.meta.lang.test:${metaborgVersion}

results in the ``dependencies.compile`` option being set to a list with elements:

- ``org.metaborg:org.metaborg.meta.lang.esv:${metaborgVersion}``
- ``org.metaborg:org.metaborg.meta.lang.nabl:${metaborgVersion}``
- ``org.metaborg:org.metaborg.meta.lang.test:${metaborgVersion}``

-------
Options
-------

All supported configuration options for projects are listed here.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
End-user project configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

An end-user project is a project that contains programs of languages, intended to be developed by an end-user of those languages.
The configuration for an end-user project specifies dependencies.


.. describe:: dependencies

   Compile and source dependencies to other language components, and dependencies to Java artifacts.

   .. describe:: compile

      List of compile dependencies to language components. A compile dependency to a language component indicates that this project uses files of that language, and as such its compiler should be invoked.

      - Format: List of language component identifiers (see ``id`` option)
      - Default: None
      - Example::

          dependencies:
            compile:
            - org.metaborg:org.metaborg.meta.lang.esv:${metaborgVersion}

   .. describe:: source

      List of source dependencies to language components. A source dependency to a language component indicates that this project uses exported files of that language or library.

      - Format: List of language component identifiers (see ``id`` option)
      - Default: None
      - Example::

          dependencies:
            source:
            - org.metaborg:org.metaborg.meta.lib.analysis:${metaborgVersion}


^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Language specification project configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A language specification projectis a project that contains a languages specification, which contain programs of meta-languages, intended to be developed by a language developer.
It is a specialization of an end-user project, so all configuration options from end-user projects listed above, can also be used in language specification projects.


The following configuration options are mandatory:

.. describe:: id

   Identifier of the language the language specification is describing.

   - Format: ``groupId:id:version`` where version uses the Maven version syntax; ``major.minor.patch(-qualifier)?``
   - Example: ``id: org.metaborg:org.metaborg.meta.lang.sdf:2.0.0-SNAPSHOT``

.. describe:: name

   Name of the language the language specification is describing.

   - Example: ``name: SDF``


The following configuration options are optional and revert to default values when not specified:

.. describe:: metaborgVersion

   Version of the MetaBorg tools to use.

   - Format: Maven version syntax (see ``id`` option)
   - Default: Current version of the running Spoofax
   - Example: ``metaborgVersion: 2.0.0-SNAPSHOT``

.. describe:: contributions

   List of language implementation identifiers the language component generated from this language specification contributes to.

   - Format: List of language implementation names and identifiers (see ``id`` option)
   - Default: Contribution to single language implementation with the same name and identifier of this language specification.
   - Example::

       contributions:
       - name: Green-Marl
         id: com.oracle:greenmarl:1.5.0-SNAPSHOT

.. describe:: generates

   List of language names this language specification generates files for, and into which directory.

   - Format: List of language name and directory.
   - Default: None
   - Example::

       generates:
       - language: EditorService
         directory: src-gen
       - language: Stratego-Sugar
         directory: src-gen

.. describe:: exports

   List of files and directories this language specification exports for use in other language components, and optionally to which language those files and directories belong. Exported resources are packaged into the language component artifact when built.

   - Format: List of exports. There are 3 kinds of exports which are described below
   - Default: None

   .. describe:: language-specific directory export

      A language-specific directory export, exports a directory with files of a specific language.
      The directory **must be relative** to the project root. Includes and excludes are relative to the specified directory.
      These files can be used by other language components by specifying a source dependency on the language component built from this language specification.

      - Format: Language name, path to directory, optional list of includes, and optional list of excludes
      - Example::

          exports:
          - language: TemplateLang
            directory: syntax
          - language: ds
            directory: src-gen/ds-signatures
          - language: Stratego-Sugar
            directory: trans
            includes: "**/*.str"
          - language: Stratego-Sugar
            directory: src-gen
            includes: "**/*.str"

      .. warning:: Includes and excludes are only used to package the correct resources into the language component artifact, Spoofax Core does not use the includes and excludes at this moment. This may cause differences in behaviour between development and deployment environments.

   .. describe:: language-specific file export

      A language-specific file export, exports a single file of a specific language.
      The file **must be relative** to the project root.
      The file can be used by other language components by specifying a source dependency on the language component built from this language specification.

      - Format: Language name, path to file
      - Example::

          exports:
          - language: SDF
            file: include/libanalysis2.def

   .. describe:: generic resource export

      A generic resource export, exports any resources in a directory.
      The directory **must be relative** to the project root. Includes and excludes are relative to the specified directory.
      These files can be used for tasks specific to the language specification, for example to bundle library files with the language specification.

      - Format: Relative path to directory, optional list of includes, and optional list of excludes
      - Example::

          exports:
          - directory: ./
            includes:
              - lib-java/**/*
              - lib-webdsl/**/*
              - lib/webdsl/HQL-pretty.pp.af
              - lib/webdsl/WebDSL-pretty.pp.af


   .. warning:: All paths are relative to the project root. Do **NOT** use ``${path:root}`` to make paths absolute!

   .. note:: For directory exports, a list of includes and excludes can be optionally specified, using the `Ant pattern syntax <https://ant.apache.org/manual/dirtasks.html#Patterns>`_. If no includes or excludes are specified, all files in the directory are assumed to be included recursively.

   .. note:: Use ``./`` to use the root directory as export directory, ``.`` triggers an error in the YAML parser.

.. describe:: pardonedLanguages

   List of language names that are pardoned; any errors they produce will not fail builds.

   - Format: List of language names
   - Default: None
   - Example::

       pardonedLanguages:
         - EditorService
         - Stratego-Sugar
         - SDF

.. describe:: language

   Language specific configuration options.

   .. describe:: sdf

      Configuration options for SDF2 and SDF3.

      .. describe:: version

         Version of SDF to use.

         - Format: Either ``sdf2`` or ``sdf3``.
         - Default: ``sdf3``
         - Example::

             language:
               sdf:
                 version: sdf2

      .. describe:: externalDef

         External SDF definition file to use.
         If this is specified, the ``language.sdf.version`` and ``language.sdf.args`` options are ignored, and all SDF2 or SDF3 syntax files are ignored.

         - Example::

             language:
               sdf:
                 externalDef: ${path:root}/syntax/Stratego-Sugar.def

      .. describe:: args

         List of additional arguments that are passed to ``pack-sdf`` when this language specification is built.

         - Format: List of command-line arguments.
         - Default: None
         - Example::

             language:
               sdf:
                 args:
                 - -Idef
                 - ${path:root}/lib/SDF.def

   .. describe:: stratego

      Configuration options for Stratego.

      .. describe:: format

         The output format of the ``strj`` compiler when this language specification is built.

         - Format: Either ``ctree`` or ``jar``.
         - Default: ``ctree``
         - Example::

               language:
                 stratego:
                   format: jar

      .. describe:: args

         List of additional arguments that are passed to strj when this language specification is built.

         - Format: List of command-line arguments.
         - Default: None
         - Example::

             language:
               stratego:
                 args:
                 - -la
                 - stratego-lib
                 - -la
                 - stratego-sglr
                 - -la

.. describe:: build

   List of additional build steps.

   - Format: List of build steps. There are 2 kinds of additional build steps which are described below. Each build step has a phase in which it is executed, which can be one of the following:

     - initialize: runs at the start of a build
     - generateSources: runs after compilers for all compile dependencies have generated source files
     - compile: runs after the build (i.e. pack-sdf, strj, etc. have been executed), but before compiling Java files
     - pkg: runs after Java files have been compiled, and after packaging the language component
     - clean: runs when the language specification is cleaned

   - Default: None

   .. describe:: stratego-cli (Stratego build step)

      Build step that runs a command-line Stratego application.

      - Format: phase, strategy to run, and command-line arguments
      - Example::

          build:
            stratego-cli:
            - phase: compile
              strategy: org.strategoxt.tools.main-parse-pp-table
              args:
              - -i
              - ${path:root}/lib/EditorService-pretty.pp
              - -o
              - ${path:root}/target/metaborg/EditorService-pretty.pp.af

   .. describe:: ant (Ant build step)

      Build step that runs a target from an Ant build script.

      - Format: phase, path to Ant build script, and target in the build script to execute
      - Example::

          build:
            ant:
            - phase: initialize
              file: ${path:root}/build.xml
              target: main

--------
Examples
--------

Our meta-languages and meta-libraries have configuration files which can be used as examples:

- `ESV <https://github.com/metaborg/esv/blob/master/org.metaborg.meta.lang.esv/metaborg.yaml>`_
- `SDF2 <https://github.com/metaborg/sdf/blob/master/org.metaborg.meta.lang.sdf/metaborg.yaml>`_
- `SDF3 <https://github.com/metaborg/sdf/blob/master/org.metaborg.meta.lang.template/metaborg.yaml>`_
- `Stratego <https://github.com/metaborg/stratego/blob/master/org.metaborg.meta.lang.stratego/metaborg.yaml>`_
- `NaBL <https://github.com/metaborg/nabl/blob/master/org.metaborg.meta.lang.nabl/metaborg.yaml>`_
- `TS <https://github.com/metaborg/ts/blob/master/org.metaborg.meta.lang.ts/metaborg.yaml>`_
- `Analysis library <https://github.com/metaborg/runtime-libraries/blob/master/org.metaborg.meta.lib.analysis/metaborg.yaml>`_
- `NaBL2 <https://github.com/metaborg/nabl/blob/master/org.metaborg.meta.lang.nabl2/metaborg.yaml>`_
- `Analysis library 2 <https://github.com/metaborg/runtime-libraries/blob/master/org.metaborg.meta.lib.analysis2/metaborg.yaml>`_
- `DynSem <https://github.com/metaborg/dynsem/blob/master/dynsem/metaborg.yaml>`_
