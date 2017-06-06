.. highlight:: stratego

=============================
Transformation
=============================

transformation::

	module desugar
	
	imports signatures/-
	
	strategies
	
	  desugar-calc = topdown(try(desugar))
	  
	rules
	
	  desugar : Min(e) -> Sub(Num("0"), e)
	  
	  desugar : Neq(e1, e2) -> Not(Eq(e1, e2)) 
	  desugar : Gt(e1, e2) -> Lt(e2, e1)
	
	  desugar : Not(e) -> If(e, False(), True())
	  desugar : And(e1, e2) -> If(e1, e2, False())
	  desugar : Or(e1, e2) -> If(e1, True(), e2)
	  
	  desugar : Fun([x | xs@[_|_]], e) -> Fun([x], Fun(xs, e))
	  
	  desugar : Num(i) -> Num(j) 
	    where <explode-string; filter(not(?44)); implode-string> i => j
	  