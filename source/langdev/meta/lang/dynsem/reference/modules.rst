-----------------
Modules
-----------------

DynSem specifications can be split over multiple files. Every file constituted a **module**. Every module begins with a module declaration and optionally provides subsections:

.. code-block:: dynsem

  module trans/semantics/mymodule

  IMPORTS*

  SIGNATURE*

  RULES*

The name of the module must consist of the path to its file relative to the root of the project, followed by the file name without the *.ds* extension. The example above declares the module ``mymodule`` in the file *mymodule.ds* which is located at ``trans/semantics/`` relative to the project root.

~~~~~~~~~~~~~~~~~
Importing modules
~~~~~~~~~~~~~~~~~

Modules can import other modules using one or more **imports** sections. The module below imports modules ``A``, ``B`` and ``C``, and shows that multiple modules can be imported at once and that an **imports** section can appear anywhere in the module:

.. code-block:: dynsem

  module trans/semantics/mymodule

  imports
    trans/semantics/A
    trans/semantics/B

  rules
    ...

  imports
    trans/semantics/C


The semantics of imports are those of the `C include directive`_, i.e. imports are includes and they are transitive. All signatures and rules defined in (transitively) imported modules are visibile for the importing module. Cyclic imports are automatically resolved.

.. _C include directive: https://en.wikipedia.org/wiki/Include_directive#C.2FC.2B.2B

~~~~~~~~~~
Signatures
~~~~~~~~~~

A module may have any number of **signature** sections. Signatures are used to declare sorts, constructors, components and arrows. See :ref:`dynsemtermsignatures` for defining sorts and constructors, and :ref:`dynsemarrowsignatures` for defining components, arrows and other operations.

~~~~~
Rules
~~~~~

Multiple **rules** sections are permitted in a DynSem module. Each rule section declares arbitrarily many reduction rules. See :ref:`dynsemrules` about defining reduction rules and the constructs supported.
