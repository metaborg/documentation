.. _statix-signature-generator:

===================
Signature Generator
===================

.. role:: statix(code)
   :language: statix
   :class: highlight

.. role:: stratego(code)
   :language: stratego
   :class: highlight

.. role:: sdf3(code)
   :language: sdf3
   :class: highlight

It is quite cumbersome to write Statix signatures. Thankfully,
the ``sdf3.ext.statix`` project can generate these signatures for you.

Well-Formed SDF3 Requirements
-----------------------------
For the generator to work correctly, your SDF3 must be well formed. In particular, you must:

* explicitly declare each sort *exactly once* in your project
* declare lexical sorts in a ``lexical sorts`` block
* declare context-free sorts in a ``context-free sorts`` block
* for every use of a sort: either have a local declaration of a sort, or an import of a file that declares the sort
* not declare sorts that are not used in any rules
* not use any implicitly declared sorts
* not use complex injections, such as :sdf3:`Pair = Expr Expr`
* not use ``sdf2table: c``

The generator generates strategies and signatures for each explicit declaration
of a sort in SDF3, which is why each sort must be declared exactly once.
SDF3 does not generate Stratego signatures for placeholders for sorts that have
no corresponding rules, causing errors in the generated Statix injection
explication strategies.
Complex injections are not supported across Spoofax.
Optional sorts cannot be represented in Statix.



Applying the Generator in Spoofax 2
-----------------------------------

In your language project's ``metaborg.yaml`` file, change your compile dependencies
to include ``org.metaborg:sdf3.ext.statix``. For example:

.. code-block:: yaml

   dependencies:
     compile:
     - org.metaborg:org.metaborg.meta.lang.esv:${metaborgVersion}
     - org.metaborg:org.metaborg.meta.lang.template:${metaborgVersion}
     - org.metaborg:sdf3.ext.statix:${metaborgVersion}

.. pull-quote::

   *Note*: Clean the project and restart Eclipse when changing the ``metaborg.yaml`` file.

Once you clean your project, the extension automatically generates the following:

* Statix signatures declarations (in ``src-gen/statix/signatures/``)
* Stratego strategies for explicating and removing injections (in ``src-gen/injections/``)


Using the Generated Injection strategies
----------------------------------------
The generator generates strategies for explicating and removing injections.
This is unfortunately needed since Statix does not support injections directly.
To use these strategies, import ``injections/-`` and call the ``explicate-injections-MyLang-Start``
and ``implicate-injections-MyLang-Start`` strategies for the analysis pre-processing and post-processing
respectively, where ``MyLang`` is the name of your language and ``Start`` is your language's start
symbol (as specified in ``Syntax.esv``). For example, in ``trans/analysis.str``:

.. code-block:: stratego

   module analysis

   imports

     libspoofax/sdf/pp

     statixruntime
     statix/api

     injections/-

   rules

     editor-analyze = stx-editor-analyze(pre-analyze, post-analyze|"static-semantics", "programOk")
     pre-analyze  = explicate-injections-MyLang-Start
     post-analyze = implicate-injections-MyLang-Start



Using the Generated Signatures
------------------------------
Using the generated Statix signatures is quite simple: just import them into your Statix specification.
Each SDF3 file gets an associated Statix file with the signatures. For example, if your syntax is
defined across two files named ``MyLang.sdf3`` and ``Common.sdf3``, then in Statix you should
add the following imports:

.. code-block:: statix

   imports
     signatures/MyLang-sig
     signatures/Common-sig

Because Statix does not support injections, you have to use explicit constructor names for injections.
For example, the following SDF3 syntax:

.. code-block:: sdf3

   context-free sorts
     Stmt VarName

   lexical sorts
     ID

   context-free syntax
     Stmt.VarDecl = <var <VarName>;>
     VarName.Wildcard = <_>
     VarName = ID

   lexical syntax
     ID = [a-zA-Z] [a-zA-Z0-9\_]* 

   lexical restrictions
     ID -/- [a-zA-Z0-9\_]
   
would approximately produce the following signatures:

