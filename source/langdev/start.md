# Language Development Getting Started

This guide will get you started with language development in Spoofax, within an Eclipse environment.

## Requirements

Spoofax runs on the major operating systems:

* Windows (32 and 64 bits)
* Linux (32 and 64 bits)
* Mac OSX (Intel only)

Spoofax requires a working internet connection to download several libraries when it is first started.
These libraries are cached afterwards, and only need to be re-downloaded when you update Spoofax.

## Installation

To get started with Spoofax, download an Eclipse Mars installation with Spoofax preinstalled for your platform:

* [Windows 32-bits, embedded JRE](http://download.spoofax.org/update/release/2.0.0/eclipse/spoofax-win32-x86-jre-2.0.0.zip)
* [Windows 64-bits, embedded JRE](http://download.spoofax.org/update/release/2.0.0/eclipse/spoofax-win32-x86_64-jre-2.0.0.zip)
* [Linux 32-bits, embedded JRE](http://download.spoofax.org/update/release/2.0.0/eclipse/spoofax-linux-x86-jre-2.0.0.tar.gz)
* [Linux 64-bits, embedded JRE](http://download.spoofax.org/update/release/2.0.0/eclipse/spoofax-linux-x86_64-jre-2.0.0.tar.gz)
* [Mac OS X (Intel only), embedded JRE](http://download.spoofax.org/update/release/2.0.0/eclipse/spoofax-macosx-x86_64-jre-2.0.0.tar.gz)

These are bundled with an embedded Java Runtime Environment (JRE) version 7, such that a JRE on your system is not required.
If your system has a JRE of version 7 or higher installed, and would rather use that, use the following download links instead:

* [Windows 32-bits](http://download.spoofax.org/update/release/2.0.0/eclipse/spoofax-win32-x86-2.0.0.zip)
* [Windows 64-bits](http://download.spoofax.org/update/release/2.0.0/eclipse/spoofax-win32-x86_64-2.0.0.zip)
* [Linux 32-bits](http://download.spoofax.org/update/release/2.0.0/eclipse/spoofax-linux-x86-2.0.0.tar.gz)
* [Linux 64-bits](http://download.spoofax.org/update/release/2.0.0/eclipse/spoofax-linux-x86_64-2.0.0.tar.gz)
* [Mac OS X (Intel only)](http://download.spoofax.org/update/release/2.0.0/eclipse/spoofax-macosx-x86_64-2.0.0.tar.gz)

Unpack the downloaded archive to a location with write access, since Eclipse requires write access to the unpacked Eclipse installation.

```eval_rst
.. warning:: On Windows, do **not** unpack the Eclipse installation into :file:`Program Files`, because no write access is granted there, breaking both Eclipse and Spoofax.
```

```eval_rst
.. warning:: On Ubuntu 16.04, Eclipse is known to have problems with GTK+ 3. To work around this issue, add the following to :file:`eclipse.ini`::

     --launcher.GTK_version
     2

   before the line::

     --launcher.appendVmargs
```

Start up Eclipse, depending on your operating system:

* Windows: open <span class='file'>eclipse.exe</span>
* Linux: open <span class='file'>eclipse</span>
* Mac OSX: open <span class='file'>Eclipse.app</span>

```eval_rst
.. note::
   On Mac OSX, if Eclipse cannot be opened because it is from an unidentified developer, right click :file:`Eclipse.app` and choose :guilabel:`Open` to grant permission to open Eclipse.

   If Eclipse cannot be opened because it is damaged, open the Terminal, navigate to the directory where :file:`Eclipse.app` is located, and execute:

   .. code-block:: bash

      xattr -rc Eclipse.app

   This will clear the attributes that Eclipse has been downloaded from the internet, and grant permission to open Eclipse.
```

## Hello World Language

To get you started, let's do the 'hello world' of language development; the hello world language.
In Eclipse, open the new project dialog by choosing <span class='menuselection'>File -> New -> Project</span> from the main menu.
In the new project dialog, select <span class='menuselection'>Spoofax -> Spoofax language project</span> and press <span class='guilabel'>Next</span> to open the wizard for creating a Spoofax language specification project.
As project name, choose `helloworld`, which will automatically fill in the identifier, name, and extension of the language.
Keep the defaults for the other fields and press <span class='guilabel'>Finish</span> to create the project.
Once the project has been created, open and expand it in the package or project explorer view.

The syntax for the language is specified in the <span class='file'>syntax/helloworld.sdf3</span> SDF3 file.
[SDF3](meta/lang/sdf3.md) is our syntax definition language, from which we derive a parser, pretty-printer, and syntactic completions from your language.
Currently, the syntax contains a single start symbol `Start`, and a production that accepts an empty program: `Start.Empty = <>`.
Remove that production and replace it with the following productions:

```sdf3
  Start.Program = <<Word> <Word>>
  Word.Hello = <hello>
  Word.World = <world>
```

This grammar accepts a program consisting of 2 words, where the words can be `hello` or `world`, with any number of layout characters (whitespace, tabs, empty lines, , comments, etc.) in between.

To observe our changes to the grammar, we must first rebuild the project by selecting <span class='menuselection'>Project -> Build Project</span>.
Create a new file by choosing <span class='menuselection'>File -> New -> File</span>, put the file at the root of the <span class='file'>helloworld</span> project and name it <span class='file'>test.hel</span>.
Open that file and try out the parser by typing `hello world`, any combinations of the 2 words, and with or without layout between words.

If everything went well, the syntax highlighter will highlight the words in purple, which is the default highlighting color for keywords.
To see the abstract syntax tree that the parser derives from your program, select <span class='menuselection'>Spoofax -> Syntax -> Show parsed AST</span>.
If you make an error in the program, for example `hello worl`, an error message will show up indicating where the error is.

## How to proceed?

Guides for developing a language with Spoofax:

* [Declare Your Language](http://metaborgcube.github.io/declare-your-language/) - This book has not been updated for Spoofax 2.0 yet, but most content still applies.
* [Compiler Construction assignments](http://tudelft-in4303.github.io/assignments/) - The Compiler Construction course at TUDelft has practical assignments in which a full [MiniJava](http://www.cambridge.org/us/features/052182060X/) compiler is made in Spoofax. Contact us if you'd like the get the initial Spoofax project (it is secret to prevent fraud).

Reference manuals for our meta-languages:

* [SDF3](meta/lang/sdf3.md)
* [Stratego](meta/lang/stratego/index.rst)
* [NaBL](meta/lang/nabl.md)
* [NaBL2](meta/lang/nabl2/index.rst)
* [DynSem](meta/lang/dynsem/index.rst)
* [SPT](meta/lang/spt.md)

Example language specifications:

* [paplj language](https://github.com/MetaBorgCube/declare-your-language/tree/core/paplj/paplj.full)
