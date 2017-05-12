.. highlight:: esv

.. _esv-lang-manual:

***
ESV
***

The Editor SerVice (ESV) language is a declarative meta-language for configuring the editor services of a language. For example, the following ESV code fragment configures the syntax highlighting for a language, based on the types of tokens::

  module color

  colorer

    keyword    : 153 51 153
    identifier : black
    string     : 177 47 2
    number     : 17 131 22
    operator   : black
    layout     : 63 127 95 italic

We now look at how an ESV file is structured.

Structure
=========

Each ESV file starts by defining a module for the file. Module identifiers must be unique. Modules can be imported with an import statement. For example, the following code fragment defines an ESV file with module ``Main`` and imports module ``Syntax`` and ``Analysis``::

  module Main

  imports

    Syntax
    Analysis

Importing modules means importing all the sections and definitions from that module.

The rest of the ESV file can contain sections for configuring editor services and other aspects of a language. Sections can be defined multiple times. For example, the following code fragment defines an ESV file with several sections::

  module Main

  language

    extensions : ent

  colorer

    keyword    : 153 51 153
    identifier : default

  language

    line comment  : "//"

It sets the extension in a ``language`` section, adds coloring rules in a ``colorer`` section, and sets the line comment to use in a ``language`` section again.

Configuration Sections
======================

Since editor services are a cross-cutting concern, ESV has a lot of cross-cutting configuration for these concerns. We now describe each configuration section in detail.

File Extension
~~~~~~~~~~~~~~

The file extension of your language are set with the ``extensions`` option under the ``language`` section::

  language

    extensions : ent

Multiple extensions can be set with a comma-separated list::

    language

      extensions : ent, entity, entities

This registers the given extensions with Spoofax, which can then identify files to your language based on extensions. This is used to open an editor for your language in an IDE setting, and to process files of your language in a command-line setting.

Syntax
~~~~~~

The SDF parse table file, and which start symbols to use, are set as follows::

  language

    table         : target/metaborg/sdf.tbl
    start symbols : Start

Multiple start symbols can be set with a comma-separated list::

  language

    start symbols : Start, Program

The parse table of your language is set with the ``table`` option. By default, the parse table of an SDF specification is always produced at :file:`target/metaborg/sdf.tbl`. It is only neccessary to change this configuration when a custom parse table is used.
The ``start symbols`` option determine which start symbols to use when an editor is opened. This must be a subset of the start symbols defined in the SDF3 specification of your language.

The syntax for comments are set as follows::

  language

    line comment  : "//"
    block comment : "/*" "*/"

The ``line comment`` option determines how single-line comments are created. It is used by editors to toggle the comment for a single line. For example, in Eclipse, pressing :kbd:`Ctrl-/` (:kbd:`Cmd-/` on macOS), comments or uncomments the line.
The ``block comment`` option determines how multi-line comments are created. It is used similarly, but when a whole block needs to be commented or uncommented. A block comment is determined by two strings denoting the start and end symbols of the block comment.

Fences for bracket matching are set as follows::

  language

    fences : [ ] ( ) { }

The ``fences`` options determines which symbols to use and match for bracket matching. A single fence is defined by a starting and closing symbol. Multiple fences can be set with a space-separated list. Fences are used to do bracket matching in text editors.

.. warning:: Fences can contain multiple characters, but some implementations may not handle bracket matching with multiple fence characters. For example, Eclipse does not handle this case and ignores multi-character fences.

Syntax Highlighting
~~~~~~~~~~~~~~~~~~~

Token-based syntax highlighting is configured in a ``colorer`` section. Such a section can contain *style definitions* and *styling rules*.

Style definitions bind an identifier to a *style* with syntax ``identifier = style`` for reuse later. A style is a foreground (text) color, optional background color, and optional font attributes. For example, the following style definitions bind the ``red``, ``green``, and ``blue`` colors::

  colorer

    red   = 255 0 0
    green = 0 255 0
    blue  = 0 0 255

A color is denoted by its RGB values, with values ranging from 0 to 255.
An optional background color can be set by adding another RGB value::

  colorer

    redWithGreenBackground = 255 0 0 0 255 0

Optional font attributes can be used to make the font bold or italic::

  colorer

    redWithBold   = 255 0 0 bold
    redWithItalic = 255 0 0 italic
    redWithGreenBackgroundWithBoldItalic = 255 0 0 0 255 0 bold italic

