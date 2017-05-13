
====================================
Examples
====================================

Here we collect a list of (pointers to) languages developed with Spoofax. Not all projects have publicly available sources. Let us know if you know of more projects to list here.

MetaBorg: Bootstrapping Spoofax
-----------------------------------

Spoofax is bootstrapped; all meta-languages used in Spoofax are developed in Spoofax. You can find the repositories of these languages along with the Spoofax run-time system on the `MetaBorg <https://github.com/metaborg>`_ organization on github.
The  :ref:`introduction to Spoofax development <dev-intro>` section provides an overview of these repositories.


Spoofax in Production
-------------------------

Spoofax is used for the development of several languages that are used in the production of software systems.

WebDSL
  A web programming language <http://webdsl.org/>
  
IceDust
  A data modeling language supporting relations, multiplicities, derived values and configurable strategies for calculation of derived values <https://github.com/MetaBorgCube/IceDust>
 
Green-Marl
  A DSL for graph analysis developed at Oracle Labs for `running graph algorithms in PGX <https://docs.oracle.com/cd/E56133_01/latest/reference/overview/run.html>`_
  
PGQL `Property Graph Query Language <http://pgql-lang.org/>`_
  A DSL for graph querying developed at Oracle Labs as part of `Parallel Graph AnalytiX <https://docs.oracle.com/cd/E56133_01/latest/index.html>`_ framework. The Spoofax definition is part of the open source implementation <https://github.com/oracle/pgql-lang>.

LeQuest
  A DSL for modeling medical equipment interfaces for development of training software. This is a proprietary language.
  
  
Spoofax in Education
------------------------

We use Spoofax in education at TU Delft in a master's course `compiler construction course <https://tudelft-in4303-2016.github.io/>`_ and in a bachelor course on concepts of programming languages. The two main example languages used in that course are Mini Java and Tiger:

Mini Java
  A subset of the object-oriented Java language defined as assignment in Appel's book. The sources are not published since our students need to produce this. But you can follow `the assignments <https://tudelft-in4303-2016.github.io/assignments/>`_.
   
Jasmin
  A Spoofax editor for Jasmin, an assembler for the Java Virtual Machine, which is used as target language for the Mini Java compiler. <https://github.com/MetaBorgCube/spoofax-jasmin>
  
Tiger
  A functional language used as example in the ML edition of Appel's book. The `metaborg-tiger <https://github.com/MetaBorgCube/metaborg-tiger>`_ repository provides a complete definition of syntax in SDF3, static semantics in NaBL2, and dynamic semantics in DynSem.
  
PAPLJ
  Another subset of Java based on an assignment for Shriram Krishnamurthi's book on Programming and Programming Languages. <https://github.com/MetaBorgCube/metaborg-papl>
  
  
MetaBorgCube
-----------------

The `MetaBorgCube <https://github.com/metaborgcube>`_ github organization is a collection of language projects developed with Spoofax. These are often research or demonstration projects exploring (some aspect of) language definition with Spoofax. The projects are (stuck) at different stages of development, not necessarily using the latest version of Spoofax, and at different stages of maintenance (decay). Consider these projects as inspiration rather than as a source of working code. Some repositories are private; let us know if you are interested. Here is a selection:
  
Simpl
  A small imperative language to demonstrate DynSem <https://github.com/MetaBorgCube/simpl>
  
QL/QLS
  Questionaire language used as example language in the language workbench challenge <https://github.com/MetaBorgCube/metaborg-ql>
  
Grace
  A programming language designed for programming education. The Spoofax project defines a syntax definition, desugaring, and operational semantics for the language. <https://github.com/MetaBorgCube/metaborg-grace>
    
Go
  A subset of the Go programming language with a translation to JavaScript (Private Repository)
  
MetaC
  A version of the C programming language with modules and domain-specific language extensions <https://github.com/MetaBorgCube/metac>
  
Pascal
  A syntax and static semantics of the Pascal programming language <https://github.com/MetaBorgCube/metaborg-pascal>

    

  