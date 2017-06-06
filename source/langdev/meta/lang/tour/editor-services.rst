.. highlight:: esv

=============================
Editor Services
=============================


Main.esv
--------------

main::

	module Main
	
	imports Syntax Analysis
	
	language
	
	  extensions : calc
	
	  provider : target/metaborg/stratego.ctree
	  //provider : target/metaborg/stratego.jar
	  provider : target/metaborg/stratego-javastrat.jar
	  
Syntax.esv
-------------------------
	  
syntax configuration::

	module Syntax
	
	imports 
	
	  libspoofax/color/default
	  completion/colorer/Calc-cc-esv
	
	language
	
	  table         : target/metaborg/sdf-new.tbl
	  start symbols : Program
	
	  line comment  : "//"
	  block comment : "/*" * "*/"
	  fences        : [ ] ( ) { }
	
	menus
	  
	  menu: "Syntax" (openeditor)
	    
	    action: "Format"          = editor-format (source)
	    action: "Show parsed AST" = debug-show-aterm (source)
	    
	views
	  
	  outline view: editor-outline (source)
	    expand to level: 3
	   

Transformation.esv
-------------------------------------

transformation configuration::

	module Transformation
	
	menus
	
	  menu: "Desugar" (openeditor)
	  
	    action: "Desugar" = desugar-pp (source)
	    action: "Desugar (AST)" = desugar-aterm (source)

Analysis.esv
-------------------------------------

analysis configuration::

	module Analysis
	
	imports
	
	  nabl2/Menus
	  nabl2/References
	
	language
	
	  observer : editor-analyze (constraint)
