.. highlight:: sdf3

==========================
Syntax Definition
==========================

We start with the definition of the concrete syntax of Calc using the syntax definition formalism SDF3. A syntax definition formalism is a language for defining all aspects of the syntax of a programming language. That goes well beyond a language for defining just the grammar; SDF3 also covers the definition of lexical syntax, AST constructors, formatting directives, and more.

Modules
---------------

To start with, syntax definitions consist of modules that can import other syntax modules.
This is useful for dividing a large grammar into parts, but also for reusing a standard language component (e.g. expressions) between language definitions, or for composing the syntax of different languages.
We first examine the `main syntax module <https://github.com/MetaBorgCube/metaborg-calc/blob/master/org.metaborg.lang.calc/syntax/Calc.sdf3>`_ for Calc, which is named after the language and which imports module ``CalcLexical`` which defines the lexical syntax of the language::

	module Calc
	imports CalcLexical
	
The module defines the sorts ``Program`` and ``Exp`` as start symbols, which means that parsing starts with these sorts::

	context-free start-symbols Program Exp
	
Context-Free Syntax
--------------------------

Syntactically, a language is a set of well-formed sentences.
(In programming languages, sentences are typically known as programs.)
Sentences are typically formed by composing different kinds of phrases, such as identifiers, constants, expressions, statements, functions, and modules.
In grammar terminology there are two broad categories of phrases, *terminals* and *non-terminals*. 
In SDF3 we use *sorts* to identify both categories.
For Calc we start with defining the ``Program`` and ``Stat`` sorts::

	sorts Program Stat	
	
	
A grammar consists of rules (known as productions) for composing phrases from sub-phrases. 
A Calc program consists of a list of statements that are either bindings that bind the value of an expression to a variable (identifier) or expression statements. 
This is defined by the following productions::

	context-free syntax    
	
	  Program.Program = <<{Stat "\n"}+>>
	  
	  Stat.Bind = <<ID> = <Exp>;>
	  Stat.Exp  = <<Exp>;>

If we take a closer look at the ``Stat.Bind`` production we see the following ingredients:

* The production defines one of two altneratives for the ``Stat`` sort. The alternatives of a sort are defined by separate productions. This makes it possible to introduce productions in an order that makes sense for presenting a language definition. Instead of defining all productions for a sort in one block, it is rather possible to define the productions for different sorts that together define a language concept together. Furthermore, it enables `modular` definition of syntax.

* The body a production defines the composition of sub-phrases that it corresponds to. Thus, the body ``<<ID> = <Exp>;>`` defines a bind statement as the composition of an identifier, followed by an equal sign, followed by an expression, terminated by a semicolon.

* The body is known as a `template` and uses inverse quotation. The template makes everything inside literal elements of the text to be parsed, except for the quasi-quoted sorts (``<ID>`` and ``<Exp>``). 

* The sub-phrases are implicitly separated by layout (whitespace and comments). The definition of layout is not built-in. We will see the definition of the layout for Calc when we discuss lexical syntax below. 
	 
* The constructor is used to construct abstract syntax tree nodes. Thus, the ``Bind`` constructor creates trees with two arguments trees for the identifier (``ID``) and expression (``Exp``) subtrees; in abstract syntax we leave out the literals and layout.

Note that a program is defined as a list of one or more statements, which could be expressed with the regular expression operator `+` as ``Stat+``. 
The SDF3 notation ``{Sort sep}+`` denotes a list of ``Sort`` phrases `separated` by ``sep``.
For example, ``{Exp ","}+`` is a list of one or more expressions separated by commas.
In the definition of statement lists we use a newline as separator. However, this does not imply that statements should be separated by newlines, but rather that newlines are inserted when formatting a program, as we will discuss below.


Expressions
-------------------------

Sorts and productions give us the basic concepts for defining syntax.
Calc programs essentially consist of a sequence of expressions.
So, the bulk of the its syntax definition consists of productions for various expression forms denoted by the ``Exp`` sort::
	  
	sorts Exp
	context-free syntax 	  
	  Exp = <(<Exp>)> {bracket}
	  
The `bracket` production defines that we can enclose an expression in parentheses. The ``bracket`` annotation states that we can ignore this production when constructing abstract syntax trees. That is, the abstract syntax tree for ``(x + 1)`` is the same as the abstract syntax tree for ``x + 1``.
	  
	  
Operator Syntax
-------------------------

Operators are the workhorse of a language such as Calc. 
They capture the domain-specific operations that the language is built around.
We start with the syntax of arithmetic operators::
	
	context-free syntax // numbers
	  Exp.Num = NUM
	  Exp.Min = <-<Exp>>
	  Exp.Pow = <<Exp> ^ <Exp>> {right}
	  Exp.Mul = <<Exp> * <Exp>> {left}
	  Exp.Div = <<Exp> / <Exp>> {left}
	  Exp.Sub = <<Exp> - <Exp>> {left, prefer}
	  Exp.Add = <<Exp> + <Exp>> {left}
	  	  
Note that the concrete syntax is directly aligned with the abstract syntax. 
An addition is represented as the composition of two expression and the `+` symbol.
This is best illustrated using term notation for abstract syntax trees.
The term ``C(t1, ..., tn)`` denotes the abstract syntax tree for a production with constructor ``C`` and ``n`` sub-trees.
For example, the term ``Add(Num("1"), Var("x"))`` represents the abstract syntax tree for the expression ``1 + x``.

