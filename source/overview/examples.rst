
====================================
Examples
====================================

Here we collect a list of (pointers to) languages developed with Spoofax. Not all projects have publicly available sources. Let us know if you know of more projects to list here.

MetaBorg
-----------------

Spoofax is bootstrapped; all meta-languages used in Spoofax are developed in Spoofax. You can find the repositories of these languages along with the Spoofax run-time system on the `MetaBorg <https://github.com/metaborg>`_ organization on github.
The  :ref:`introduction to Spoofax development section <dev-intro>` provides an overview of these repositories.

Spoofax in Education
----------------------

We use Spoofax in a `compiler construction course at TU Delft <https://tudelft-in4303-2016.github.io/>`_. The two main example languages used in that course are Mini Java and Tiger:

Mini Java
  An object-oriented example language, subset of Java. The sources are not published since our students need to produce this. But you can follow `the assignments <https://tudelft-in4303-2016.github.io/assignments/>`_.
   
Tiger
  A functional example language based on Appel's book. The `metaborg-tiger <https://github.com/MetaBorgCube/metaborg-tiger>`_ repository provides a complete definition of syntax in SDF3, static semantics in NaBL2, and dynamic semantics in DynSem.

MetaBorgCube
-----------------

The `MetaBorgCube <https://github.com/metaborgcube>`_ github organization is a collection of language projects developed with Spoofax. Here is a selection:

Jasmin
  A Spoofax editor for Jasmin, an assembler for the Java Virtual Machine. (`Repository <https://github.com/MetaBorgCube/spoofax-jasmin>`_)
  
IceDust
  a data modeling language https://github.com/MetaBorgCube/IceDust
  
Simpl
  A small imperative language to demonstrate DynSem (`Repository <https://github.com/MetaBorgCube/simpl>`_)
  
Grace
  A programming language designed for programming education. The Spoofax project defines a syntax definition, desugaring, and operational semantics for the language. (`Repository <https://github.com/MetaBorgCube/metaborg-grace>`_)

Other Projects 
----------------------

Green-Marl
  A DSL for graph analysis developed at Oracle Labs for `running graph algorithms in PGX <https://docs.oracle.com/cd/E56133_01/latest/reference/overview/run.html>`_
  
PGQL `Property Graph Query Language <http://pgql-lang.org/>`_
  A DSL for graph querying developed at Oracle Labs as part of `Parallel Graph AnalytiX <https://docs.oracle.com/cd/E56133_01/latest/index.html>`_ framework. The Spoofax definition is part of the open source implementation <https://github.com/oracle/pgql-lang>.

LeQuest
  A DSL for modeling medical equipment interfaces for development of training software.
  