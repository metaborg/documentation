
.. raw:: html
	
	<a href="https://github.com/metaborgcube/metaborg-calc"><img style="position: absolute; top: 0; right: 0; border: 0;" src="https://camo.githubusercontent.com/e7bbb0521b397edbd5fe43e7f760759336b5e05f/68747470733a2f2f73332e616d617a6f6e6177732e636f6d2f6769746875622f726962626f6e732f666f726b6d655f72696768745f677265656e5f3030373230302e706e67" alt="Fork me on GitHub" data-canonical-src="https://s3.amazonaws.com/github/ribbons/forkme_right_green_007200.png"></a>

=============================================
Language Definition with Spoofax
=============================================

In this chapter we make a complete tour of language definition in Spoofax using Calc, a small calculator language, as example. 
In the sections of this chapter we define all aspects of the Calc language, including its concrete syntax, static semantics, dynamic semantics, testing, and configuration of the IDE.
The source code of the language definition is available on
`github <https://github.com/MetaBorgCube/metaborg-calc>`_.
You can follow along by forking `the project <https://github.com/MetaBorgCube/metaborg-calc>`_ and building it in Spoofax.

The Calc language supports the following features

- Arithmetic with integer and floating point numbers with arbitrary precision
- Boolean values and boolean operators 
- First-class (but non-recursive) polymorphic functions
- Variable bindings through top-level definitions and let bindings in expressions
- Type inference provides static type checking without explicit type annotations

The following Calc program calculates the monthly payments for a mortgage (according to `Wikipedia <https://en.wikipedia.org/wiki/Mortgage_calculator>`_)::

	monthly = \r Y P.
	  let N = Y * 12 in // number of months
	   if(r == 0) // no interest
	     P / N
	   else 
	     let rM = r / (100 * 12) in // monthly interest rate
	     let f = (1 + rM) ^ N in
	       (rM * P * f) / (f - 1);		  			   
		    
	r = 1.7;     // yearly interest rate (percentage)   
	Y = 30;      // number of years  
	P = 385,000; // principal 	
	
	monthly r Y P;  
	

At the end of the chapter we give a list of exercises with ideas for extending the language. Those may be a good way to further explore the capabilities of Spoofax before venturing out on your own.
If you do make one of those extensions (or another one for that matter), we would welcome pull requests for branches of the project.

Note that this is not an introduction to formal language theory, compiler construction, concepts of programming languages. 
Nor is this chapter an exhaustive introduction to all features of Spoofax.

.. toctree::
   :maxdepth: 1
   :numbered: 2
   :caption: Table of Contents
   
   syntax
   abstract-syntax
   transformation
   static-semantics
   dynamic-semantics
   editor-services
   testing
   exercises