# Language Extension

This page describes how to do language extension through the Spoofax mechanism of exporting source files and importing them in the extension project.

## Exporting source files in base language

Export all relevant source files through the metaborg.yaml file.

```
exports:
- language: ATerm
  directory: src-gen/syntax
- language: SDF
  directory: src-gen/syntax
  includes: "**/*.sdf"
- language: TemplateLang
  directory: syntax
  includes: "**/*.sdf3"
- language: Stratego-Sugar
  directory: trans
  includes: "**/*.str"
- language: Stratego-Sugar
  directory: src-gen
  includes: "**/*.str"
  excludes: "nabl2/**/*.str"
- language: Stratego-Sugar
  directory: src-gen/nabl2
  includes: "**/*.str"
- language: EditorService
  directory: src-gen
  includes: "**/*.esv"
- language: EditorService
  directory: editor
  includes: "**/*.esv"
```

Note that you need to export all generated files from the meta languages as well (generated Stratego and SDF from SDF3 and NaBL2 in the above example).

Note that `src-gen/nabl2` needs to be its own export, as it is a stratego root directory.

Note that we export the SDF3 source files in order to be able to extend these in a language extension.

Suggestion: move all exported files into a sub-folder with the base-language name to avoid name clashes in the langugage extension.

## Importing source files in language extension

Import the language in the yaml file:

```
dependencies:
  source:
  - org.metaborg.lang:icedust2:0.6.3-SNAPSHOT
```

Import all syntax by importing the top-level AST construct in SDF3:

```
module myextension

imports
  
  Modules //refers to icedust2/syntax/Modules.sdf3

context-free start-symbols
  
  Start
```

Make the pretty printer work properly by generating it with the base-language name (in metaborg.yaml):

```
language:
  sdf:
    pretty-print: icedust2
```

Import all stratego by importing the main stratego file of the base language:

```
module myextension

imports
  
  icedust2
```

## Limitations

Currently, importing exported source files only works for Spoofax meta language files.

The following types of files need to be copy pasted currently:

- files that need to be exported in the final compiler (no re-exporting)
- native java strategies
- .tbl files (for parsing Stratego mix syntax)
- icon files

More info: http://yellowgrass.org/issue/Spoofax/211