.. code-block:: statix

   module signatures/Test-sig

   imports

   signature
     sorts
       Stmt
       VarName
       ID = string
     constructors
       Stmt-Plhdr : Stmt
       VarName-Plhdr : VarName

   signature
     constructors
       VarDecl : VarName -> Stmt
       Wildcard : VarName
       ID2VarName : ID -> VarName

Now, in Statix if you just want to capture the term of sort ``VarName`` in the
``VarDecl`` constructor, this would suffice:

.. code-block:: statix

  VarDecl(x)

But if you want to match the term only if it has the sort ``ID``, then you have
to use the explicit injection constructor name ``ID2VarName``:

.. code-block:: statix

  VarDecl(ID2VarName(x))

In this example, ``ID`` is a lexical sort, so it is an alias for ``string``
in the Statix specification.



Troubleshooting
---------------

Calls non-existing
~~~~~~~~~~~~~~~~~~
Build fails with errors such as this:

.. code-block:: none

    [ strj | error ] *** ("is-MyLang-MySort-or-inj",0,0) calls non-existing ("is-MyLang-ID-or-inj",0,0)
    [ strj | error ] *** ("explicate-injections-MyLang-MySort",0,0) calls non-existing ("explicate-injections-MyLang-ID",0,0)
    [ strj | error ] *** ("implicate-injections-MyLang-MySort",0,0) calls non-existing ("implicate-injections-MyLang-ID",0,0)
    Executing strj failed: {}
    Failing builder was required by "Generate sources".
    BUILD FAILED

To solve this, ensure you have declared ``ID`` (in this example) as a ``lexical sort``
in your syntax, and make sure that the syntax file with rules for ``MySort``
that reference ``ID`` import the syntax file that declares ``ID``.


Transformation failed unexpectedly
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Clean or build fails with an error such as this:

.. code-block:: none

    ERROR: Optional sorts are not supported by Statix: Opt(Sort("MySort"))
    Transformation failed unexpectedly for eclipse:///mylang/syntax/mysyntax.sdf3
    org.metaborg.core.transform.TransformException: Invoking Stratego strategy generate-statix failed at term:
      CfSignature("MySort", Some("MyCons"), [ Param(Opt(Sort("MySort")), "mySort") ])
    Stratego trace:
      generate_statix_0_0
      generate_statix_abstract_0_0
      geninj_generate_statix_0_0
      geninj_module_to_sig_0_0
      with_1_1
      flatfilter_1_0
      filter_1_0
      with_1_1 <==
      map_1_0
      geninj_symbol_to_stxsig_0_0
    Internal error: 'with' clause failed unexpectedly in 'geninj-sig-to-stxsig'

Note the first line with ``ERROR``, it tells you that something is not supported.
In this case, the use of optional sorts such as ``MySort?`` is not supported
by Statix and the Statix signature generator.

To solve this, rewrite a syntax rule with an optional sort such as:

.. code-block:: sdf3
    
    Stmt.VarDecl    = <<Type?> <ID> = <Exp>>

Into a rule with an explicit sort:

.. code-block:: sdf3

    Stmt.VarDecl    = <<Type-OPT> <ID> = <Exp>>
    Type-OPT.NoType = <>
    Type-OPT        = Type

Note that the ``-OPT`` suffix has no special meaning. You can name
the sort differently, such as ``OptionalType``.


Constructor MySort-Plhdr/0 not declared
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Buid fails with an error such as this:

.. code-block:: none

    [ strj | error ] in rule explicate-injections-MyLang-MySort(0|0): constructor MySort-Plhdr/0 not declared
    -     MySort-Plhdr()
    Executing strj failed: {}
    BUILD FAILED

You have declared a sort for which you don't have any rules. Remove the sort
from the ``context-free sorts`` or ``sorts`` block.

No pp entry found, cannot rewrite to box
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Clean fails with an error such as this:

.. code-block:: none

    [ identity crisis | error ] No pp entry found for: (1,["declSortLex"])
    - [ identity crisis | error ] Cannot rewrite to box: 
    -         declSortLex("MySort")

You are using the old ``sdf2table: c``. Change this in ``metaborg.yaml`` into
``sdf2table: java``.
