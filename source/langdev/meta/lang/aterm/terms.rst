===========================
Annotated Terms
===========================

Terms in Stratego are terms in the *Annotated Term Format*, or *ATerms* for short. The ATerm format provides a set of constructs for representing trees, comparable to XML or algebraic data types in functional programming languages. For example, the expression ``4 + f(5 * x)`` might be represented in a term as::

    Plus(Int("4"), Call("f", [Mul(Int("5"), Var("x"))]))

ATerms are constructed from the following elements:

Integer
  An integer constant, that is a list of decimal digits, is an ATerm.

  Examples: ``1``, ``12343``.
  
String
  A string constant, that is a list of characters between double quotes is an ATerm. Special characters such as double quotes and newlines should be escaped using a backslash. The backslash character itself should be escaped as well.

  Examples: ``"foobar"``, ``"string with quotes\""``, ``"escaped escape character\\ and a newline\n"``.
  
Constructor application
  A constructor is an identifier, that is an alphanumeric string starting with a letter, or a double quoted string.

  A constructor application ``c(t1,...,tn)`` creates a term by applying a constructor to a list of zero or more terms. For example, the term ``Plus(Int("4"),Var("x"))`` uses the constructors ``Plus``, ``Int``, and ``Var`` to create a nested term from the strings ``"4"`` and ``"x"``.

  When a constructor application has no subterms (a "nullary constructor") the parentheses can be omitted. However, this syntax is discouraged because this notation conflicts with variable names in some parts of the language, leading to confusing failures when you meant a variable but accidentally matched agains a constructor. 

List
  A list is a term of the form ``[t1,...,tn]``, that is a list of zero or more terms between square brackets. While all applications of a specific constructor typically have the same number of subterms, lists can have a variable number of subterms. The elements of a list are typically of the same type, while the subterms of a constructor application can vary in type.

  Example: The second argument of the call to ``"f"`` in the term ``Call("f",[Int("5"),Var("x")])`` is a list of expressions.

Tuple
  A tuple ``(t1,...,tn)`` is a constructor application without a constructor.

  Example: ``(Var("x"), Type("int"))``

Annotation
  The elements defined above are used to create the structural part of terms. Optionally, a term can be annotated with a list terms. These annotations typically carry additional semantic information about the term. An annotated term has the form ``t{t1,...,tn}``.

  Example: ``Lt(Var("n"),Int("1")){Type("bool")}``. The contents of annotations is up to the application.


Exchanging Terms
-----------------------------

The term format described above is used in Stratego programs to denote terms, but is also used to exchange terms between programs. Thus, the internal format and the external format exactly coincide. Of course, internally a Stratego program uses a data-structure in memory with pointers rather than manipulating a textual representation of terms. But this is completely hidden from the Stratego programmer. There are a few facts that are useful to be aware of, though.


When writing a term to a file in order to exchange it with another tool there are several representations to choose from. The textual format described above is the canonical _meaning_ of terms, but does not preserve maximal sharing. Therefore, there is also a _Binary ATerm Format (BAF)_ that preserves sharing in terms. The program _baffle_ can be used to convert between the textual and binary representations.

Inspecting Terms
-----------------------------

> TODO: Does `pp-aterm` still exist?

As a Stratego programmer you will be looking a lot at raw ATerms. Stratego pioneers would do this by opening an ATerm file in _emacs_ and trying to get a sense of the structure by parenthesis highlighting and inserting newlines here and there. These days your life is much more pleasant through the tool `pp-aterm`, which adds layout to a term to make it readable. For example, parsing the following program::

    let function fact(n : int) : int =
          if n < 1 then 1 else (n * fact(n - 1))
     in printint(fact(10))
    end

produces the following ATerm (say in file `fac.trm`)::

    Let([FunDecs([FunDec("fact",[FArg("n",Tp(Tid("int")))],Tp(Tid("int")),
    If(Lt(Var("n"),Int("1")),Int("1"),Seq([Times(Var("n"),Call(Var("fact"),
    [Minus(Var("n"),Int("1"))]))])))])],[Call(Var("printint"),[Call(Var(
    "fact"),[Int("10")])])])

By pretty-printing the term using `pp-aterm` as

> TODO: Is this syntax still correct?

    $ pp-aterm -i fac.trm -o fac-pp.trm --max-term-size 20

we get a much more readable term::

    Let(
      [ FunDecs(
          [ FunDec(
              "fact"
            , [FArg("n", Tp(Tid("int")))]
            , Tp(Tid("int"))
            , If(
                Lt(Var("n"), Int("1"))
              , Int("1")
              , Seq([ Times(Var("n"), Call(Var("fact"), [Minus(Var("n"), Int("1"))]))
                    ])
              )
            )
          ]
        )
      ]
    , [ Call(Var("printint"), [Call(Var("fact"), [Int("10")])])
      ]
    )

