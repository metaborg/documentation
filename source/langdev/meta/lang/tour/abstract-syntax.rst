.. highlight:: stratego

=============================
Abstract Syntax
=============================

signature::

	module signatures/Calc-sig
	
	imports signatures/CalcLexical-sig
	
	signature
	  sorts Program Exp Type
	  constructors
	    Program       : List(Stat) -> Program
	    Exp           : Exp -> Stat
	    Bind          : ID * Exp -> Stat
	    Program-Plhdr : Program
	    Stat-Plhdr    : Stat
	    ID-Plhdr      : ID
	    Exp-Plhdr     : Exp
	    Num           : NUM -> Exp
	    Min           : Exp -> Exp
	    Pow           : Exp * Exp -> Exp
	    Mul           : Exp * Exp -> Exp
	    Div           : Exp * Exp -> Exp
	    Sub           : Exp * Exp -> Exp
	    Add           : Exp * Exp -> Exp
	    Eq            : Exp * Exp -> Exp
	    Neq           : Exp * Exp -> Exp
	    Gt            : Exp * Exp -> Exp
	    Lt            : Exp * Exp -> Exp
	    NUM-Plhdr     : NUM
	    Exp-Plhdr     : Exp
	    True          : Exp
	    False         : Exp
	    Not           : Exp -> Exp
	    And           : Exp * Exp -> Exp
	    Or            : Exp * Exp -> Exp
	    If            : Exp * Exp * Exp -> Exp
	    Exp-Plhdr     : Exp
	    Var           : ID -> Exp
	    Let           : ID * Exp * Exp -> Exp
	    Fun           : List(ID) * Exp -> Exp
	    App           : Exp * Exp -> Exp
	    ID-Plhdr      : ID
	    Exp-Plhdr     : Exp
	    NumT          : Type
	    BoolT         : Type
	    FunT          : Exp * Exp -> Type
	    Exp-Plhdr     : Exp
		    