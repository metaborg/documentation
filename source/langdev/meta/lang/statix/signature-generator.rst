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
* not use optional terms, such as :sdf3:`Decl.VarDecl = ID Type?`

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
To use these stratgies, import ``injections/-`` and call the ``explicate-injections-MyLang``
and ``implicate-injections-MyLang`` strategies for the analysis pre-processing and post-processing
respectively, where ``MyLang`` is the name of your language. For example, in ``trans/analysis.str``:

.. code-block:: stratego

   module analysis

   imports

     libspoofax/sdf/pp

     statixruntime
     statix/api

     injections/-

   rules

     editor-analyze = stx-editor-analyze(pre-analyze, post-analyze|"static-semantics", "programOk")
     pre-analyze = explicate-injections-MyLang
     post-analyze = strip-annos; implicate-injections-MyLang



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

