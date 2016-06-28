=============
Configuration
=============

The REPL supports the configuration of any language with a DynSem
specification. The configuration consists of three parts: the
(optional) extension of the syntax, the configuration in the ESV, and
the creation of DynSem rules specific to the REPL. We explain each
part of the configuration with a running example.

Extending the syntax definition
-------------------------------
Sometimes a language has a slightly different syntax inside the
context of a REPL. For example, Haskell's GHCi has the ``let x =
<expression>`` syntax for defining new variables and functions. In our
example, we try to replicate the same behavior for our REPL.

To extend the syntax, we use a new start symbol called ``Shell``, and
specify a grammar rule for it as shown below.

.. code-block:: sdf3
   :linenos:

   context-free start-symbols
     // Define it as start symbol.
     Prog Shell

   context-free syntax
     // Syntax for the Shell.
     Shell.Let = <let <ID> = <Exp>> {non-assoc}

The start symbol is also specified in the ESV configuration of the
REPL, which will be explained in the next section.

ESV configuration
-----------------

The ESV configuration of the REPL supports setting two properties: the
evaluation method and the start symbol that is used inside of the
REPL.

.. code-block:: esv
   :linenos:

   module Shell

   shell
     evaluation method  : "dynsem"
     shell start symbol : Shell

When the user entered an expression, the REPL first tries to parse
using the start symbol as configured above. If that fails, it uses the
ordinary start symbol as a fallback.

Extending the DynSem specification
----------------------------------

To allow expressions to be evaluated in the context of previous
evaluations, one has to extend one's DynSem specification with two
kinds of REPL-specific rules. The first is a rule for initializing the
execution environment for the REPL, shown below. The second are the
rules for implementing REPL-specific semantics.

.. note:: This section assumes basic knowledge of DynSem, and that
	  your language already has a DynSem specification. To learn
	  more about DynSem, refer to the
	  :ref:`DynSem documentation <dynsemdocumentation>`.

The initialization rule
~~~~~~~~~~~~~~~~~~~~~~~

The initialization rule shown below is evaluated upon the first
evaluation done after starting up the REPL. It instantiates the
semantic components that form the execution environment for the REPL:
an environment with an initial variable binding of :math:`x \mapsto
4`, and an empty store. The REPL uses and updates the semantic
components in its successive evaluations.

.. code-block:: dynsem
   :linenos:

   signature

     sorts
       ShellInit

     constructors
       ShellInit : ShellInit

     arrows
       // Note: the ShellInit rule must have this exact signature.
       ShellInit -init-> ShellInit

   rules
     // Initialization of shell state: an environment with "x" bound to 4,
     // and an empty store.
     ShellInit() -init-> ShellInit() :: Env { "x" |--> NumV(4) }, Store {}.

The rule must have the exact signature as shown above. That is, the
sort must be of the name ``ShellInit``, with an arity of
zero. Furthermore, the input of the rule must be ``ShellInit``, and
its name must be ``init``. The result value of the rule can be
anything, as it is discarded. The only part of the result of this rule
that is used by the REPL are the read-write semantic components (in
this case, the environment and the store).

REPL-specific semantics
~~~~~~~~~~~~~~~~~~~~~~~

The second kind of configuration are the rules for the REPL-specific
semantics. These can be seen as entry points for the REPL to the
interpreter. The rules are all named ``shell``, so that they are
distinct of the ordinary semantics. An example of such a rule is shown
below: it implements binding the result of an expression to a
variable. This rule specifies the dynamic semantics of the
REPL-specific syntax that we made earlier in this section. With the
specification of this rule, the bound variable can be used in
successive evaluations done by the user of the REPL.

.. code-block:: dynsem
   :linenos:

   signature
     arrows
       Expr -shell-> V

   rules
     // let x = 2
     Let(x, e) :: E -shell-> v :: E'
     where
       E |- e :: Store {} --> v :: Store _;
       E |- bindVar(x, v) --> E'.

Note that the environment ``E`` is passed as a *read-write* component,
instead of a *read-only* component. This is because in this case the
environment *should* be writable, since the resulting environment
after execution should be available to the REPL. In line 9, the
original specification is recursively invoked.
