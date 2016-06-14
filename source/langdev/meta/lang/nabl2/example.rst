Example Specification for PCF
=============================

We show an NaBL2 specification for a simple PCF language. The language
contains the following grammar rules

.. code-block:: sdf3

   sorts Expr
 
   context-free syntax
 
     Expr.Const    = INT
     Expr.BinExpr  = [[Expr] [BinOp] [Expr]]
     Expr.Ifz      = [ifz [Expr] then [Expr] else [Expr]]
  
     Expr.Fun      = [fun [ID] -> [Expr]]
     Expr.App      = [[Expr] [Expr]]
     Expr.Ref      = ID

The NaBL2 specification defines constraint generation rules for every
syntactic construct, and a rule to start the collection process

.. code-block:: nabl2

   module analysis/pcf
   
   imports signatures/-
   
   type signatures
   
     IntTy()
     FunTy(type,type)
   
   constraint-generation rules
   
     init [[ Start(e) ]] :=
         [[ e ^ (global) : ty ]].
         
     [[ Const(_) ^ (s) : IntTy() ]] :=
       true.
                                           
     [[ BinExpr(e1,_,e2) ^ (s) : IntTy() ]] :=
       [[ e1 ^ (s) : IntTy() ]],
       [[ e2 ^ (s) : IntTy() ]].
       
     [[ Ifz(c,t,f) ^ (s) : ty ]] :=
       [[ c ^ (s) : IntTy() ]],
       [[ t ^ (s) : ty ]],
       [[ f ^ (s) : ty ]].
                                     
     [[ Fun(x,e) ^ (s) : FunTy(ty1,ty2) ]] :=
       [[ e ^ (s') : ty2 ]],
       {x} : ty1,
       {x} <- s',
       s' -P-> s,
       new s'.
    
     [[ App(e1,e2) ^ (s) : ty' ]] :=
       [[ e1  ^ (s) : FunTy(ty,ty') ]],
       [[ e2  ^ (s) : ty ]].
   
     [[ Ref(x) ^ (s) : ty ]] :=
       {x} -> s,
       {x} |-> d,
       d : ty.

