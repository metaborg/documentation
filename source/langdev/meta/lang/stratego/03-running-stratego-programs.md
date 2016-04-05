```eval_rst
.. highlight:: str
```

# 3. Running Stratego Programs

Now let's see how we can actually transform terms using Stratego programs. In the rest of this chapter we will first look at the structure of Stratego programs, and how to compile and run them. In the next chapters we will then see how to define transformations.


## 3.1. Compiling Stratego Programs

The simplest program you can write in Stratego is the following `identity.str` program:

    module identity
    imports list-cons
    strategies
      main = id

It features the following elements: each Stratego file is a module, which has the same name as the file it is stored in without the `.str` extension. A module may import other modules in order to use the definitions in those modules. A module may contain one or more `strategies` sections that introduce new strategy definitions. It will become clear later what strategies and strategy definitions are. Each Stratego program has _one main definition_, which indicates the strategy to be executed on invocation of the program. In the example, the body of this program's main definition is the _identity_ strategy `id`.

Now let's see what this program means. To find that out, we first need to compile it, which we do using the Stratego compiler `strc` as follows:

```bash
$ strc -i identity.str
[ strc | info ] Compiling 'identity.str'
[ strc | info ] Front-end succeeded         : [user/system] = [0.59s/0.56s]
[ strc | info ] Back-end succeeded          : [user/system] = [0.46s/0.16s]
[ strc | info ] C compilation succeeded     : [user/system] = [0.28s/0.23s]
[ strc | info ] Compilation succeeded       : [user/system] = [1.35s/0.95s]
```

The `-i` option of `strc` indicates the module to compile. The compiler also reads all imported modules, in this case the `list-cons.str` module that is part of the Stratego library and that `strc` magically knows how to find. The compiler prints some information about what it is doing, i.e., the stages of compilation that it goes through and the times for those stages. You can turn this off using the argument `--verbose 0`. However, since the compiler is not very fast, it may be satisfying to see something going on.

The result of compilation is an executable named `identity` after the name of the main module of the program. Just to satisfy our curiosity we inspect the file system to see what the compiler has done:

```bash
$ ls -l identity*
-rwxrwxr-x  1 7182 Sep  7 14:54 identity*
-rw-------  1 1362 Sep  7 14:54 identity.c
-rw-rw-r--  1  200 Sep  7 14:54 identity.dep
-rw-rw-r--  1 2472 Sep  7 14:54 identity.o
-rw-rw-r--  1   57 Sep  7 13:03 identity.str
```

Here we see that in addition to the executable the compiler has produced a couple of other files. First of all the `identity.c` file gives away the fact that the compiler first translates a Stratego program to C and then uses the C compiler to compile to machine code. The `identity.o` file is the result of compiling the generated C program. Finally, the contents of the `identity.dep` file will look somewhat like this:

```bash
identity: \
        /usr/local/share/stratego-lib/collection/list/cons.rtree \
        /usr/local/share/stratego-lib/list-cons.rtree \
        ./identity.str
```

It is a rule in the Make language that declares the dependencies of the `identity` program. You can include this file in a `Makefile` to automate its compilation. For example, the following `Makefile` automates the compilation of the `identity` program:

```make
include identity.dep

identity : identity.str
        strc -i identity.str
```

Just invoke `make` on the command-line whenever you change something in the program.

Ok, we were digressing a bit. Let's turn back to finding out what the `identity` program does. When we execute the program with some arbitrary arguments on the command-line, this is what happens:

```bash
$ ./identity foo bar
["./identity","foo","bar"]
```

The program writes to `stdout` the list of command-line arguments as a list of strings in the ATerm format. So what we have learned is that a Stratego program applies its main strategy to the list of command-line arguments, and writes the resulting term to `stdout`. Since the strategy in the `identity` program is the identity transformation it just writes the original command-line arguments (as a term).


## 3.2. Basic Input and Output

That was instructive, but not very useful. We are not interested in transforming lists of strings, but rather programs represented as terms. So we want to read a term from a file, transform it, and write it to another file. Let's open the bag of tricks. The `identity-io` program improves the previous program:

    module identity-io
    imports libstrategolib
    strategies
      main = io-wrap(id)