Style rules assign styles to matched tokens with syntax ``matcher : styleOrRef``. The left hand side of style rules match a token, whereas the right hand side assigns a style by referring to a previously defined style definition, or by directly assigning a style. For example, the following matches a token type and references a style definition::

  colorer

    operator : black

whereas the following matches a token with a sort and constructor, and directly assigns a style::

  colorer

    ClassBodyDec.MethodDec : 0 255 0


The following matchers on the left-hand side are supported:

- Matching on built-in token types. The following types are supported:

  - ``identifier`` - matches identifiers, found by lexical non-terminals without numbers
  - ``string`` - matches strings, found by lexical non-terminals that include quotation marks
  - ``number`` - matches numbers, found by lexical non-terminals with numbers
  - ``keyword`` - matches keywords, found by terminals in the syntax definition
  - ``operator`` - matches operations, found by terminals that contain just symbols (no characters)
  - ``layout`` - matches layout, such as whitespace and comments, found by layout definition
  - ``unknown`` - matches tokens which the parser was unable to infer a type for

  For example, the following code defines a simple highlighting with token types::

    colorer

      keyword    : 153 51 153
      identifier : black
      string     : 177 47 2
      number     : 17 131 22
      operator   : black
      layout     : 63 127 95 italic

- Matching on sorts of tokens. For example::

    colorer

      ID       : darkblue
      TYPEID   : blue
      JQTYPEID : blue
      PQTYPEID : blue
      FUNCID   : 153 51 0
      JFUNCID  : 153 51 0
      STRING   : 177 47 2

- Matching on sorts of tokens, and the constructor of the term that was created using the token. This uses the ``Sort.Constructor`` syntax. For example::

    colorer

      ClassBodyDec.MethodDec : yellow
      ClassBodyDec.FieldDec  : red

- Matching on the constructor only. This uses the ``_.Constructor`` syntax. For example::

    colorer

      _.Str     : blue
      _.StrCong : blue
      _.QStr    : blue
      _.QDollar : blue
      _.QBr     : gray

Menus
~~~~~

Menus are used to bind actions of your language, such as transformations, to a menu in the IDE.
Menus are defined under a ``menus`` section::

  menus

    menu: "Generate"

This adds a submenu titled ``Generate`` to the menu of your language.
Submenus can be nested under menus, and submenus can be nested as well::

  menus

    menu: "Generate"
      submenu: "To Java"
        submenu: "Abstract"
        end
        submenu: "Concrete"
        end
      end

Actions (sometimes called builders) are defined under a menu or submenu with syntax ``action: "Name" = strategy modifiers``::

  menus

    menu: "Generate"
      action: "To normal form" = to-normal-form (source)
      submenu: "To Java"
        action: "Abstract" = to-java-abstract (openeditor)
        action: "Concrete" = to-java-concrete
      end

An action has a name which is displayed in the menu, an identifier to a Stratego strategy, and optional modifiers. The following modifiers are supported:

- ``(source)`` - indicates that the action is performed on the parsed AST, not the analyzed AST
- ``(openeditor)`` - indicates that the result of the action should be shown in a new text editor

.. _esv-action-signature:

The Stratego strategy that an action refers to has a defined signature. It must take as input a 5-tuple ``(_, _, ast, path, projectPath)``, and must produce either ``None()`` or ``(filename, output)`` when the action produces a file. The 5-tuple has wildcards which are not used by Spoofax any more, but are kept in the signature for compatibility reasons. The following Stratego code is an example of a strategy that implements this signature:

.. code-block:: stratego

   j2m-action:
     (_, _, ast, path, projectPath) -> (outputFile, result)
     with
       outputFile := $[[projectPath]/[<remove-extension> path].mod]
     ; result     := <j2m-main> ast

Modifiers can also be used on menus and submenus, which mean that all nested actions inherit those modifiers. For example, in::

  menus

    menu: "Generate" (source) (openeditor)
      action: "To normal form" = to-normal-form
      submenu: "To Java"
        action: "Abstract" = to-java-abstract
        action: "Concrete" = to-java-concrete
      end

all actions inherit the ``(source)`` and ``(openeditor)`` modifiers on the menu.

Outline
~~~~~~~

An outline is a summary of a file that is shown in a separate view next to a textual editor. An outline is created by a Stratego strategy, but is configured in ESV under the ``views`` section::

  views

    outline view: editor-outline
      expand to level: 3

This configures the ``editor-outline`` Stratego strategy to be used to create outlines, and that outline nodes should be expanded 3 levels deep by default.

.. todo:: Describe input and output signature of the outline strategy.

Hover Tooltips
~~~~~~~~~~~~~~

