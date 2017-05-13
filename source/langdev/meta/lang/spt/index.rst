.. _spt-index:

=================================
Language Testing with SPT
=================================

The SPoofax Testing language (SPT) allows language developers to test their language in a declarative way.
It offers a language to express test cases for any textual language that you want to test, and a framework for executing those tests on language implementations created with Spoofax.

We will first describe the syntax and semantics of the SPT language.
Then, we will discuss how you can execute your SPT test cases, and finally we conclude with an overview of the architecture of the SPT framework.

In this section we will describe the syntax and semantics of SPT.

If you want to write your own tests you can follow along as the different concepts are explained.
We suggest using the Spoofax Eclipse plugins, as they contain an editor for SPT files.
In an Eclipse with Spoofax installed, simply create a new file with the extension ``.spt`` and follow along to create your first SPT test suite.


.. toctree::
   :maxdepth: 1
   :numbered: 2
   
   test-suites
   test-expectations
   running-tests
   spt