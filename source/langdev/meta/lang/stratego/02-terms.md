```eval_rst
.. highlight:: str
```

# 2. Terms

Stratego programs transform terms. When using Stratego for program transformation, terms typically represent the abstract syntax tree of a program. But Stratego does not much care what a term represents. Terms can just as well represent structured documents, software models, or anything else that can be rendered in a structured format. The chapters on the [XT Transformation Tools](#) show how to transform a program text into a term by means of parsing, and to turn a term into program text again by means of pretty-printing. From now on we will just assume that we have terms that should be transformed and ignore parsing and pretty-printing.


## 2.1. Annotated Term Format

Terms in Stratego are terms in the _Annotated Term Format_, or _ATerms_ for short. The ATerm format provides a set of constructs for representing trees, comparable to XML or abstract data types in functional programming languages. For example, the code `4 + f(5 * x)` might be represented in a term as:

    Plus(Int("4"), Call("f", [Mul(Int("5"), Var("x"))]))

ATerms are constructed from the following elements:

* **Integer**: An integer constant, that is a list of decimal digits, is an ATerm.

  Examples: `1`, `12343`.
* **String**: A string constant, that is a list of characters between double quotes is an ATerm. Special characters such as double quotes and newlines should be escaped using a backslash. The backslash character itself should be escaped as well.

  Examples: `"foobar"`, `"string with quotes\""`, `"escaped escape character\\ and a newline\n"`.
* **Constructor application**: A constructor is an identifier, that is an alphanumeric string starting with a letter, or a double quoted string.

  A constructor application `c(t1,...,tn)` creates a term by applying a constructor to a list of zero or more terms. For example, the term `Plus(Int("4"),Var("x"))` uses the constructors `Plus`, `Int`, and `Var` to create a nested term from the strings `"4"` and `"x"`.

  When a constructor application has no subterms the parentheses may be omitted. Thus, the term `Zero` is equivalent to `Zero()`. Some people consider it good style to explicitly write the parentheses for nullary terms in Stratego programs. Through this rule, it is clear that a string is really a special case of a constructor application.
* **List**: A list is a term of the form `[t1,...,tn]`, that is a list of zero or more terms between square brackets. While all applications of a specific constructor typically have the same number of subterms, lists can have a variable number of subterms. The elements of a list are typically of the same type, while the subterms of a constructor application can vary in type.

  Example: The second argument of the call to `"f"` in the term `Call("f",[Int("5"),Var("x")])` is a list of expressions.
* **Tuple**: A tuple `(t1,...,tn)` is a constructor application without a constructor.

  Example: `(Var("x"), Type("int"))`
* **Annotation**: The elements defined above are used to create the structural part of terms. Optionally, a term can be annotated with a list terms. These annotations typically carry additional semantic information about the term. An annotated term has the form `t{t1,...,tn}`.

  Example: `Lt(Var("n"),Int("1")){Type("bool")}`. The contents of annotations is up to the application.


## 2.2. Exchanging Terms

The term format described above is used in Stratego programs to denote terms, but is also used to exchange terms between programs. Thus, the internal format and the external format exactly coincide. Of course, internally a Stratego program uses a data-structure in memory with pointers rather than manipulating a textual representation of terms. But this is completely hidden from the Stratego programmer. There are a few facts that are useful to be aware of, though.

> TODO: Is maximal sharing currently preserved?

The internal representation used in Stratego programs maintains maximal sharing of subterms. This means that all occurrences of a subterm are represented by a pointer to the same node in memory. This makes comparing terms in Stratego for syntactic equality a very cheap operation, i.e., just a pointer comparison.

> TODO: picture of tree vs dag representation

When writing a term to a file in order to exchange it with another tool there are several representations to choose from. The textual format described above is the canonical _meaning_ of terms, but does not preserve maximal sharing. Therefore, there is also a _Binary ATerm Format (BAF)_ that preserves sharing in terms. The program _baffle_ can be used to convert between the textual and binary representations.


## 2.3. Inspecting Terms

> TODO: Does `pp-aterm` still exist?

As a Stratego programmer you will be looking a lot at raw ATerms. Stratego pioneers would do this by opening an ATerm file in _emacs_ and trying to get a sense of the structure by parenthesis highlighting and inserting newlines here and there. These days your life is much more pleasant through the tool `pp-aterm`, which adds layout to a term to make it readable. For example, parsing the following program

    let function fact(n : int) : int =
          if n < 1 then 1 else (n * fact(n - 1))
     in printint(fact(10))
    end

produces the following ATerm (say in file `fac.trm`):

    Let([FunDecs([FunDec("fact",[FArg("n",Tp(Tid("int")))],Tp(Tid("int")),
    If(Lt(Var("n"),Int("1")),Int("1"),Seq([Times(Var("n"),Call(Var("fact"),
    [Minus(Var("n"),Int("1"))]))])))])],[Call(Var("printint"),[Call(Var(
    "fact"),[Int("10")])])])

By pretty-printing the term using `pp-aterm` as

> TODO: Is this syntax still correct?

    $ pp-aterm -i fac.trm -o fac-pp.trm --max-term-size 20

we get a much more readable term:

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


## 2.4. Signatures

To use terms in Stratego programs, their constructors should be declared in a signature. A signature declares a number of sorts and a number of constructors for these sorts. For each constructor, a signature declares the number and types of its arguments. For example, the following signature declares some typical constructors for constructing abstract syntax trees of expressions in a programming language:

    signature
      sorts Id Exp
      constructors
               : String -> Id
        Var    : Id -> Exp
        Int    : Int -> Exp
        Plus   : Exp * Exp -> Exp
        Mul    : Exp * Exp -> Exp
        Call   : Id  * List(Exp) -> Exp

Currently, the Stratego compiler only checks the arity of constructor applications against the signature. Still, it is considered good style to also declare the types of constructors in a sensible manner for the purpose of documentation. Also, a later version of the language may introduce type checking.
