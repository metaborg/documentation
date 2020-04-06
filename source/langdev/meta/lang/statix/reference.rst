==================
Language Reference
==================

.. role:: doc-lex(code)
   :language: doc-lex
   :class: highlight

.. role:: statix(code)
   :language: statix
   :class: highlight

This section gives a systematic overview of the Statix language.

Lexical matters
---------------

Identifiers
^^^^^^^^^^^

.. code-block:: doc-lex

   lc-id = [a-z][a-zA-Z0-9\_]*
   uc-id = [A-Z][a-zA-Z0-9\_]*

Most identifiers in Statix fall into one of two categories, which we
will refer to as:

* *Lowercase identifiers*, that start with a lowercase character, and
  must match the regular expression :doc-lex:`[a-z][a-zA-Z0-9\_]*`.
* *Uppercase identifiers*, that start with an uppercase character, and
  must match the regular expression :doc-lex:`[A-Z][a-zA-Z0-9\_]*`.

Comments
^^^^^^^^

Comments in Statix follow the C-style:

* ``// ... single line ...`` for single-line comments
* ``/* ... multiple lines ... */`` for multi-line comments

Multi-line comments can be nested, and run until the end of the file
when the closing ``*/`` is omitted.

Terms and patterns
------------------

.. code-block:: doc-lex

   term = uc-id "(" {term ","}* ")"
        | "(" {term ","}* ")"
        | "[" {term ","}* "]"
        | "[" {term ","}* "|" term "]"
        | int
        | str
        | namespace-id? "{" {term ", "}* ("@" var-id)? "}"
        | var-id

   pattern = uc-id "(" {pattern ","}* ")"
           | "(" {pattern ","}* ")"
           | "[" {pattern ","}* "]"
           | "[" {pattern ","}* "|" pattern "]"
           | int
           | str
           | var-id
           | "_"

    int = [1-9][0-9]*
    str = "\"" ([^\"\\]|"\\"[nrt\\])* "\""

    position = "-"
             | var-id
             | "_"

Modules
-------

.. code-block:: doc-cf-[

   module [module-id]

     [section*]
 
NaBL2 specifications are organized in modules. A module is identified
by a module identifier. Module identifiers consist of one or more
names seperated by slashes, as in :doc-lex:`{name "/"}+`. The names
must match the regular expression
:doc-lex:`[a-zA-Z0-9\_][a-zA-Z0-9\_\.\-]*`.

Every module is defined in its own file, with the extensions
``.stx``. The module name and the file paths must coincide.

*Example.* An empty module ``analysis/main``, defined in a file
:file:`.../analysis/main.nabl2`.

.. code-block:: statix

   module analysis/main

   // work on this

Modules consist of sections for imports, signatures, and rule
definitions. The rest of this section describes imports, and
subsequents sections deal with signatures and rules.

Imports
^^^^^^^
 
.. code-block:: doc-cf-[

  imports

    [module-ref*]

A module can import definitions from other modules be importing the
other module. Imports are specified in an ``imports`` section, which
lists the modules being imported. A module reference can be:

* A module identifier, which imports a single module with that name.
* A wildcard, which imports all modules with a given prefix. A
  wildcard is like a module identifier, but with a dash as the last
  part, as in :doc-lex:`{name "/"}+ "/-"`.

A wildcard import does not work recursively. For example,
``analysis/-`` would imports ``analysis/functions``, and
``analysis/classes``, but not ``analysis/lets/recursive``.

*Example.* A main module importing several submodules.

.. code-block:: statix

   module main

   imports

      builtins
      functions/-
      classes/-
      types

Signatures
----------

.. code-block:: doc-cf-[

  signatures

    [signature*]

Terms
^^^^^

Sorts
"""""

Constructors
""""""""""""

Name binding
^^^^^^^^^^^^

Relations
"""""""""

Namespaces
""""""""""

Name resolution
"""""""""""""""

Rules
^^^^^

.. code-block:: doc-cf-[

   constraint generator

     [rule-def*]


Predicat rules
^^^^^^^^^^^^^^

Functional rules
^^^^^^^^^^^^^^^^

Mapping rules
^^^^^^^^^^^^^

Constraints
-----------

Base constraints
^^^^^^^^^^^^^^^^

Term equality
^^^^^^^^^^^^^
    
Name binding
^^^^^^^^^^^^

Scope graph
"""""""""""

Queries
"""""""

Occurrences
"""""""""""

Arithmetic
^^^^^^^^^^

Misc notes
----------

Error messages
^^^^^^^^^^^^^^

