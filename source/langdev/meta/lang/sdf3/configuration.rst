.. _sdf3-configuration:

SDF3 Configuration
------------------

When using SDF3 inside Spoofax, it is possible to specify different configuration options that. They allow
using the new parser generator, specifying the shape of completion placeholders, or disable
SDF altogether. These options should be specified in the :file:`metaborg.yaml` file.

For example, to disable SDF for the current project, use:

.. code-block:: yaml

   language:
       sdf:
         enabled: false

This configuration should be present when defining language components for a language that has SDF enabled.

SDF3 allows generating placeholders for code completion. The default "shape" of placeholders is ``[[Symbol]]``. However, it is possible
to tweak this shape using the configuration below (the configuration for suffix is optional):

.. code-block:: yaml

   language:
     sdf:
       placeholder:
         prefix: "$"
         suffix: "$"

Currently, the path to the parse table is specified in the :file:`Syntax.esv` file, commonly as ``table: target/metaborg/sdf.tbl``.
When the ESV file does not contain this entry, it is also possible to specify the path to the parse table in the :file:`metaborg.yaml` file.
This is useful when testing an external parse table, or using a parse table different from the one being generated in the project.
In the example below, the table is loaded from the path ``tables/sdf.tbl``. The same can be applied to the parse table used for code completion.

.. code-block:: yaml

   language:
     sdf:
       parse-table: "tables/sdf.tbl"
       completion-parse-table: "tables/sdf-completions.tbl"

In a Spoofax project, it is also possible to use SDF2 instead of SDF3. This enables SDF2 tools such as the SDF2 parenthesizer,
signature generator, etc. For example:

.. code-block:: yaml

   language:
     sdf:
       version: sdf2


Finally, by default SDF3 compilation works by generating SDF2 files, and depending on the SDF2 toolchain. However,
a new (and experimental) parse table generator can be selected by writing:

.. code-block:: yaml

   language:
     sdf:
       sdf2table: java

This configuration disables the SDF2 generation, and may cause problems when defining grammars to use concrete syntax, since
this feature is not supported yet by SDF3.
However, the ``java`` parse table generator supports Unicode, whereas SDF2 generation does not.
Furthermore, ``dynamic`` can be used instead of ``java``, to enable lazy parse table
generation, where the parse table is generated while the program is parsed.

JSGLR version
=============

An experimental new version of the SGLR parser implementation is available: JSGLR2. It supports parsing, imploding and
syntax highlighting. Error reporting, recovery and completions are currently not supported. It can be enabled with:

.. code-block:: yaml

   language:
     sdf:
       jsglr-version: v2

There are some extensions of JSGLR2 available. To use them, set the ``jsglr-version`` option to one of the following:

:``data-dependent``:       Data-dependent JSGLR2 solves deep priority conflicts using data-dependent parsing, which does
                           not require duplicating the grammar productions.
:``incremental``:          Incremental JSGLR2 reuses previous parse results to speed up parsing.
:``layout-sensitive``:     Layout-sensitive JSGLR2 is documented in the
                           `reference manual of SDF3 <reference.html#layout-sensitive-parsing>`_.
:``recovery``:             JSGLR2 with recovery tries to recover from parse errors. This extension is experimental and
                           only available in the development version of Spoofax.
:``recovery-incremental``: Incremental JSGLR2 with recovery. This extension is experimental and only available in the
                           development version of Spoofax.

JSGLR2 logging
==============

Logging is available for JSGLR2. It can be enabled with:

.. code-block:: yaml

   language:
     sdf:
       jsglr2-logging: all

Since logging all parsing events is quite verbose, several other scopes are available in addition to the ``all`` option:

:``none``: Log nothing (default).
:``minimal``: Only log the start and end of a parse, including a measurement of total parse time (including imploding and tokenization).
:``parsing``: Log all standard parsing events (such as stack and parse forest operations, action execution, etc.) but no variant-specific events (e.g. related to recovery).
:``recovery``: Log the recovery iterations and the recovery productions that are applied.

.. warning:: Whenever changing any of these configurations, clean the project before rebuilding.

.. TODO: write documentation on how to use SDF3 outside of Spoofax