Hover tooltips show a textual tooltip with extra information, when hovering part of the text. Hover tooltips are created by a Stratego strategy, but are configured in ESV under the ``references`` section::

  references

    hover _ : editor-hover

The identifier after the colon refers to the Stratego strategy that creates the hover tooltip. The Stratego strategy takes an AST node, and either fails if no tooltip should be produced, or returns a tooltip string.

The string may contain a few simple HTML tag to style the output. The following tags are supported:

- ``<br/>`` - line break
- ``<b>text</b>`` - bold
- ``<i>text</i>`` - italics
- ``<pre>code</pre>`` - preformatted (code) text

Compiler
~~~~~~~~

The compiler strategy (frequently called the on-save handler) is used to transform files when they are saved in an editor. In an IDE setting, when a new project is opened, the compiler strategy is also executed on each file in the project, as well as when files change in the background. In a command-line batch compiler setting, it is used to transform all files.

The compiler strategy is configured in ESV with the ``on save`` option::

  language

    on save : compile-file

The identifier after the colon refers to the Stratego strategy that performs the transformation. This strategy must have the :ref:`exact same signature as the one for actions <esv-action-signature>`.

Analyzer and Context
~~~~~~~~~~~~~~~~~~~~

The analyzer strategy is used to perform static analyses such as name and type analysis, on the AST that a parser produces. An analysis context provides a project-wide store to facilitate multi-file analysis and incrementality. There are four ways to configure the analysis, which set the analyzer strategy with option ``observer`` and context with option ``context``.

- No analysis. This disables analysis completely. Do not set an ``observer`` and set the ``context`` to none::

    language

      context : none

- Stratego-based analysis. This allows you to implement your analysis in Stratego::

    language

      context  : legacy
      observer : editor-analyze

  The identifier after the colon refers to the Stratego strategy that performs the analysis. It must take as input a 3-tuple ``(ast, path, projectPath)``. As output it must produce a 4-tuple ``(ast, error*, warning*, note*)``. The following Stratego code is an example of a strategy that implements this signature:

  .. code-block:: stratego

     editor-analyze:
       (ast, path, projectPath) -> (ast', errors, warnings, notes)
       with
         ast'     := <analyze> ast
       ; errors   := <collect-all(check-error)> ast'
       ; warnings := <collect-all(check-warning)> ast'
       ; notes    := <collect-all(check-note)> ast'

- NaBL/TS based analysis. This uses the :ref:`NaBL and TS <nabl-index>` meta-languages for name and type analysis. Your project must have been generated with NaBL+TS as the analyzer. It will produce the following ESV configuration::

    language

      context  : taskengine
      observer : editor-analyze (multifile)

- NaBL2 based analysis. This uses the :ref:`NaBL2 <nabl2-index>` meta-language for name and type analysis. Your project must have been generated with NaBL2 as the analyzer. It will produce the following ESV configuration::

    language

      observer : editor-analyze (constraint)

  By default, the NaBL2 analyzer works in single-file mode and does not consider multi-file name resolution. To enable that, add the ``(multifile)`` modifier::

      language

        observer : editor-analyze (constraint) (multifile)

Reference Resolution
~~~~~~~~~~~~~~~~~~~~

Reference resolution takes an AST node containing a reference, and tries to resolve it to its definition. The resolution is performed by a Stratego strategy, but is configured in ESV under the ``references`` section::

  references

    reference _ : editor-resolve

The identifier after the colon refers to the Stratego strategy that performs the resolution. The Stratego strategy takes an AST node, and either fails if it could not be resolved, or returns an AST node that has an origin location pointing to the definition site.

If you use the :ref:`NaBL and TS <nabl-index>` or :ref:`NaBL2 <nabl2-index>` meta-language to implement name and type analysis, the provided ``editor-resolve`` strategy implements resolution generically.

Stratego
~~~~~~~~

The JAR and CTree files that will be loaded into the Stratego runtime for your language can be configured with the ``provider`` option::

  language

    provider : target/metaborg/stratego.ctree

The extension of the provider should match the format in the :file:`metaborg.yaml` file of your language.

Multiple files can be set by setting the option multiple times::

  language

    provider : target/metaborg/stratego.ctree
    provider : target/custom1.jar
    provider : target/custom2.ctree


Main File
=========

ESV currently does not have a configurable main file. The main ESV file of your language must be located at :file:`editor/Main.esv` or :file:`editor/main.esv`. Every ESV file that is (transitively) imported from the main ESV file is used.