The program looks similar to the previous one, but there are a couple of differences. First, instead of importing module `list-cons`, this module imports `libstrategolib`, which is the interface to the separately compiled Stratego library. This library provides a host of useful strategies that are needed in implementing program transformations. Part IV gives an overview of the Stratego library, and we will every now and then use some useful strategies from the library before we get there.

Right now we are interested in the `io-wrap` strategy used above. It implements a wrapper strategy that takes care of input and output for our program. To compile the program we need to link it with the `stratego-lib` library using the `-la` option:

```bash
$ strc -i identity-io.str -la stratego-lib
```

What the relation is between `libstrategolib` and `stratego-lib` will become clear later; knowing that it is needed to compile programs using `libstrategolib` suffices for now.

If we run the compiled `identity-io` program with its `--help` option we see the standard interface supported by the `io-wrap` strategy:

```bash
$ ./identity-io --help
Options:
   -i f|--input f   Read input from f
   -o f|--output f  Write output to f
   -b               Write binary output
   -S|--silent      Silent execution (same as --verbose 0)
   --verbose i      Verbosity level i (default 1)
                    ( i as a number or as a verbosity descriptor:
                      emergency, alert, critical, error,
                      warning, notice, info, debug, vomit )
   -k i | --keep i  Keep intermediates (default 0)
   --statistics i  Print statistics (default 0 = none)
   -h|-?|--help     Display usage information
   --about          Display information about this program
   --version        Same as --about
```

The most relevant options are the `-i` option for the input file and the `-o` option for the output file. For instance, if we have some file `foo-bar.trm` containing an ATerm we can apply the program to it:

```bash
$ echo "Foo(Bar())" > foo-bar.trm
$ ./identity-io -i foo-bar.trm -o foo-bar2.trm
$ cat foo-bar2.trm
Foo(Bar)
```

If we leave out the `-i` and/or `-o` options, input is read from `stdin` and output is written to `stdout`. Thus, we can also invoke the program in a pipe:

```bash
$ echo "Foo(Bar())" | ./identity-io
Foo(Bar)
```

Now it might seem that the `identity-io` program just copies its input file to the output file. In fact, the `identity-io` does not just accept any input. If we try to apply the program to a text file that is not an ATerm, it protests and fails:

```bash
$ echo "+ foo bar" | ./identity-io
readFromTextFile: parse error at line 0, col 0
not a valid term
./identity: rewriting failed
```

So we have written a program to check if a file represents an ATerm.


## 3.3. Combining Transformations

A Stratego program based on `io-wrap` defines a transformation from terms to terms. Such transformations can be combined into more complex transformations, by creating a chain of tool invocations. For example, if we have a Stratego program `trafo-a` applying some undefined `transformation-a` to the input term of the program

    module trafo-a
    imports libstrategolib
    strategies
      main = io-wrap(transformation-a)
      transformation-a = ...

and we have another similar program `trafo-b` applying a `transformation-b`:

    module tool-b
    imports libstrategolib
    strategies
      main = io-wrap(transformation-b)
      transformation-b = ...

then we can combine the transformations to transform an `input` file to an `output` file using a Unix pipe, as in

```bash
$ tool-a -i input | tool-b -o output
```

or using an intermediate file:

```bash
$ tool-a -i input -o intermediate
$ tool-b -i intermediate -o output
```

## 3.4. Running Programs Interactively with the Stratego Shell

