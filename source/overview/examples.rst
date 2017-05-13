
====================================
Examples
====================================

Here we collect a list of (pointers to) languages developed with Spoofax. Not all projects have publicly available sources. Let us know if you know of more projects to list here.

MetaBorg
-----------------

Spoofax is bootstrapped; all meta-languages used in Spoofax are developed in Spoofax. You can find the repositories of these languages along with the Spoofax run-time system on the `MetaBorg <https://github.com/metaborg>`_ organization on github.
The  :ref:`introduction to Spoofax development <dev-intro>` section provides an overview of these repositories.

Spoofax in Education
----------------------

We use Spoofax in a `compiler construction course at TU Delft <https://tudelft-in4303-2016.github.io/>`_. The two main example languages used in that course are Mini Java and Tiger:

Mini Java
  An object-oriented example language, subset of Java. The sources are not published since our students need to produce this. But you can follow `the assignments <https://tudelft-in4303-2016.github.io/assignments/>`_.
   
Tiger
  A functional example language based on Appel's book. The `metaborg-tiger <https://github.com/MetaBorgCube/metaborg-tiger>`_ repository provides a complete definition of syntax in SDF3, static semantics in NaBL2, and dynamic semantics in DynSem.
  
PAPLJ
  Another subset of Java based on an assignment for Shriram Krishnamurthi's book on Programming and Programming Languages. (`Repository <https://github.com/MetaBorgCube/metaborg-papl>`_)

MetaBorgCube
-----------------

The `MetaBorgCube <https://github.com/metaborgcube>`_ github organization is a collection of language projects developed with Spoofax. (The projects are at different stages development and based on different versions of Spoofax. Some repositories are private; let us know if you are interested.) Here is a selection:
  
Simpl
  A small imperative language to demonstrate DynSem (`Repository <https://github.com/MetaBorgCube/simpl>`_)
  
QL/QLS
  Questionaire language used as example language in the language workbench challenge(`Repository <https://github.com/MetaBorgCube/metaborg-ql>`_)
  
Grace
  A programming language designed for programming education. The Spoofax project defines a syntax definition, desugaring, and operational semantics for the language. (`Repository <https://github.com/MetaBorgCube/metaborg-grace>`_)
    
Go
  A subset of the Go programming language with a translation to JavaScript (Private Repository)
  
IceDust
  a data modeling language (`Repository <https://github.com/MetaBorgCube/IceDust>`_)
  
Jasmin
  A Spoofax editor for Jasmin, an assembler for the Java Virtual Machine. (`Repository <https://github.com/MetaBorgCube/spoofax-jasmin>`_)
  
MetaC
  A version of the C programming language with modules and domain-specific language extensions (`Repository <https://github.com/MetaBorgCube/metac>`_)
  
Pascal
  A syntax and static semantics of the Pascal programming language (`Repository <https://github.com/MetaBorgCube/metaborg-pascal>`_)

    
Other Languages 
----------------------

WebDSL
  A web programming language <http://webdsl.org/>

Green-Marl
  A DSL for graph analysis developed at Oracle Labs for `running graph algorithms in PGX <https://docs.oracle.com/cd/E56133_01/latest/reference/overview/run.html>`_
  
PGQL `Property Graph Query Language <http://pgql-lang.org/>`_
  A DSL for graph querying developed at Oracle Labs as part of `Parallel Graph AnalytiX <https://docs.oracle.com/cd/E56133_01/latest/index.html>`_ framework. The Spoofax definition is part of the open source implementation (`Repository <https://github.com/oracle/pgql-lang>`_).

LeQuest
  A DSL for modeling medical equipment interfaces for development of training software.
  