The consequence of this direct alignment is that the grammar is ambiguous.
According to the ``Exp.Add`` production there are two ways to parse the expression ``1 + x + y``, i.e. as ``Add(Add(Num("1"), Var("x")), Var("y"))`` or as ``Add(Num("1"), Add(Var("x"), Var("y")))``.

A common approach to disambiguate the grammar for an expression language is by encoding the associativity and precedence of operators in the productions using additional sorts to represent precedence levels. However, that leads to grammars that are hard to understand and maintain and that do not have a one-to-one correspondence to the desired abstract syntax.

In SDF3, ambiguous expression syntax can be `declaratively` disambiguated using separate associativity and priority declarations.
For example, the ``Exp.Add`` production above defines that addition is left associative.
That is, the expression ``1 + x + y`` should be interpreted as ``Add(Add(Num("1"), Var("x")), Var("y"))``, i.e. ``(1 + x) + y``.
The other operators are disambiguated similarly according to `standard mathematical conventions <https://en.wikipedia.org/wiki/Operator_associativity>`_.
Note that power (exponentiation) is `right` associative, i.e. ``x ^ y ^ z`` is equivalent to ``x ^ (y ^ z)``.

comparison operators::
	  
	context-free syntax // numbers
	  Exp.Eq  = <<Exp> == <Exp>> {non-assoc}
	  Exp.Neq = <<Exp> != <Exp>> {non-assoc}
	  Exp.Gt  = [[Exp] > [Exp]]  {non-assoc}
	  Exp.Lt  = [[Exp] < [Exp]]  {non-assoc}
	  
Non-assoc means that a phrase such as ``a < b == true`` is not syntactically well-formed. 
One should use parentheses, for example ``(a < b) == true``, to explicitly indicate the disambiguation.
	
booleans::

	context-free syntax // booleans
	
	  Exp.True  = <true>
	  Exp.False = <false>
	  Exp.Not   = <!<Exp>>
	  Exp.And   = <<Exp> & <Exp>> {left}
	  Exp.Or    = <<Exp> | <Exp>> {left}
	  
	  Exp.If = <  
	    if(<Exp>)
	      <Exp> 
	    else 
	      <Exp>
	  > 

variables::
	
	context-free syntax // variables and functions
	
	  Exp.Var = ID
	  Exp.Let = <
	    let <ID> = <Exp> in
	    <Exp>
	  >
	  Exp.Fun = <\\ <ID+> . <Exp>>
	  Exp.App = <<Exp> <Exp>> {left}

Disambiguation
---------------------



priorities::
	   
	context-free priorities
	  Exp.Min
	  > Exp.App 
	  > Exp.Pow 
	  > {left: Exp.Mul Exp.Div} 
	  > {left: Exp.Add Exp.Sub} 
	  > {non-assoc: Exp.Eq Exp.Neq Exp.Gt Exp.Lt}
	  > Exp.Not 
	  > Exp.And 
	  > Exp.Or 
	  > Exp.If
	  > Exp.Let 
	  > Exp.Fun
	
	sorts Type
	context-free syntax
	  Type.NumT  = <Num>
	  Type.BoolT = <Bool>
	  Type.FunT  = [[Exp] -> [Exp]] {right}
	  Type       = <(<Type>)> {bracket}
	
	template options
	  ID = keyword {reject}
	  

Lexical Syntax
--------------------------

lexical syntax::

	module CalcLexical
	
	lexical syntax
	  ID = [a-zA-Z] [a-zA-Z0-9]* 
	lexical restrictions
	  ID -/- [a-zA-Z0-9\_]
	  
	lexical syntax // numbers  
	  INT      = "-"? [0-9]+   
	  IntGroup = [0-9][0-9][0-9]
	  IntPref  = ([0-9] | ([0-9][0-9])) ","
	  INT      = IntPref? {IntGroup ","}+
	  FLOAT    = INT "." [0-9]+
	  NUM      = INT | FLOAT
	lexical restrictions
	  INT   -/- [0-9]
	  FLOAT -/- [0-9]
	  NUM   -/- [0-9]
	  
	lexical syntax 
	  STRING         = "\"" StringChar* "\"" 
	  StringChar     = ~[\"\n] 
	  StringChar     = "\\\"" 
	  StringChar     = BackSlashChar 
	  BackSlashChar  = "\\" 
	lexical restrictions 
	  // Backslash chars in strings may not be followed by "  
	  BackSlashChar -/- [\"]
	  
	lexical syntax // layout: whitespace and comments
	  LAYOUT         = [\ \t\n\r] 
	  CommentChar    = [\*] 
	  LAYOUT         = "/*" InsideComment* "*/" 
	  InsideComment  = ~[\*] 
	  InsideComment  = CommentChar 
	  LAYOUT         = "//" ~[\n\r]* NewLineEOF 
	  NewLineEOF     = [\n\r] 
	  NewLineEOF     = EOF 
	  EOF            =  
	  
	lexical restrictions 
	  CommentChar -/- [\/]
	  // EOF may not be followed by any char  
	  EOF         -/- ~[]
	  
	context-free restrictions
	  // Ensure greedy matching for comments  
	  LAYOUT? -/- [\ \t\n\r]
	  LAYOUT? -/- [\/].[\/]
	  LAYOUT? -/- [\/].[\*]

	  
Grammar Interpretations
--------------------------

A grammar can be interpreted for (at least) three different operations:

* Parsing: recognizing sub-phrases

* Constructing trees: schema for well-formed abstract syntax trees

* Formatting: ``{Stat "\n"}+``


