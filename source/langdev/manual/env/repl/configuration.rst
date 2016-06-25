=============
Configuration
=============

The REPL supports the configuration of any language with a DynSem
specification. The configuration consists of two parts: the
configuration in the ESV, and the creation of DynSem rules specific to
the REPL.

ESV configuration
-----------------

The ESV configuration of the REPL supports setting two properties: the
evaluation method and the start symbol that is used inside of the
REPL.

.. code-block:: esv

   module Shell

   shell
       evaluation method  : "dynsem"
       shell start symbol : Expr

When the user entered an expression, the REPL first tries to parse
using the start symbol as configured above. If that fails it, uses the
default start symbol as specified in the ESV as a fallback.