We have just learned how to write, compile, and execute Stratego programs. This is the normal mode for development of transformation systems with Stratego. Indeed, we usually do not invoke the compiler from the command-line _by hand_, but have an automated build system based on (auto)make to build all programs in a project at once. For learning to use the language this can be rather laborious, however. Therefore, we have also developed the [Stratego Shell](http://releases.strategoxt.org/strategoxt-manual/unstable/manual/chunk-book/ref-stratego-shell.html), an interactive interpreter for the Stratego language. The shell allows you to type in transformation strategies on the command-line and directly seeing their effect on the current term. While this does not scale to developing large programs, it can be instructive to experiment while learning the language. In the following chapters we will use the stratego-shell to illustrate various features of the language.

Here is a short session with the Stratego Shell that shows the basics of using it:

```bash
$ stratego-shell
stratego> :show
()
stratego> !Foo(Bar())
Foo(Bar)
stratego> id
Foo(Bar)
stratego> fail
command failed
stratego> :show
Foo(Bar)
stratego> :quit
Foo(Bar)
$
```

The shell is invoked by calling the command `stratego-shell` on the regular command-line. The `stratego>` prompt then indicates that you have entered the Stratego Shell. After the prompt you can enter strategies or special shell commands.

Strategies are the statements and functions of the Stratego language. A strategy transforms a term into a new term, or fails. The term to which a strategy is applied, is called the _current term_. In the Stratego Shell you can see the current term with `:show`. In the session above we see that the current term is the empty tuple if you have just started the Stratego Shell. At the prompt of the shell you can enter strategies. If the strategy succeeds, then the shell will show the transformed term, which is now the new current term. For example, in the session above the strategy `!Foo(Bar())` replaces the current term with the term `Foo(Bar())`, which is echoed directly after applying the strategy. The next strategy that is applied is the identity strategy `id` that we saw before. Here it becomes clear that it just returns the term to which it is applied. Thus, we have the following general scheme of applying a strategy to the current term:

```bash
current term
stratego> strategy expression
transformed current
stratego>
```

Strategies can also fail. For example, the application of the `fail` strategy always fails. In the case of failure, the shell will print a message and leave the current term untouched:

```bash
current term
stratego> strategy expression
command failed
stratego> :show
current term
```

Finally, you can leave the shell using the `:quit` command.

The Stratego Shell has a number of non-strategy commands to operate the shell configuration. Theses commands are recognizable by the `:` prefix. The `:help` command tells you what commands are available in the shell:

```text
$ stratego-shell
stratego> :help

Rewriting
  strategy          rewrite the current subject term with strategy

Defining Strategies
  id = strategy     define a strategy  (doesn't change the current subject term)
  id : rule         define a rule      (doesn't change the current subject term)
  import modname    import strategy definitions from 'modname' (file system or xtc)
  :undef id         delete defintions of all strategies 'id'/(s,t)
  :undef id(s,t)    delete defintion of strategy 'id'/(s,t)
  :reset            delete all term bindings, all strategies, reset syntax.

Debugging
  :show             show the current subject term
  :autoshow on|off  show the current subject term after each rewrite
  :binding id       show term binding of id
  :bindings         show all term bindings
  :showdef id       show defintions of all strategies 'id'/(s,t)
  :showdef id(s,t)  show defintion of strategy 'id'/(s,t)
  :showast id(s,t)  show ast of defintion of strategy 'id'/(s,t)

Concrete Syntax
  :syntax defname   set the syntax to the sdf definition in 'defname'.

XTC
  :xtc import pathname

Misc
  :include file     execute command in the script of `file`
  :verbose int      set the verbosity level (0-9)
  :clear            clear the screen
  :exit             exit the Stratego Shell
  :quit             same as :exit
  :q                same as :exit
  :about            information about the Stratego Shell
  :help             show this help information
stratego>
```

## 3.5. Summary

Let's summarize what we have learned so far about Stratego programming.

First, a Stratego program is divided into modules, which reside in files with extension `.str` and have the following general form:

    module mod0
    imports libstrategolib mod1 mod2
    signature
      sorts A B C
      constructors
        Foo : A -> B
        Bar : A
    strategies
      main = io-wrap(foo)
      foo = id

Modules can import other modules and can define signatures for declaring the structure of terms and can define strategies, which we not really know much about yet. However, the `io-wrap` strategy can be used to handle the input and output of a Stratego program. This strategy is defined in the `libstrategolib` module, which provides an interface to the Stratego Library. The main module of a Stratego program should have a `main` strategy that defines the entry point of the program.

Next, a Stratego program is compiled to an executable program using the Stratego Compiler `strc`.

```bash
$ strc -i mod0 -la stratego-lib
```

The resulting executable applies the `main` strategy to command-line arguments turned into a list-of-strings term. The `io-wrap` strategy interprets these command-line arguments to handle input and output using standard command-line options.

Finally, the Stratego Shell can be used to invoke strategies interactively.

```bash
$ stratego-shell
stratego> id
()
stratego>
```
