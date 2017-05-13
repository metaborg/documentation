
Generating Scala case classes from SDF3 grammars
------------------------------------------------

.. warning :: This feature is experimental and may result in Stratego
              errors during the generation process and/or invalid Scala
              code in the generated files.

SDF3 generates Stratego signatures of AST nodes that the parser uses. A
new addition is the generation of Scala case classes that are similar in
structure to such AST nodes. These Scala files can be generated using
the menu entry
``Spoofax > Generate > Signature > Generate Scala Signatures``. The
files are generated in ``src-gen/signatures/scala-signatures/``.

You can now copy the generated Scala files to a separate maven project.
The files use a spoofax-scala interop library called
``org.metaborg.scalaterms``. Take a look at the generated code for hints
on useful patterns.

This Scala maven project should generate a jar that you can then use in
your Spoofax project as a provider. That will allow you to connect it to
your Spoofax project with Stratego. You write a tiny amount of Java to
register an external strategy, which immediately calls into the Scala
code. The interop library also has more classes to help with turning
Java ATerms from Stratego into a handier structure in Scala. That in
turn should help you write Scala code that can be used as a ``Strategy``
implementation for such strategies as ``editor-analyze``,
``editor-hover`` or ``editor-resolve``.

Name mangling
~~~~~~~~~~~~~

There is a small amount of name mangling used so the namespaces from
SDF3 don't conflict when they are merged into Scala's class namespace:

-  Module names get an `M` prefixed and `-` are removed
-  Sort names get an `S` prefixed
-  Constructor names get their arity appended
-  Field names in constructors are the lowercased sort name combined
   with the index in the list of children. SDF labels are currently
   ignored. Feel free to contribute support for this.

Known issues
~~~~~~~~~~~~

The following result in Scala code that doesn't compile:

-  Defining a context-free sort equals a lexical sort without wrapping
   it in a constructor.
-  Defining parts of the same sort in different files.
-  Defining injections (`sort1 = sort2`) where the sorts are not all
   in the same file. (Can be fixed by putting the generated Scala in
   one file).
-  Please [report](yellowgrass.org/createIssue/SpoofaxWithCore) any
   other issues you have.