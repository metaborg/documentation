.. highlight:: nabl2

=============================
Static Semantics
=============================

foobar::

	module statics/calc
	
	imports signatures/- 
	
	rules 
	
	  init ^ (s) := new s.
	
	  [[ Program(stats) ^ (s) ]] := 
	    new s', s' ---> s,
	    Stats[[ stats ^ (s') ]].
	  
	  Stats[[ [] ^ (s) ]].
	  
	  Stats[[ [ stat | stats ] ^ (s) ]] :=
	    Stat[[ stat ^ (s, s_nxt) ]],
	    Stats[[ stats ^ (s_nxt) ]].
	    
	  Stat[[ Bind(x, e) ^ (s, s') ]] := 
	    s' == s_nxt,
	    new s_nxt, s_nxt ---> s,
	    {x} <- s_nxt, {x} : ty_gen,
	    ty_gen genOf ty,
	    [[ e ^ (s) : ty ]].
	    
	  Stat[[ Exp(e) ^ (s, s_nxt) ]] := 
	    s == s_nxt,
	    [[ e ^ (s) : ty ]].
	
	rules // numbers
	    
	  [[ Num(x) ^ (s) : NumT() ]].
	  
	  [[ Pow(e1, e2) ^ (s) : NumT() ]] := 
	     [[ e1 ^ (s) : NumT() ]], 
	     [[ e2 ^ (s) : NumT() ]]. 
	  [[ Mul(e1, e2) ^ (s) : NumT() ]] := 
	     [[ e1 ^ (s) : NumT() ]], 
	     [[ e2 ^ (s) : NumT() ]]. 
	  [[ Add(e1, e2) ^ (s) : NumT() ]] := 
	     [[ e1 ^ (s) : NumT() ]], 
	     [[ e2 ^ (s) : NumT() ]]. 
	  [[ Sub(e1, e2) ^ (s) : NumT() ]] := 
	     [[ e1 ^ (s) : NumT() ]], 
	     [[ e2 ^ (s) : NumT() ]].  
	  [[ Div(e1, e2) ^ (s) : NumT() ]] := 
	     [[ e1 ^ (s) : NumT() ]], 
	     [[ e2 ^ (s) : NumT() ]].
	   
	  [[ Eq(e1, e2) ^ (s)  : BoolT() ]] := 
	     [[ e1 ^ (s) : NumT() ]], 
	     [[ e2 ^ (s) : NumT() ]].
	  [[ Lt(e1, e2) ^ (s)  : BoolT() ]] := 
	     [[ e1 ^ (s) : NumT() ]], 
	     [[ e2 ^ (s) : NumT() ]].
	
	rules // booleans
	  
	  [[ True()  ^ (s) : BoolT() ]].
	  [[ False() ^ (s) : BoolT() ]].
	  
	  [[ If(e1, e2, e3) ^ (s) : ty2 ]] := 
	     [[ e1 ^ (s) : BoolT() ]], 
	     [[ e2 ^ (s) : ty2 ]], 
	     [[ e3 ^ (s) : ty3 ]],
	     ty2 == ty3 | error $[branches should have same type] @ e2.
	
	rules // variables and functions
	
	  [[ Var(x) ^ (s) : ty ]] := 
	    {x} -> s, {x} |-> d, d : ty_gen, ty instOf ty_gen.
	    
	  [[ Let(x, e1, e2) ^ (s) : ty2 ]] := 
	     new s', {x} <- s', {x} : ty, s' -P-> s, 
	     [[ e1 ^ (s)  : ty ]], 
	     [[ e2 ^ (s') : ty2 ]].
	    
	  [[ Fun([x], e) ^ (s) : FunT(ty1, ty2) ]] :=
	     new s', {x} <- s', {x} : ty1, s' -P-> s, 
	     [[ e ^ (s') : ty2 ]].
	     
	  [[ App(e1, e2) ^ (s) : ty2 ]] := 
	     [[ e1 ^ (s) : FunT(ty1, ty2) ]], 
	     [[ e2 ^ (s) : ty1 ]].