.. highlight:: dynsem

=============================
Dynamic Semantics
=============================

run-time values::

	module dynamics/eval
	imports src-gen/ds-signatures/Calc-sig dynamics/bigdecimal
	signature
	  sorts Value
	  sort aliases
	    Env = Map(ID, Value)
	  constructors
	    NumV  : BigDecimal -> Value
	    BoolV : Bool -> Value
	    ClosV : ID * Exp * Env -> Value
	  variables
	    v : Value
	  components
	    E : Env

evaluation of program::
	    
	signature
	  arrows
	    Program -init-> Value
	rules
	  Program(e) -init-> v
	  where E {} |- e --> v

evaluation of expressions::
	
	signature
	  arrows
	    Exp --> Value
	rules // numbers
	  
	  Num(n) --> NumV(parseB(n))  
	  
	  Pow(NumV(i), NumV(j)) --> NumV(powB(i, j))
	  Mul(NumV(i), NumV(j)) --> NumV(mulB(i, j))
	  Div(NumV(i), NumV(j)) --> NumV(divB(i, j))
	  Sub(NumV(i), NumV(j)) --> NumV(subB(i, j))
	  Add(NumV(i), NumV(j)) --> NumV(addB(i, j))
	  
	  Lt(NumV(i), NumV(j)) --> BoolV(ltB(i, j))
	  Eq(NumV(i), NumV(j)) --> BoolV(eqB(i, j))
	
	signature
	  arrows  
	    ift(Value, Exp, Exp) --> Value
	rules // booleans
	  
	  False() --> BoolV(false)
	  True() --> BoolV(true)
	  
	  If(v1, e2, e3) --> ift(v1, e2, e3)
	  
	  ift(BoolV(true), e2, _) --> e2
	  ift(BoolV(false), _, e3) --> e3
	
	rules // variables and functions
	  
	  E |- Var(x) --> E[x]
	  
	  E |- Fun([x], e) --> ClosV(x, e, E)
	  
	  E |- Let(x, v1, e2) --> v
	  where E {x |--> v1, E} |- e2 --> v
	  
	  App(ClosV(x, e, E), v_arg) --> v
	  where E {x |--> v_arg, E} |- e --> v
	  
	signature
	  arrows
	    List(Stat) --> Value
	    Stat --> (Value * Env)
	rules // top-level statements
	
	  [stat] : List(Stat) --> v
	  where stat --> (v, _)
	    
	  [stat | stats@[_|_]] : List(Stat) --> v
	  where stat --> (_, E); E |- stats --> v
	  
	  E |- Bind(x, v) --> (v, {x |--> v, E})
	  
	  E |- Exp(v) --> (v, E)
	 
Native Operators
-----------------------

declaration::

	module dynamics/bigdecimal
	signature      
	  native datatypes  
	    "java.math.BigDecimal" as BigDecimal { }
	  native operators
	    parseB : String -> BigDecimal 
	    addB : BigDecimal * BigDecimal -> BigDecimal
	    powB : BigDecimal * BigDecimal -> BigDecimal
	    subB : BigDecimal * BigDecimal -> BigDecimal
	    mulB : BigDecimal * BigDecimal -> BigDecimal
	    divB : BigDecimal * BigDecimal -> BigDecimal
	    ltB  : BigDecimal * BigDecimal -> Bool
	    eqB  : BigDecimal * BigDecimal -> Bool
	    
Java Implementation
-------------------------


	   